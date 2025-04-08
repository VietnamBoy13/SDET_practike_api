import requests
from requests import Response


class BaseAPI:
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url
        self.headers = None
        self.user_id = None
        self.body = None
        self.token = None

    def request_get(self, endpoint: str, **kwargs) -> Response:
        """
        Выполняет GET-запрос.
        :param endpoint: Конечная точка API
        :param kwargs: дополнительные параметры запроса
        :return: Объект Response
        """
        url = f"{self.base_url}{endpoint}"
        return requests.get(url, headers=self.headers, **kwargs)

    def request_post(
        self,
        endpoint: str,
        data: dict = None,
        **kwargs
    ) -> Response:
        """
        Выполняет POST-запрос.
        :param endpoint: Конечная точка API
        :param data: данные для тела запроса
        :param kwargs: дополнительные параметры запроса
        :return: Объект Response
        """
        url = f"{self.base_url}{endpoint}"
        return requests.post(url, json=data, headers=self.headers, **kwargs)

    def request_delete(self, endpoint: str, **kwargs) -> Response:
        """
        Выполняет DELETE-запрос.
        :param endpoint: Конечная точка API
        :param kwargs: дополнительные параметры запроса
        :return: Объект Response
        """
        url = f"{self.base_url}{endpoint}"
        return requests.delete(url, headers=self.headers, **kwargs)

    def request_patch(
        self,
        endpoint: str,
        data: dict = None,
        **kwargs
    ) -> Response:
        """
        Выполняет PATCH-запрос.
        :param endpoint: Конечная точка API
        :param data: данные для обновления
        :param kwargs: дополнительные параметры запроса
        :return: Объект Response
        """
        url = f"{self.base_url}{endpoint}"
        return requests.patch(url, json=data, headers=self.headers, **kwargs)