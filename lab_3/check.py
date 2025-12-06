import re
import pandas as pd
from typing import Dict, List, Pattern

def is_invalid_data(pattern: Pattern, value: str) -> bool:
    """Проверяет значение на невалидность"""
    return not bool(pattern.fullmatch(str(value)))


def find_invalid_rows(validation_patterns: Dict[str, str], data: pd.DataFrame) -> List[int]:
    """Находит строки с ошибками"""
    invalid_rows = set()

    # Скомпилируем все паттерны заранее
    compiled_patterns = {}
    for col_name, pattern_str in validation_patterns.items():
        compiled_patterns[col_name] = re.compile(pattern_str)

    # Проверяем каждую колонку
    for col_name, pattern in compiled_patterns.items():
        if col_name not in data.columns:
            continue

        # Проверяем каждое значение в колонке
        for index, value in data[col_name].items():
            if is_invalid_data(pattern, value):
                invalid_rows.add(index)

    return sorted(invalid_rows)