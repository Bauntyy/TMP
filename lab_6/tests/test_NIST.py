import pytest
from NIST_test import frequency_test, same_bits_test, longest_sequence_test


class TestFrequencyTest:
    """Тесты для frequency_test"""

    def test_frequency_test_valid_sequence(self):
        """Тест с валидной последовательностью"""
        # Случайная последовательность
        sequence = "1010101010101010" * 10  # 160 бит
        result = frequency_test(sequence)

        assert isinstance(result, float)
        assert 0 <= result <= 1

    def test_frequency_test_all_ones(self):
        """Тест с последовательностью из всех единиц"""
        sequence = "1" * 100
        result = frequency_test(sequence)
        # p-value должен быть очень маленьким
        assert result < 0.01

    def test_frequency_test_empty_sequence(self):
        """Тест с пустой последовательностью"""
        with pytest.raises(ValueError) as exc_info:
            frequency_test("")
        assert "не может быть пустой" in str(exc_info.value)


class TestSameBitsTest:
    """Тесты для same_bits_test"""

    def test_same_bits_test_valid_sequence(self):
        """Тест с валидной последовательностью"""
        sequence = "0101010101010101"
        result = same_bits_test(sequence)

        assert isinstance(result, float)
        assert 0 <= result <= 1

    def test_same_bits_test_all_same(self):
        """Тест с одинаковыми битами"""
        sequence = "1" * 100
        result = same_bits_test(sequence)
        # Для всех одинаковых битов p-value должен быть 0
        assert result == 0.0

    def test_same_bits_test_empty_sequence(self):
        """Тест с пустой последовательностью"""
        with pytest.raises(ValueError) as exc_info:
            same_bits_test("")
        assert "не может быть пустой" in str(exc_info.value)


class TestLongestSequenceTest:
    """Тесты для longest_sequence_test"""

    @pytest.fixture
    def sample_pi_i(self):
        """Фикстура с тестовыми значениями PI_I"""
        return [0.2148, 0.3672, 0.2305, 0.1875]

    def test_longest_sequence_test_valid(self, sample_pi_i):
        """Тест с валидной последовательностью"""
        # Создаем последовательность, кратную 8
        sequence = "10101010" * 16  # 128 бит = 16 блоков по 8
        result = longest_sequence_test(sequence, sample_pi_i, block_size=8)

        assert isinstance(result, float)
        assert 0 <= result <= 1

    def test_longest_sequence_test_empty(self, sample_pi_i):
        """Тест с пустой последовательностью"""
        with pytest.raises(ValueError) as exc_info:
            longest_sequence_test("", sample_pi_i)
        assert "не может быть пустой" in str(exc_info.value)

    def test_longest_sequence_test_sequence_too_short(self, sample_pi_i):
        """Тест когда последовательность короче размера блока"""
        sequence = "101"
        with pytest.raises(ValueError) as exc_info:
            longest_sequence_test(sequence, sample_pi_i, block_size=8)
        assert "должна быть больше длины блока" in str(exc_info.value)

    def test_longest_sequence_test_not_multiple_of_block_size(self, sample_pi_i):
        """Тест когда длина не кратна размеру блока"""
        sequence = "10101010" * 2 + "101"  # 19 бит, не кратно 8
        with pytest.raises(ValueError) as exc_info:
            longest_sequence_test(sequence, sample_pi_i, block_size=8)
        assert "должна быть кратна" in str(exc_info.value)

    def test_longest_sequence_test_invalid_chars(self, sample_pi_i):
        """Тест с некорректными символами"""
        sequence = "1010abcd" * 4
        with pytest.raises(ValueError) as exc_info:
            longest_sequence_test(sequence, sample_pi_i, block_size=8)
        assert "содержит посторонние символы" in str(exc_info.value)

    def test_longest_sequence_test_few_ones(self, sample_pi_i):
        """Тест с очень малым количеством единиц"""
        sequence = "00000001" * 4
        result = longest_sequence_test(sequence, sample_pi_i, block_size=8)
        assert isinstance(result, float)


# Дополнительные интеграционные тесты
def test_integration_all_tests():
    """Интеграционный тест всех NIST тестов"""
    sequence = "1100110001" * 10  # 100 бит
    pi_i = [0.2148, 0.3672, 0.2305, 0.1875]

    # Для longest_sequence_test нужна последовательность, кратная 8
    sequence = sequence[:96]

    freq_result = frequency_test(sequence)
    same_result = same_bits_test(sequence)
    longest_result = longest_sequence_test(sequence, pi_i, block_size=8)

    # Все результаты должны быть float в диапазоне [0, 1]
    assert all(isinstance(x, float) for x in [freq_result, same_result, longest_result])
    assert all(0 <= x <= 1 for x in [freq_result, same_result, longest_result])