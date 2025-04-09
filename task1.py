"""
Замикання
Реалізуйте функцію caching_fibonacci, яка створює та використовує кеш для зберігання
 і повторного використання вже обчислених значень чисел Фібоначчі.
"""
from typing import Callable


def caching_fibonacci(cache=None) -> Callable[[int], int]:
    """
    Calculates fibonacci using cache
    :param cache:
    :return: Callable[[int], int] fibonacci
    """
    if cache is None:
        cache = {}

    def fibonacci(n: int) -> int:
        if n <= 0:
            return 0
        if n == 1:
            return 1
        if n in cache:
            return cache[n]

        cache[n] = fibonacci(n-1) + fibonacci(n-2)
        return cache[n]

    return fibonacci

# Отримуємо функцію fibonacci
fib = caching_fibonacci()

# Використовуємо функцію fibonacci для обчислення чисел Фібоначчі
print(fib(10))  # Виведе 55
print(fib(15))  # Виведе 610
