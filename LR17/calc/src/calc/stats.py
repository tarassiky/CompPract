from typing import List
from math import sqrt
from .core import convert_precision


def calculate_mean(numbers: List[float]) -> float:
    """Вычисление среднего значения."""
    return sum(numbers) / len(numbers) if numbers else 0


def calculate_std_dev(numbers: List[float], precision: int = 2) -> float:
    """Вычисление среднеквадратичного отклонения."""
    if not numbers:
        return 0.0

    mean = calculate_mean(numbers)
    variance = sum((x - mean) ** 2 for x in numbers) / len(numbers)
    std_dev = sqrt(variance)
    return convert_precision(std_dev, precision)
