# make executable
chmod u+x pre-commit
cp pre-commit Universität/ML-Bundesliga/.git/hooks



"""Example tests."""
import pytest


def fib(n):
    """Returns the first n fibonacci numbers, starting with 1, 1, 2, …."""
    if n < 0:
        raise ValueError("Expected a positive number, got: {}".format(n))
    numbers = []
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
        numbers.append(a)
    return numbers


def test_fib_simple_cases():
    assert fib(0) == []
    assert fib(1) == [1]
    assert fib(2) == [1, 1]
    assert fib(5) == [1, 1, 2, 3, 5]

def test_fib_negative():
    with pytest.raises(ValueError):
        assert fib(-1)


@pytest.mark.parametrize("n", [
    10,
    20,
    100,
    1000,
])
def test_fib_arbitrary_length(n):
    result = fib(n)

    assert result[:2] == [1, 1]

    for a, b, c in zip(result, result[1:], result[2:]):
        assert a + b == c

