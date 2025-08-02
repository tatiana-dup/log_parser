import pytest
from unittest.mock import patch, MagicMock

import main
from report import AverageResponseTimeReport


def test_no_file_arg(monkeypatch, capsys):
    """
    Без аргумента --file не запускается работа, а выводится
    сообщение, что аргумент обязателен.
    """
    monkeypatch.setattr('sys.argv', ['main.py', '--report', 'average'])
    with pytest.raises(SystemExit) as e:
        main.main()

    cuptured = capsys.readouterr()
    assert e.value.code == 2
    assert 'the following arguments are required:' in cuptured.err
    assert '--file' in cuptured.err


def test_no_report_arg(monkeypatch, capsys, correct_log_file):
    """
    Без аргумента --report не запускается работа, а выводится
    сообщение, что аргумент обязателен.
    """
    monkeypatch.setattr('sys.argv',
                        ['main.py', '--file', str(correct_log_file)])
    with pytest.raises(SystemExit) as e:
        main.main()

    cuptured = capsys.readouterr()
    assert e.value.code == 2
    assert 'the following arguments are required:' in cuptured.err
    assert '--report' in cuptured.err


def test_no_param_for_file(monkeypatch, capsys):
    """
    Без параметров для аргумента --file не запускается работа, а выводится
    сообщение, что необходимо указать как минимум один параметр.
    """
    monkeypatch.setattr('sys.argv',
                        ['main.py', '--file', '--report', 'average'])
    with pytest.raises(SystemExit) as e:
        main.main()

    cuptured = capsys.readouterr()
    assert e.value.code == 2
    assert 'expected at least one argument' in cuptured.err
    assert '--file' in cuptured.err


def test_no_param_for_report(monkeypatch, capsys, correct_log_file):
    """
    Без параметра для аргумента --report не запускается работа, а выводится
    сообщение, что необходимо указать как один параметр.
    """
    monkeypatch.setattr('sys.argv',
                        ['main.py', '--file', str(correct_log_file),
                         '--report'])
    with pytest.raises(SystemExit) as e:
        main.main()

    cuptured = capsys.readouterr()
    assert e.value.code == 2
    assert 'expected one argument' in cuptured.err
    assert '--report' in cuptured.err


def test_several_param_for_report(monkeypatch, capsys, correct_log_file):
    """
    При попытке указать сразу несколько параметров для аргумента --report
    не запускается работа, а выводится сообщение, что это неопознанный
    аргумент.
    """
    extra_arg = 'users'
    monkeypatch.setattr('sys.argv',
                        ['main.py', '--file', str(correct_log_file),
                         '--report', 'average', extra_arg])
    with pytest.raises(SystemExit) as e:
        main.main()

    cuptured = capsys.readouterr()
    assert e.value.code == 2
    assert 'unrecognized arguments' in cuptured.err
    assert extra_arg in cuptured.err


def test_unexpected_param_for_report(monkeypatch, capsys, correct_log_file):
    """
    Если в качестве параметра аргументу --report передано название отчета,
    которого нет среди доступных отчетов, то работа скрипта не запускается,
    и выводится сообщение, что нужно выбрать название отчета из списка.
    """
    unexpected_param = 'users'
    choises_for_report = "'" + "', '".join(main.REPORTS.keys()) + "'"
    monkeypatch.setattr('sys.argv',
                        ['main.py', '--file', str(correct_log_file),
                         '--report', unexpected_param])
    with pytest.raises(SystemExit) as e:
        main.main()

    cuptured = capsys.readouterr()
    assert e.value.code == 2
    assert 'argument --report: invalid choice:' in cuptured.err
    assert f'choose from {choises_for_report}' in cuptured.err


def test_correct_use_average_report(monkeypatch, correct_log_file):
    """
    Проверяет, что при запросе отчета average через командную строку,
    будет запущена генерация нужного отчета.
    """
    monkeypatch.setattr('sys.argv',
                        ['main.py', '--file', str(correct_log_file),
                         '--report', 'average'])

    mock_instance = MagicMock()

    assert main.REPORTS.get('average') == AverageResponseTimeReport

    with patch.dict('main.REPORTS', {'average': lambda: mock_instance}):
        main.main()

    mock_instance.generate.assert_called_once()


def test_all_file_paths_passed_to_log_parser(monkeypatch,
                                             correct_data_1,
                                             correct_data_2,
                                             correct_log_file,
                                             correct_log_file2):
    """
    Проверяет, что при передачи нескольких путей к файлам, все указанные пути
    будут переданы в LogParser.
    """
    monkeypatch.setattr(
        'sys.argv',
        ['main.py', '--file', str(correct_log_file), str(correct_log_file2),
         '--report', 'average']
    )

    mock_parser_instance = MagicMock()
    mock_parser_instance.get_data.return_value = (correct_data_1
                                                  + correct_data_2)

    with patch('main.LogParser',
               return_value=mock_parser_instance) as mock_parser_class:
        main.main()

        mock_parser_class.assert_called_once()
        passed_args = mock_parser_class.call_args[0][0]

        assert isinstance(passed_args, list)
        assert correct_log_file in passed_args
        assert correct_log_file2 in passed_args
        assert len(passed_args) == 2

        mock_parser_instance.get_data.assert_called_once()
