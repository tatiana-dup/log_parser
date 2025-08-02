import argparse
import pathlib

from log_parser import LogParser
from report import AverageResponseTimeReport


REPORTS = {
    'average': AverageResponseTimeReport,
}


def main():
    input_parser = argparse.ArgumentParser(description='Log report generator.')

    input_parser.add_argument('--file', type=pathlib.Path, required=True,
                              action='extend', nargs='+', dest='files',
                              help='Enter the name of file(s) with JSON-data.')
    input_parser.add_argument('--report', choices=REPORTS.keys(),
                              required=True,
                              help='Enter the name of report from list.')

    input_args = input_parser.parse_args()

    log_data = LogParser(input_args.files).get_data()
    report_class = REPORTS[input_args.report]
    report = report_class()
    report.generate(log_data)


if __name__ == '__main__':
    main()
