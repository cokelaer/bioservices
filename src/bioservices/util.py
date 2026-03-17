from typing import List, Sequence, Tuple, TypeVar, Union

T = TypeVar("T")


def squash(seq: Union[List[T], Tuple[T, ...]]) -> Union[T, List[T], Tuple[T, ...]]:
    """Return the single element of a one-item sequence, otherwise return the sequence unchanged.

    :param seq: a list or tuple to potentially unwrap.
    :returns: the unwrapped element if *seq* has exactly one item, otherwise *seq* itself.

    Example::

        >>> squash([42])
        42
        >>> squash([1, 2])
        [1, 2]
    """
    value = seq

    if isinstance(value, (list, tuple)) and len(value) == 1:
        value = value[0]

    return value


def sequencify(value: Union[T, List[T], Tuple[T, ...]], type_: type = list) -> Sequence[T]:
    """Wrap a scalar value in a list (or other sequence type) if it is not already a list or tuple.

    :param value: the value to wrap.
    :param type_: the target sequence type (default: ``list``).
    :returns: *value* unchanged if it is already a list or tuple, otherwise a new sequence of
        *type_* containing *value* as its sole element.

    Example::

        >>> sequencify("hello")
        ['hello']
        >>> sequencify([1, 2, 3])
        [1, 2, 3]
        >>> sequencify("hello", type_=tuple)
        ('hello',)
    """
    if not isinstance(value, (list, tuple)):
        value = [value]

    value = type_(value)

    return value
