#!/usr/bin/env python
from __future__ import annotations
from saqc.core.generic import VariableABC, ABC
import pandas as pd
import numpy as np

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from saqc.core.variable import Variable


class UnivariatDataFunc(VariableABC, ABC):
    """
    Functions that alter data.
    - must return a new Variable
    - may set new flags on the new Variable
    - may use the existing old Flags squeezed to a pd.Series
      (see `FlagsFrame.current`) as the initial flags for the
      new Variable
    """

    def clip(self: Variable, lower, upper, flag=-88) -> Variable:
        # keep index
        # alter data
        # initial flags: squeezed old
        result = self.flag_limits(lower, upper, flag=flag).copy()
        result.data.clip(lower, upper, inplace=True)
        return self._constructor(result)

    def interpolate(self: Variable, flag=None) -> Variable:
        # keep index
        # alter data
        # initial flags: squeezed old
        meta = dict(source="interpolate")
        if flag is not None:
            flags = self.flagna(flag).flags
        else:
            flags = self.flags
        data = self.data.interpolate()
        return self._constructor(data, flags)

    def reindex(self: Variable, index=None, method=None) -> Variable:
        # - set new index
        # - reset all flags
        data = self.data.reindex(index, method=method)
        return self._constructor(data)


class UnivariatFlagFunc(VariableABC, ABC):
    def flag_limits(self: Variable, lower=-np.inf, upper=np.inf, flag=9) -> Variable:
        result = self.copy(deep=False)
        mask = (result.data < lower) | (result.data > upper)
        result.flags.append_with_mask(mask, flag)
        return result

    def flag_something(self: Variable, flag=99) -> Variable:
        result = self.copy(deep=False)
        sample = result.data.sample(frac=0.3)
        new = result.flags.template()
        new[sample.index] = flag
        result.flags.append(new)
        return result

    def flagna(self, flag=999):
        result = self.copy(False)
        meta = dict(source="flagna")
        result.flags.append_with_mask(result.data.isna(), flag, meta)
        return result

    def flag_generic(self, func, flag=99):
        # func ==> ``lambda v: v.data != 3``
        new = self.copy()
        mask = func(self.data)
        new.flags.append_with_mask(mask, flag, dict(source="flag_generic"))
        return new