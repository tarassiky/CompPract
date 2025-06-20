from .core import Calculator
from .stats import calculate_std_dev
from tabulate import tabulate
import sys


def run_calculator():
    """Запуск интерактивного калькулятора."""
    calc = Calculator()
    operations = {
        '+': calc.add,
        '-': calc.subtract,
        '*': calc.multiply,
        '/': calc.divide,
        '^': calc.power,
        '//': calc.floor_divide,
        '%': calc.modulo
    }

    print("\nКалькулятор с действиями")
    print("'+' - Сложение")
    print("'-' - Вычитание")
    print("'*' - Умножение")
    print("'/' - Деление")
    print("'^' - Возведение в степень")
    print("'//' - Деление без остатка")
    print("'%' - Деление по модулю\n")

    try:
        num1 = float(input("Число 1: "))
        num2 = float(input("Число 2: "))
        op = input("Оператор: ")

        if op not in operations:
            print("Неизвестная операция")
            return

        result = operations[op](num1, num2)

        table = [
            ["Число 1", "Операция", "Число 2", "Результат"],
            [num1, op, num2, result]
        ]

        print(tabulate(table, headers="firstrow", tablefmt="grid"))

    except ValueError as e:
        print(f"Ошибка: {e}")


def run_stats():
    """Запуск статистических вычислений."""
    print("\nПоиск среднеквадратичного отклонения")
    try:
        count = int(input("Введите количество чисел: "))
        numbers = []
        for i in range(count):
            num = float(input(f"Введите число {i + 1}: "))
            numbers.append(num)

        std_dev = calculate_std_dev(numbers)
        print(f"\nСреднеквадратичное отклонение: {std_dev}\n")

    except ValueError as e:
        print(f"Ошибка: {e}")


def main():
    """Главная функция CLI."""
    while True:
        print("\nВыберите режим:")
        print("1 - Калькулятор")
        print("2 - Статистика")
        print("0 - Выход")

        choice = input("Ваш выбор: ")

        if choice == '1':
            run_calculator()
        elif choice == '2':
            run_stats()
        elif choice == '0':
            print("Выход из программы")
            break
        else:
            print("Неверный ввод, попробуйте снова")


if __name__ == "__main__":
    main()