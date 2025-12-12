import pytest
import json
import os
import tempfile
from unittest.mock import patch, mock_open
from functions import read_json, read_sequence, run_tests, write_results


class TestReadJson:
    """Тесты для функции read_json"""

    def test_read_json_success(self):
        test_data = {
            "cpp_sequence": "test_path.txt",
            "java_sequence": "test_path2.txt",
            "result_path": "result.txt",
            "PI_I": [0.1, 0.2, 0.3, 0.4]
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_data, f)
            temp_path = f.name

        try:
            with patch('functions.__file__', temp_path):
                data, pi_constants = read_json(os.path.basename(temp_path))

                assert data == test_data
                assert pi_constants == [0.1, 0.2, 0.3, 0.4]
        finally:
            os.unlink(temp_path)

    def test_read_json_file_not_found(self, capsys):
        """Тест обработки отсутствующего файла"""
        data, pi_constants = read_json("non_existent.json")

        assert data == {}
        assert pi_constants == []

        captured = capsys.readouterr()
        assert "не найден" in captured.out

    def test_read_json_invalid_json(self, capsys):
        """Тест обработки некорректного JSON"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("{ invalid json }")
            temp_path = f.name

        try:
            with patch('functions.__file__', temp_path):
                data, pi_constants = read_json(os.path.basename(temp_path))

                assert data == {}
                assert pi_constants == []

                captured = capsys.readouterr()
                assert "не в формате JSON" in captured.out
        finally:
            os.unlink(temp_path)


class TestReadSequence:
    """Тесты для функции read_sequence"""

    def test_read_sequence_success(self):
        """Тест успешного чтения последовательности"""
        test_content = "1010 1100\n1111 0000"
        expected = "1010110011110000"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(test_content)
            temp_path = f.name

        try:
            result = read_sequence(temp_path)
            assert result == expected
        finally:
            os.unlink(temp_path)

    def test_read_sequence_file_not_found(self):
        """Тест обработки отсутствующего файла"""
        with pytest.raises(FileNotFoundError) as exc_info:
            read_sequence("non_existent.txt")
        assert "не найден" in str(exc_info.value)


class TestRunTests:
    """Тесты для функции run_tests"""

    def test_run_tests_with_mock(self):
        test_sequence = "1010101010101010"
        test_pi = [0.1, 0.2, 0.3, 0.4]

        with patch('functions.frequency_test') as mock_freq, \
                patch('functions.same_bits_test') as mock_same, \
                patch('functions.longest_sequence_test') as mock_longest:
            mock_freq.return_value = 0.12345
            mock_same.return_value = 0.54321
            mock_longest.return_value = 0.98765

            results = run_tests(test_sequence, test_pi)

            assert len(results) == 3
            assert "Result of frequency bit test: 0.12345" in results[0]
            assert "Result of run same bit test: 0.54321" in results[1]
            assert "Result of longest ones sequence test: 0.98765" in results[2]

            mock_freq.assert_called_once_with(test_sequence)
            mock_same.assert_called_once_with(test_sequence)
            mock_longest.assert_called_once_with(test_sequence, test_pi)


class TestWriteResults:
    """Тесты для функции write_results"""

    def test_write_results_success(self):
        """Тест успешной записи результатов"""
        cpp_results = [
            "Result of frequency bit test: 0.123",
            "Result of run same bit test: 0.456"
        ]
        java_results = [
            "Result of frequency bit test: 0.789",
            "Result of run same bit test: 0.999"
        ]

        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            temp_path = f.name

        try:
            write_results(temp_path, cpp_results, java_results)

            with open(temp_path, 'r') as f:
                content = f.read()

            assert "C++ results:" in content
            assert "JAVA results:" in content
            assert "0.123" in content
            assert "0.999" in content
        finally:
            os.unlink(temp_path)

    def test_write_results_io_error(self):
        """Тест обработки ошибки записи"""
        invalid_path = "/nonexistent/folder/file.txt"

        with pytest.raises(Exception) as exc_info:
            write_results(invalid_path, [], [])
        assert "Error while writing to file" in str(exc_info.value)