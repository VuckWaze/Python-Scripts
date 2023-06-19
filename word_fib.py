def word_fib(n: int, chars='SL'):
    """
    Generate fibonacci word sequences by self reference.
    """
    if n == 0: return chars[0] # Base case 1
    if n == 1: return chars[1] # Base case 2
    else:      return word_fib(n-1, chars) + word_fib(n-2, chars)