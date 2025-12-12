import math as m
from scipy.special import gammainc


def frequency_test(binary_sequence: str):
    """Проводит частотный побитовый тест (Frequency Monobit Test) для бинарной последовательности.

       Тест проверяет, является ли количество нулей и единиц в последовательности статистически близким,
       что ожидается для случайной последовательности.

       Args:
           binary_sequence: Бинарная строка, состоящая из символов '0' и '1'.

       Returns:
           float: P-значение теста. Если p-value ≥ 0.01, последовательность считается случайной.

       Raises:
           ValueError: Если входная последовательность пуста.
       """
    if len(binary_sequence) == 0:
        raise ValueError("Последовательность не может быть пустой")
    result = 0

    for bit in binary_sequence:
        if bit == "1":
            result += 1
        else:
            result -= 1

    S_N = abs(result)/m.sqrt(len(binary_sequence))
    p_value = m.erfc(S_N/m.sqrt(2))
    return p_value


def same_bits_test(binary_sequence):
    """Проводит тест на чередование битов (Runs Test) для бинарной последовательности.

       Тест проверяет, является ли количество переходов между нулями и единицами статистически значимым,
       что характерно для случайных последовательностей.

       Args:
           binary_sequence: Бинарная строка, состоящая из символов '0' и '1'.

       Returns:
           float: P-значение теста. Если p-value ≥ 0.01, последовательность считается случайной.

       Raises:
           ValueError: Если входная последовательность пуста.
       """
    if len(binary_sequence) == 0:
        raise ValueError("Последовательность не может быть пустой")

    n = len(binary_sequence)
    unit_of_ones = binary_sequence.count('1') / n

    if abs(unit_of_ones - 0.5) >= 2/m.sqrt(n):
        p_value = 0
        return p_value

    sign_alternations = 0
    for i in range(1, n):
        if binary_sequence[i] != binary_sequence[i-1]:
            sign_alternations += 1

    numerator = abs(sign_alternations - 2 * n * unit_of_ones * (1 - unit_of_ones))
    denominator = 2 * m.sqrt(2 * n) * unit_of_ones * (1 - unit_of_ones)
    p_value = m.erfc(numerator / denominator)
    return p_value


def longest_sequence_test(binary_sequence, PI_i,  block_size = 8):
    """Проводит тест на длиннейшую последовательность единиц в блоках (Longest Run of Ones Test).

       Тест разбивает последовательность на блоки и проверяет распределение максимальных длин серий единиц
       в каждом блоке, сравнивая с теоретически ожидаемым распределением.

       Args:
           binary_sequence: Бинарная строка, состоящая из символов '0' и '1'.
           PI_i: Список теоретических вероятностей для разных длин серий (4 элемента).
           block_size: Размер блока (по умолчанию 8 бит).

       Returns:
           float: P-значение теста. Если p-value ≥ 0.01, последовательность считается случайной.

       Raises:
           ValueError: Если последовательность пуста, длина блока некорректна или обнаружены некорректные символы.
       """
    if len(binary_sequence) == 0:
        raise ValueError("Последовательность не может быть пустой")

    if block_size > len(binary_sequence):
        raise ValueError("Бинарная последовательность должна быть больше длины блока")

    if len(binary_sequence) % block_size != 0:
        raise ValueError("Длина блока должна быть кратна длине последовательности")

    # Предварительные проверки на неслучайность
    ones_count = binary_sequence.count('1')
    if ones_count <= 1:  # Менее 2 единиц → явно неслучайно
        return 0

    V_i = [0] * 4
    for i in range(0, len(binary_sequence), block_size):
        block = binary_sequence[i:i + block_size]
        max_len = 0
        cur_len = 0

        for bit in block:
            if bit not in {"0", "1"}:
                raise ValueError(f"Блок содержит посторонние символы: '{i}'")

            match bit:
                case "1":
                    cur_len += 1
                case "0":
                    cur_len = 0
            max_len = max(cur_len, max_len)

        match max_len:
            case _ if max_len <= 1:
                V_i[0] += 1
            case 2:
                V_i[1] += 1
            case 3:
                V_i[2] += 1
            case _:
                V_i[3] += 1

    hi_square = 0.0
    for i in range(len(V_i)):
        hi_square = sum(((V_i[i] - 16 * PI_i[i]) ** 2) / (16 * PI_i[i]) for i in range(len(V_i)))

    p_value = gammainc(3/2, hi_square/2)
    return p_value