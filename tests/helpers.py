import os
from typing import Any, NoReturn, Iterator, Iterable, TypeVar

import hypothesis
from hypothesis.strategies import integers, one_of, text

hypothesis.settings.register_profile("ci", max_examples=1000, deadline=100)
hypothesis.settings.register_profile("dev", max_examples=100, deadline=50)
hypothesis.settings.load_profile(
    os.getenv(u'HYPOTHESIS_PROFILE', default='dev'))

any_types = one_of(integers(), text())


def invalidPatternMatch(*args: Any) -> NoReturn:
    assert False, 'Pattern matching failed'


T_co = TypeVar("T_co", covariant=True)


# This must be in the standard library somewhere...
def concat(iterable: Iterable[Iterable[T_co]]) -> Iterator[T_co]:
    return (inner_element for inner_iterator in iterable
            for inner_element in inner_iterator)


PATH_TO_TEST_BASE_DIRECTORY = os.path.dirname(__file__)
