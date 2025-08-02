import json
import pytest


@pytest.fixture(scope='session')
def correct_data_1():
    return [
        {"@timestamp": "2025-06-22T13:57:32+00:00", "status": 200, "url": "/api/a/...", "request_method": "GET", "response_time": 0.024, "http_user_agent": "..."},
        {"@timestamp": "2025-06-22T13:57:32+00:00", "status": 200, "url": "/api/a/...", "request_method": "GET", "response_time": 0.02, "http_user_agent": "..."}
    ]


@pytest.fixture(scope='session')
def correct_data_2():
    return [
        {"@timestamp": "2025-06-22T13:57:32+00:00", "status": 200, "url": "/api/b/...", "request_method": "GET", "response_time": 0.036, "http_user_agent": "..."},
        {"@timestamp": "2025-06-22T13:57:32+00:00", "status": 200, "url": "/api/b/...", "request_method": "GET", "response_time": 0.046, "http_user_agent": "..."}
    ]


@pytest.fixture()
def correct_log_file(tmp_path, correct_data_1):
    temp_file = tmp_path / 'correct_log_file.log'
    with temp_file.open('w') as f:
        for i in correct_data_1:
            json.dump(i, f)
            f.write('\n')
    return temp_file


@pytest.fixture()
def correct_log_file2(tmp_path, correct_data_2):
    temp_file = tmp_path / 'correct_log_file2.log'
    with temp_file.open('w') as f:
        for i in correct_data_2:
            json.dump(i, f)
            f.write('\n')
    return temp_file


@pytest.fixture()
def empty_log_file(tmp_path):
    temp_file = tmp_path / 'empty_log_file.log'
    temp_file.touch()
    return temp_file


@pytest.fixture()
def not_json_data_log_file(tmp_path):
    content = 'Текст'
    temp_file = tmp_path / 'not_json_data_log_file.log'
    temp_file.write_text(content)
    return temp_file
