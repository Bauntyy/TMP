import re
from datetime import datetime
import pandas as pd
from typing import Dict, List, Pattern

def is_invalid_data(pattern: Pattern, value: str, col_name: str = None) -> bool:
    if pd.isna(value):
        return True

    value_str = str(value).strip()

    if value_str == '' or value_str == 'nan':
        return True

    if not bool(pattern.fullmatch(value_str)):
        return True

    if col_name:
        if col_name == 'height':
            # Проверка, что рост в разумных пределах (0.5-2.5 метра)
            try:
                height = float(value_str)
                if height < 0.5 or height > 2.5:
                    return True
            except ValueError:
                pass

        elif col_name == 'longitude':
            # Долгота должна быть в пределах [-180, 180]
            try:
                lon = float(value_str)
                if lon < -180 or lon > 180:
                    return True
            except ValueError:
                pass

        elif col_name == 'date':
            # Проверка корректности даты
            try:
                datetime.strptime(value_str, '%Y-%m-%d')
            except ValueError:
                return True

        elif col_name == 'blood_type':
            # Проверка символов резус-фактора
            # В таблице указано, что отрицательный резус обозначен символом \u2212
            last_char = value_str[-1]
            if last_char not in ['+', '-', '−']:
                return True


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

        for index, value in data[col_name].items():
            if is_invalid_data(pattern, value, col_name):
                invalid_rows.add(index)

    return sorted(invalid_rows)