#!/usr/bin/env python
from __future__ import annotations


from typing import Any, TypeVar, Callable, Union, TYPE_CHECKING

try:
    from typing import Self
except ImportError:
    Self = TypeVar("Self")

import pandas as pd

if TYPE_CHECKING:
    from saqc.core.variable import Variable, MaskedVariable, BaseVariable


# Either Variable or SaQC not the Union of both,
# that mean tha a function defined like this `foo(a: VarOrQcT) -> VarOrQcT`
# returns an object of the same type as `a` is.
# It never takes a Variable and return a SaQC object.
VarOrQcT = TypeVar("VarOrQcT", "Variable", "SaQC")

SupportsIndex = Union[pd.DataFrame, "Variable", "FlagsFrame"]
SupportsColumns = Union[pd.DataFrame, "FlagsFrame"]

# VariableT is stricter and ensures that the same subclass of Variable always is
# used. E.g. `def func(a: VariableT) -> variableT: ...` means that if a
# MaskedVariable is passed into a function, a MaskedVariable is always
# returned and if a Variable is passed in, a Variable is always returned.
VariableT = TypeVar("VariableT", bound="BaseVariable")

# to maintain type information across generic functions and parametrization
T = TypeVar("T")

# used in decorators to preserve the signature of the function it decorates
# see https://mypy.readthedocs.io/en/stable/generics.html#declaring-decorators
FuncType = Callable[..., Any]
F = TypeVar("F", bound=FuncType)
