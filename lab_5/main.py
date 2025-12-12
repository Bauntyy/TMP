from functions import read_json, read_sequence, run_tests, write_results


def main() -> None:
    """Основная функция для запуска тестирования бинарных последовательностей.

    Чтение конфигурации из JSON-файла, загрузка тестовых последовательностей,
    выполнение статистических тестов (NIST) для C++ и Java реализаций,
    сохранение результатов в указанный файл.

    Workflow:
        1. Чтение конфигурации из constants.json
        2. Загрузка бинарных последовательностей из указанных путей
        3. Запуск тестов для каждой последовательности:
            - Frequency Test (частотный тест)
            - Runs Test (тест на чередование)
            - Longest Run of Ones Test (тест длинных серий)
        4. Сохранение результатов сравнения в файл

    Raises:
        FileNotFoundError: Если отсутствуют входные файлы
        ValueError: Если некорректные данные в конфигурации
        Exception: При ошибках записи результатов
    """
    # Загрузка конфигурации и тестовых констант
    constants, PI_i = read_json("constants.json")

    # Получение путей к тестовым данным из конфигурации
    cpp_sequence_path = constants.get("cpp_sequence")
    java_sequence_path = constants.get("java_sequence")
    result_path = constants.get("result_path")
    print(java_sequence_path, cpp_sequence_path)

    # import os
    # print("Текущая рабочая директория:", os.getcwd())

    # Чтение бинарных последовательностей
    cpp_sequence = read_sequence(cpp_sequence_path)
    java_sequence = read_sequence(java_sequence_path)

    # Выполнение статистических тестов
    cpp_results = run_tests(cpp_sequence, PI_i)
    java_results = run_tests(java_sequence, PI_i)
    print(cpp_results, "\n", java_results)

    # Сохранение результатов тестирования
    write_results(result_path, cpp_results, java_results)


if __name__ == "__main__":
    main()