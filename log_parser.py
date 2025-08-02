import json
import sys
import pathlib


class LogParser():
    """
    Класс для извлечения JSON объектов из файлов и их десериализации в
    python-объекты.
    """
    def __init__(self, upload_files: list[pathlib.Path]):
        self.files = self._check_files(upload_files)

    def get_data(self) -> list[dict]:
        all_data = []
        files_with_unexpected_data = []
        for file in self.files:
            with file.open() as f:
                try:
                    file_data = [json.loads(line) for line in f]
                    all_data.extend(file_data)
                except json.JSONDecodeError:
                    files_with_unexpected_data.append(str(file))
        if files_with_unexpected_data:
            print('These files contain unexpected data: '
                  f'{files_with_unexpected_data}. Please check the files: '
                  'each line in the log file must contain a single valid '
                  'JSON object.')
            sys.exit(1)
        if not all_data:
            print('There is not data in file(s). Please make sure the '
                  'file(s) is not empty.')
            sys.exit(1)
        return all_data

    def _check_files(self, upload_files: list[pathlib.Path]
                     ) -> list[pathlib.Path]:
        non_existent_files = []
        for file in upload_files:
            if not file.exists():
                non_existent_files.append(str(file))
        if non_existent_files:
            print(f'Files are not found: {non_existent_files}. '
                  'Please enter a correct path to file.')
            sys.exit(1)
        else:
            return upload_files
