'''
Отчет о потреблении кофе

Что нужно сделать?
Нужно написать скрипт для обработки csv-файла.
Скрипт читает файлы с данными о подготовке студентов к экзаменам (см. примеры ниже) и формирует отчеты. Нужно сформировать один отчет в котором будет медианная сумма трат на кофе по каждому студенту за весь период сессии. Отчёт включает в себя список студентов и медиану трат (по колонке coffee spent), отчёт сортируются по убыванию трат. Название файлов (может быть несколько) и название отчета передается в виде параметров --files и --report (в нашем случае это median-coffee). Отчёт формируется по всем переданных файлам, а не по каждому отдельно.
Чтобы сфокусироваться на функционале формирования отчёта и не отвлекаться на рутинные задачи (обработку параметров скрипта, чтения файлов и вывод), можно использовать стандартную библиотеку argparse и csv, для расчета медианы statistics, а для отображения в консоли tabulate.

Примеры файлов можно посмотреть здесь, выглядят так:
student,date,coffee_spent,sleep_hours,study_hours,mood,exam
Алексей Смирнов,2024-06-01,450,4.5,12,норм,Математика
Алексей Смирнов,2024-06-02,500,4.0,14,устал,Математика
Алексей Смирнов,2024-06-03,550,3.5,16,зомби,Математика
Дарья Петрова,2024-06-01,200,7.0,6,отл,Математика
Дарья Петрова,2024-06-02,250,6.5,8,норм,Математика
Дарья Петрова,2024-06-03,300,6.0,9,норм,Математика
Иван Кузнецов,2024-06-01,600,3.0,15,зомби,Математика
Иван Кузнецов,2024-06-02,650,2.5,17,зомби,Математика
Иван Кузнецов,2024-06-03,700,2.0,18,не выжил,Математика
Мария Соколова,2024-06-01,100,8.0,3,отл,Математика
Мария Соколова,2024-06-02,120,8.5,2,отл,Математика
Мария Соколова,2024-06-03,150,7.5,4,отл,Математика
Павел Новиков,2024-06-01,380,5.0,10,норм,Математика
Павел Новиков,2024-06-02,420,4.5,11,устал,Математика
Павел Новиков,2024-06-03,470,4.0,13,устал,Математика
Елена Волкова,2024-06-01,280,6.0,8,норм,Математика
Елена Волкова,2024-06-02,310,5.5,9,норм,Математика
Елена Волкова,2024-06-03,340,5.0,10,устал,Математика
 
Какие функциональные требования?
●   можно передать пути к файлам через --files
●   можно указать название отчета через --report (median-coffee)
●   в консоль (не в файл) выводится отчёт в виде таблицы
Какие не функциональные требования?
●   для всего кроме тестов и вывода в консоль, можно использовать только стандартную библиотеку, например:
○   для обработки параметров скрипта нельзя использовать click, можно argparse
○   для чтения файлов нельзя использовать pandas, но можно csv
●   в архитектуру заложена возможность добавления новых отчётов, как раз через параметр --report, в дальнейшем нужно будет добавлять отчёты с другой логикой расчетов, поэтому их добавление должно быть удобным.
●   код покрыт тестами написанными на pytest
●   для тестов можно использовать любые дополнительные библиотеки
●   код соответствует:
○   общепринятым стандартам написания проектов на python
○   общепринятому стилю
Как сдавать задание?
●   присылайте ссылку на git репозиторий, ссылки на google drive или yandex не подходят
●   присылайте примеры запуска скрипта, например:
○   можно сделать скриншот запуска скрипта и добавить его репозиторий, для примера работы можно использовать эти файлы. За приложенные примеры запуска ревьюер скажет вам спасибо и добавит баллы.
●   перед отправкой ссылки на репозиторий проверьте, пожалуйста, что репозиторий публичный и его можно посмотреть
'''
# -*- coding: utf-8 -*-

import os
import csv
import argparse
import statistics
from _io import TextIOWrapper
from typing import Any, Set, List, Generator, Optional

