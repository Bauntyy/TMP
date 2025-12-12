import json
import os
from NIST_test import frequency_test, same_bits_test, longest_sequence_test


def read_json(filename: str) -> tuple[dict, list]:
    """Читает данные из JSON-файла и возвращает константы для тестов.

    Args:
        filename: Имя JSON-файла в той же директории, что и скрипт.

    Returns:
        tuple[dict, list]: Кортеж, содержащий:
            - Все данные из файла (dict)
            - Список констант PI_I (list)

    Note:
        В случае ошибок возвращает пустые dict и list.
    """
    try:
        file_path = os.path.join(os.path.dirname(__file__), filename)
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            PI_constants = data.get("PI_I", [])
            return data, PI_constants
    except FileNotFoundError:
        print(f"Файл {filename} не найден в папке скрипта!")
        return {}, []
    except json.JSONDecodeError:
        print("Ошибка: файл не в формате JSON!")
        return {}, []


def read_sequence(file_path: str) -> str:
    """Читает бинарную последовательность из файла.

    Args:
        file_path: Путь к файлу с последовательностью.

    Returns:
        str: Бинарная последовательность без пробелов.

    Raises:
        Exception: Если файл не найден.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read().replace(" ", "").replace("\n", "")
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {file_path} не найден")


def run_tests(sequence: str, PI_i: list) -> list[str]:
    """Запускает набор статистических тестов для бинарной последовательности.

    Args:
        sequence: Тестируемая бинарная последовательность.
        PI_i: Список констант для теста длинных последовательностей.

    Returns:
        list[str]: Список строк с результатами тестов в формате:
            [
                "Result of frequency bit test: X",
                "Result of run same bit test: Y",
                "Result of longest ones sequence test: Z"
            ]
    """
    results = []
    freq_test_result = frequency_test(sequence)
    results.append(f"Result of frequency bit test: {freq_test_result}")
    run_same_result = same_bits_test(sequence)
    results.append(f"Result of run same bit test: {run_same_result}")
    longest_ones_result = longest_sequence_test(sequence, PI_i)
    results.append(f"Result of longest ones sequence test: {longest_ones_result}")
    return results


def write_results(path: str, cpp_result: list[str], java_result: list[str]) -> None:
    """Записывает результаты тестов в файл.

    Args:
        path: Путь к файлу для записи.
        cpp_result: Результаты тестов для C++ реализации.
        java_result: Результаты тестов для Java реализации.

    Raises:
        Exception: При ошибках записи в файл.
    """
    try:
        with open(path, "w") as file:
            file.write("C++ results:\n")
            for results in cpp_result:
                file.write(results + "\n")
            file.write("JAVA results:\n")
            for results in java_result:
                file.write(results + "\n")
    except IOError as e:
        raise Exception(f"Error while writing to file: {e}")