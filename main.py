import csv
from dataclasses import dataclass
from email.policy import default
import json
import click
# from make_dict_config import Record, record_to_json
from make_dict_config_sample import Record, record_to_json

def read_csv(file_path: str):
    with open(file_path, encoding='utf-8') as f:
        reader = csv.reader(f)
        return [row for row in reader]


@dataclass
class CsvRowsToDics:
    rows: list

    def __convert_liststring_to_list(self, elm):
        if elm and type(elm) == str and elm.startswith("['"):
            elm = [elm.replace('"', '').replace('[', '').replace(
                ']', '').replace("'", '') for elm in elm.split(",")]
        if elm and type(elm) == str and elm.startswith("[]"):
            elm = list()
        return elm

    def __convert_normal_list(self, row: list):
        new_row = list()
        for elm in row:
            elm = self.__convert_liststring_to_list(elm)
            new_row.append(elm)
        return new_row

    def invoke(self):
        dics = list()
        for row in self.rows:
            new_row = self.__convert_normal_list(row)
            rec = Record(*new_row)
            dic = record_to_json(rec)
            dics.append(dic)
        return dics


def convert_dict_to_be_breakline_splitted_str(dics):
    result = [json.dumps(rec, ensure_ascii=False) for rec in dics]
    result = '\n'.join(result)
    return result

def write_dict_to_json(path, dict):
    with open(path, "w", encoding='utf-8') as f:
        f.write(dict)


@click.command()
@click.option('--filename_input', default='sample.csv')
@click.option('--filename_output', default='sample.json')
def main(filename_input, filename_output):
    csv_rows = read_csv(f'data/{filename_input}')
    convertor = CsvRowsToDics(csv_rows)
    dics = convertor.invoke()
    json_breakline_splitted = convert_dict_to_be_breakline_splitted_str(dics)
    write_dict_to_json(f'data/{filename_output}', json_breakline_splitted)


if __name__ == '__main__':
    main()
