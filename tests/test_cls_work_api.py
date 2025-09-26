import unittest
from unittest.mock import patch, MagicMock
import requests
from src.cls_work_api import HeadHunterHAPI


class TestHeadHunterHAPI(unittest.TestCase):

    def setUp(self):
        """ Метод, который выполняется перед каждым тестом """
        self.hhh_api = HeadHunterHAPI()

    @patch('requests.get')
    def test_connect_to_api_success(self, mock_get):
        """ Тест успешного подключения к API """
        # Мокаем ответ от API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'items': []}
        mock_get.return_value = mock_response

        response = self.hhh_api._connect_to_api()
        self.assertIsNotNone(response)  # Проверяем, что ответ возвращен
        self.assertEqual(response.status_code, 200)  # Проверяем, что статус-код 200
        self.assertEqual(response.json()['items'], [])  # Проверяем, что возвращенный список пустой

    @patch('requests.get')
    def test_connect_to_api_failure(self, mock_get):
        """ Тест обработки ошибки при подключении к API """
        # Мокаем ошибку сети
        mock_get.side_effect = requests.exceptions.RequestException("Network error")

        response = self.hhh_api._connect_to_api()
        self.assertIsNone(response)  # Проверяем, что при ошибке возвращается None

    @patch('requests.get')
    def test_get_vacancies(self, mock_get):
        """ Тест получения вакансий """
        # Мокаем ответ от API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'items': [
                {
                    'id': '12345',
                    'name': 'Python Developer',
                    'area': {'name': 'Москва'},
                    'salary': {'from': 100000, 'to': 150000, 'currency': 'RUR'}
                }
            ]
        }
        mock_get.return_value = mock_response

        result = self.hhh_api.get_vacancies(key_word="Python")

        self.assertEqual(len(result), 1)  # Проверяем, что вернулся один элемент
        self.assertEqual(result[0]['name'], 'Python Developer')  # Проверяем корректность данных
        self.assertEqual(result[0]['salr_from'], 100000)  # Проверяем зарплату

    @patch('requests.get')
    def test_get_vacancies_empty(self, mock_get):
        """ Тест получения вакансий при пустом ответе """
        # Мокаем ответ от API с пустым списком вакансий
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'items': []}
        mock_get.return_value = mock_response

        result = self.hhh_api.get_vacancies(key_word="Python")

        self.assertEqual(len(result), 0)  # Проверяем, что нет полученных вакансий


if __name__ == '__main__':
    unittest.main()