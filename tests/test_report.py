import os

from main import _MedianCoffee, ReportRow, CSVReader


CSV_FILE = os.path.join(os.getcwd(), 'example_files/math.csv')


class TestMedianCoffeeReport:
    def setup_method(self, method):
        self.fd = open(CSV_FILE, mode='r', encoding='utf-8')
        self.csv_file = CSVReader(self.fd)

        self.median_coffee = _MedianCoffee(csv_files=[self.csv_file,])
        self.fd.close()

    def test_calc_func(self):
        ReportRow('test', '1')
        ReportRow('test', '2')
        report_row = ReportRow('test', '3')
        output = self.median_coffee.calc_func(report_row)

        assert output == 2.0


class TestReportRow:
    def test_unique(self):
        r1 = ReportRow('test_1', 1)
        r2 = ReportRow('test_1', 2)
        r3 = ReportRow('test_2', 3)

        assert r1 is r2
        assert r2 is not r3