from tabulate import tabulate


VALID_EXTENSION = '.csv'


class CSVReader:
    def __init__(self, csv_file: TextIOWrapper):
        self._csv_file = csv_file

    def read_lines(self) -> Generator:
        rows = csv.DictReader(self._csv_file)
        for row in rows:
            yield row


def get_csv_readers(files: List[str]) -> List[CSVReader]:
    csv_files = []
    for csv_file_path in files:
        is_csv = csv_file_path.lower().endswith(VALID_EXTENSION)
        is_exists = os.path.exists(csv_file_path)
        if not is_csv or not is_exists:
            continue

        csv_file = open(csv_file_path, mode='r', encoding='utf-8')
        reader = CSVReader(csv_file)
        csv_files.append(reader)
    return csv_files


class ReportRow:
    instancies = {}

    def __new__(cls, identifier: str, value: Any):
        if identifier in ReportRow.instancies.keys():
            created_row = ReportRow.instancies[identifier]
            created_row.values.append(value)
            return created_row

        new_report_row = super().__new__(cls)
        new_report_row.identifier = identifier
        new_report_row.values = [value,]
        ReportRow.instancies[identifier] = new_report_row
        return new_report_row

    @property
    def value(self) -> Optional[Any]:
        if hasattr(self, '_value'):
            return self._value
        return None

    @value.setter
    def value(self, value: Any) -> None:
        self._value = value


class _BaseReport:
    def __init__(self, csv_files: List[CSVReader]):
        self._csv_files = csv_files
        self.all_rows = self._get_all_rows()

    def calculate(self, reverse: bool=True) -> List[ReportRow]:
        for row in self.all_rows:
            row.value = self.calc_func(row)
        return sorted(self.all_rows, key=lambda row: row.value, reverse=reverse)

    def table_report(self, reverse: bool=True) -> str:
        headers = (self.identifier_column_name, self.calc_column_name)
        data = map(lambda row: [row.identifier, row.value], self.calculate(reverse))
        table = tabulate(data,
                         headers=headers,
                         tablefmt='grid',
                         numalign='right',
                         floatfmt='.2f')
        return table

    def _get_all_rows(self) -> Set[ReportRow]:
        output = set()
        for csv_file in self._csv_files:
            for row in csv_file.read_lines():
                identifier = row.get(self.identifier_column_name)
                output.add(ReportRow(
                    identifier=identifier,
                    value=row[self.calc_column_name]
                ))
        return output


class _MedianCoffee(_BaseReport):
    title = 'median-coffee'
    identifier_column_name = 'student'
    calc_column_name = 'coffee_spent'

    def calc_func(self, row: ReportRow) -> float:
        values = map(float, row.values)
        median = statistics.median(values)
        return median


class _AverageSleepTime(_BaseReport):
    title = 'sleep-hours'
    identifier_column_name = 'student'
    calc_column_name = 'sleep_hours'

    def calc_func(self, row: ReportRow) -> float:
        values = map(float, row.values)
        mean = statistics.fmean(values)
        return mean


class Report:
    isinstancies = _BaseReport.__subclasses__()

    def __new__(cls, report_title: str, *args, **kwargs):
        instance = next(filter(
            lambda rep: rep.title==report_title,
            Report.isinstancies
        ))
        return instance(*args, **kwargs)


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-f',
                            '--files',
                            nargs='+',
                            required=True,
                            help='Waiting to receive a file, files, or directory with .csv files.',
                            metavar='FILE')
    report_help_text = 'Variables: ' + ', '.join([f'"{cls.title}"' for cls in Report.isinstancies])
    arg_parser.add_argument('-r',
                            '--report',
                            help=f'Waiting for report title to be received. {report_help_text}',
                            default='median-coffee')
    args = arg_parser.parse_args()
    csv_files = get_csv_readers(args.files)
    report_title = args.report

    report = Report(report_title, csv_files=csv_files)
    print(report.table_report())


if __name__ == '__main__':
    main()
