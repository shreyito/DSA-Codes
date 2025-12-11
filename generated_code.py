def fibonacci(n):
    """
    Calculates the first 'n' numbers of the Fibonacci sequence.

    The Fibonacci sequence is a series of numbers where each number is the
    sum of the two preceding ones, usually starting with 0 and 1.
    (e.g., 0, 1, 1, 2, 3, 5, 8, ...)

    Args:
        n (int): The number of Fibonacci terms to generate.
                 Must be a non-negative integer.

    Returns:
        list: A list containing the first 'n' Fibonacci numbers.

    Raises:
        TypeError: If 'n' is not an integer.
        ValueError: If 'n' is a negative integer.

    Examples:
        >>> fibonacci(0)
        []
        >>> fibonacci(1)
        [0]
        >>> fibonacci(5)
        [0, 1, 1, 2, 3]
        >>> fibonacci(10)
        [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    """
    # Error handling for input type
    if not isinstance(n, int):
        raise TypeError("Input 'n' must be an integer.")

    # Error handling for input value
    if n < 0:
        raise ValueError("Input 'n' must be a non-negative integer.")

    # Base cases for the sequence generation
    if n == 0:
        return []
    elif n == 1:
        return [0]
    
    # Iterative calculation for n > 1
    sequence = [0, 1]
    while len(sequence) < n:
        next_fib = sequence[-1] + sequence[-2]
        sequence.append(next_fib)
        
    return sequence