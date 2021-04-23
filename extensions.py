import json
import requests
from config import exchanger, API_KEY


class ConverterException(Exception):  # чтобы выбрасывать не ValueError, а собственные ошибки
    pass

class Converter:
    @staticmethod
    def get_price(values):
        if len(values) != 3:
            raise ConverterException('Неверное количество параметров')
        quote, base, amount = values

        if quote == base:
            raise ConverterException(f'Невозможно перевести одинаковые валюты {base}')

        try:
            quote_ticker = exchanger[quote]
        except KeyError:
            raise ConverterException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = exchanger[base]
        except KeyError:
            raise ConverterException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConverterException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://free.currconv.com/api/v7/convert?q={quote_ticker}_{base_ticker}&compact=ultra&apiKey={API_KEY}')
        result = json.loads(r.content)
        for i in result.values():
            pass

        total = float(i) * amount

        return round(total, 3)
