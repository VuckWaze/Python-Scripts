'''
Uses the Taylor/MacLauren series to approximate the trig functions. Might be useful for embedded applications
where a table would take up too much space.

'''

pi: float = 3.14159265359


def floor(x: float) -> int:
  return int(x)


def ceil(x: float) -> int:
  return int(x + 1)


def fact(n: int) -> int:
  if n == 0:
    return 1
  else:
    return n * fact(n - 1)


def sin(x: float) -> float:
  n, r = divmod(x, pi)
  r = r if n % 2 == 0 else -r
  return r - r**3 / (fact(3)) + r**5 / (fact(5)) - r**7 / (fact(7))


def cos(x: float) -> float:
  n, r = divmod(x, 2 * pi)
  r = r if n % 2 == 0 else -r
  size = 12
  return sum([(-1)**(int(i/2)) * r**i/fact(i) for i in range(0, size, 2)])