import json_handler
from check import find_invalid_rows
from checksum import calculate_checksum


def main():
    df = json_handler.read_csv('20.csv')
    pattern = json_handler.read_json('pattern.json')

    indexes = find_invalid_rows(pattern, df)
    checksum = calculate_checksum(indexes)

    result = {'variant': 20, 'checksum': checksum}
    json_handler.save_result('result.json', result)

if __name__ == "__main__":
    main()