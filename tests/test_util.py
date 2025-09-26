import unittest
from unittest.mock import MagicMock, patch

from src.utils import get_currency_rate  # Измените путь на правильный для вашего проекта


class TestGetCurrencyRate(unittest.TestCase):

    @patch("src.utils.request")  # Патчим метод request из модуля requests
    @patch("src.utils.load_dotenv")  # Патчим метод load_dotenv
    @patch("src.utils.os.getenv")  # Патчим os.getenv
    def test_get_currency_rate_success(self, mock_getenv, mock_load_dotenv, mock_request):
        """Тест успешного получения курса валюты"""
        mock_load_dotenv.return_value = None
        mock_getenv.return_value = "test_api_key"

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": 75.0}  # Пример успешного ответа

        mock_request.return_value = mock_response

        result = get_currency_rate("USD")

        self.assertEqual(result, {"result": 75.0})
        mock_request.assert_called_once()  # Проверяем, что запрос был выполнен один раз

    @patch("src.utils.request")  # Патчим метод request
    @patch("src.utils.load_dotenv")  # Патчим метод load_dotenv
    @patch("src.utils.os.getenv")  # Патчим os.getenv
    def test_get_currency_rate_failure(self, mock_getenv, mock_load_dotenv, mock_request):
        """Тест обработки ошибки при получении курса валюты"""
        mock_load_dotenv.return_value = None
        mock_getenv.return_value = "test_api_key"

        mock_response = MagicMock()
        mock_response.status_code = 404  # Ошибка 404 для примера
        mock_response.content = b"Not Found"  # Содержимое ответа
        mock_request.return_value = mock_response

        result = get_currency_rate("USD")

        self.assertEqual(result, [])  # Ожидаем получить пустой список при ошибке
        mock_request.assert_called_once()  # Проверяем, что запрос был выполнен один раз


if __name__ == "__main__":
    unittest.main()
