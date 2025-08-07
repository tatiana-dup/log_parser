from abc import ABC, abstractmethod
from collections import Counter
from statistics import mean

from tabulate import tabulate


REPORTS: dict = {}


def register_report(key_name):
    """
    Декоратор регистрирует отчеты в списке доступных отчетов.
    """
    def decorator(cls):
        REPORTS[key_name] = cls
        return cls
    return decorator


class Report(ABC):
    """
    Абстрактный базовый класс для всех типов отчётов.

    Определяет общий метод generate(), который фильтрует данные,
    формирует таблицу и выводит её. Дочерние классы должны
    предоставить реализацию для фильтрации и формирования таблицы.
    """

    def generate(self, data: list[dict]) -> None:
        valid_data = self._filter_valid_data(data)
        if not valid_data:
            print('Valid data for report was not found.')
            return
        table = self._create_table_data(valid_data)
        headers = self._get_headers()
        print(tabulate(table, headers, showindex=True))

    @abstractmethod
    def _filter_valid_data(self, data: list[dict]) -> list[dict]:
        pass

    @abstractmethod
    def _create_table_data(self, data: list[dict]) -> list[tuple]:
        pass

    @abstractmethod
    def _get_headers(self) -> list[str]:
        pass


@register_report('average')
class AverageResponseTimeReport(Report):
    """
    Класс для формирования отчета со списком эндпоинтов, количеством запросов
    по каждому эндпоинту и средним временем ответа.

    Фильтрует только те записи, в которых есть ключи 'url' и 'response_time',
    и response_time является числом с плавающей точкой.
    """

    def _filter_valid_data(self, data: list[dict]
                           ) -> list[dict]:
        valid_data = []
        reasons: Counter = Counter()

        for item in data:
            if 'url' not in item or 'response_time' not in item:
                reasons['missing "url" or "response_time"'] += 1
                continue
            if not isinstance(item['response_time'], float):
                reasons['"response_time" is not float'] += 1
                continue
            valid_data.append(item)

        for reason, count in reasons.items():
            print(f'WARNING! Skipped {count} JSON objects: {reason}')

        return valid_data

    def _create_table_data(self, data: list[dict]) -> list[tuple]:
        summary: dict[str, list[float]] = {}
        for i in data:
            url = i['url']
            response_time = i['response_time']
            if url in summary:
                summary[url].append(response_time)
            else:
                summary[url] = [response_time]

        return ([(key, len(value), round(mean(value), 3))
                 for key, value in summary.items()])

    def _get_headers(self) -> list[str]:
        return ['handler', 'total', 'avg_response_time']
