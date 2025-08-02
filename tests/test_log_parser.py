import pytest
from pathlib import Path

from log_parser import LogParser


def test_nonexistent_log_file(correct_log_file, capsys):
    """
    Если по указанному пути (путям) не существует файла, то прекращаем работу
    и выводим юзеру сообщение об этом.
    """
    name_nonexistent_file = 'file_does_not_exists.log'

    nonexistent_file = Path(name_nonexistent_file)

    with pytest.raises(SystemExit) as e:
        LogParser([correct_log_file, nonexistent_file])

    assert e.value.code == 1

    captured = capsys.readouterr()
    assert 'Files are not found' in captured.out
    assert name_nonexistent_file in captured.out
    assert correct_log_file.name not in captured.out


def test_empty_log_file(empty_log_file, capsys):
    """
    Если файл пустой, то прекращаем работу и выводим юзеру сообщение об этом.
    """
    with pytest.raises(SystemExit) as e:
        LogParser([empty_log_file]).get_data()

    assert e.value.code == 1

    captured = capsys.readouterr()
    assert 'There is not data in file' in captured.out


def test_not_json_data_log_file(not_json_data_log_file,
                                correct_log_file,
                                capsys):
    """
    Если хоть в одном файле есть некорректные данные (не JSON),
    то прекращаем работу и выводим юзеру сообщение об этом.
    """
    with pytest.raises(SystemExit) as e:
        LogParser([not_json_data_log_file, correct_log_file]).get_data()

    assert e.value.code == 1

    captured = capsys.readouterr()
    assert 'These files contain unexpected data' in captured.out
    assert not_json_data_log_file.name in captured.out
    assert correct_log_file.name not in captured.out


def test_log_parser_returns_list_of_dict(correct_log_file):
    """
    Парсер возвращает один список словарей.
    """
    data = LogParser([correct_log_file]).get_data()

    assert isinstance(data, list)
    assert isinstance(data[0], dict)


def test_all_data_contains_data_from_several_files(
        correct_data_1,
        correct_data_2,
        correct_log_file,
        correct_log_file2):
    """
    Если файлов было передано несколько, то данные из всех этих файлов
    есть в возвращаемом списке.
    """
    all_data = LogParser([correct_log_file, correct_log_file2]
                         ).get_data()
    assert correct_data_1[0] in all_data
    assert correct_data_2[0] in all_data
