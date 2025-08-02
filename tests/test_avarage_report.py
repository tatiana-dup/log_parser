from report import AverageResponseTimeReport


def test_filter_valid_data(capsys):
    """
    Проверяет, что в полученных данных есть нужные ключи,
    если нет, то будет выведено, сколько строк пропущенно из-за этого.
    Ключ response_time является типом flaot, если нет, то будет выведено,
    сколько строк пропущенно из-за этого.
    """
    report = AverageResponseTimeReport()
    data = [
        {"url": "/api/a", "response_time": 0.3},
        {"url": "/api/b", "response_time": "fast"},
        {"url": "/api/c"},
        {"response_time": 1.2},
        {"url": "/api/d", "response_time": 0.5},
    ]

    valid = report._filter_valid_data(data)

    assert len(valid) == 2
    assert valid[0]['url'] == '/api/a'
    assert valid[1]['url'] == '/api/d'
    cuptured = capsys.readouterr()

    assert ('WARNING! Skipped 2 JSON objects: missing "url" or "response_time"'
            ) in cuptured.out
    assert ('WARNING! Skipped 1 JSON objects: "response_time" is not float'
            ) in cuptured.out


def test_no_valid_data(capsys):
    report = AverageResponseTimeReport()
    data = [
        {"url": "/api/b", "response_time": "fast"},
        {"url": "/api/c"},
        {"response_time": 1.2},
    ]

    report.generate(data)

    cuptured = capsys.readouterr()
    assert ('Valid data for report was not found.') in cuptured.out


def test_create_table_data():
    """
    В подготовленной таблице есть все url и верные данные
    (верная сумма и верное среднее).
    """
    report = AverageResponseTimeReport()
    valid_data = [
        {"url": "/api/a", "response_time": 0.2},
        {"url": "/api/a", "response_time": 0.4},
        {"url": "/api/b", "response_time": 1.0},
    ]

    table = report._create_table_data(valid_data)

    assert table == [
        ('/api/a', 2, 0.3),
        ('/api/b', 1, 1.0),
    ]


def test_get_headers():
    """
    Функция генерации заголовков возвращает нужные заголовки.
    """
    report = AverageResponseTimeReport()
    assert report._get_headers() == ['handler', 'total', 'avg_response_time']


def test_output_data(capsys):
    """
    В выводе есть заголовки, url и верные данные.
    """
    report = AverageResponseTimeReport()
    headers = ['handler', 'total', 'avg_response_time']
    data = [
        {"url": "/api/a", "response_time": 0.2},
        {"url": "/api/a", "response_time": 0.4},
        {"url": "/api/b", "response_time": 1.0},
    ]
    report.generate(data)

    cuptured = capsys.readouterr()
    assert headers[0] in cuptured.out
    assert '/api/a' in cuptured.out
    assert '0.3' in cuptured.out
