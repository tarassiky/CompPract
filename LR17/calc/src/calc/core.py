import math
from typing import Union


class Calculator:
    """Класс калькулятора с базовыми арифметическими операциями."""

    def add(self, a: Union[int, float], b: Union[int, float]) -> float:
        """Сложение двух чисел."""
        return float(a + b)

    def subtract(self, a: Union[int, float], b: Union[int, float]) -> float:
        """Вычитание двух чисел."""
        return float(a - b)

    def multiply(self, a: Union[int, float], b: Union[int, float]) -> float:
        """Умножение двух чисел."""
        return float(a * b)

    def divide(self, a: Union[int, float], b: Union[int, float]) -> float:
        """Деление двух чисел."""
        if b == 0:
            raise ValueError("Division by zero is not allowed")
        return float(a / b)

    def power(self, a: Union[int, float], b: Union[int, float]) -> float:
        """Возведение в степень."""
        return float(a**b)

    def floor_divide(self, a: Union[int, float], b: Union[int, float]) -> float:
        """Целочисленное деление."""
        if b == 0:
            raise ValueError("Division by zero is not allowed")
        return float(a // b)

    def modulo(self, a: Union[int, float], b: Union[int, float]) -> float:
        """Остаток от деления."""
        if b == 0:
            raise ValueError("Division by zero is not allowed")
        return float(a % b)


def convert_precision(number: float, precision: int = 3) -> float:
    """Округляет число до указанного количества значащих цифр.

    Args:
        number: Число для округления
        precision: Количество значащих цифр (по умолчанию 3)

    Returns:
        Округлённое число
    """
    if number == 0 or precision <= 0:
        return 0.0

    try:
        # Вычисляем порядок округления
        log10 = math.log10(abs(number))
        order = precision - 1 - int(math.floor(log10))

        # Для очень маленьких чисел используем более точное округление
        if abs(number) < 1e-3:
            order += 1

        return round(number, order) if order >= 0 else round(number, order)
    except (ValueError, OverflowError):
        return number
