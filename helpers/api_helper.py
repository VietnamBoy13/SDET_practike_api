from typing import Dict, Type

import allure
from pydantic import BaseModel, ValidationError

from api.base_request import BaseAPI
from api.data import CREATE_ENTITY_DATA, UPDATE_ENTITY_DATA


class CreateEntityResponse(BaseModel):
    id: int
    title: str
    verified: bool


class APIHelper:
    def __init__(self):
        self.request = BaseAPI()

    @staticmethod
    def _validate_status_code(response, expected_code: int, message: str) -> None:
        assert response.status_code == expected_code, (
            f"{message} | Ожидался код статуса {expected_code}, но получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

    @staticmethod
    def _validate_response_model(model_class: Type[BaseModel], data: Dict) -> BaseModel:
        try:
            return model_class.model_validate(data)
        except ValidationError as e:
            raise AssertionError(f"Ошибка валидации ответа для модели {model_class.__name__}: {e}")

    @allure.step("Создание новой сущности")
    def create_entity(self) -> BaseModel:
        response = self.request.request_post("/api/create", CREATE_ENTITY_DATA)
        self._validate_status_code(response, 200, "Не удалось создать сущность")

        entity_data = {
            "id": int(response.text),
            "title": CREATE_ENTITY_DATA["title"],
            "verified": CREATE_ENTITY_DATA["verified"]
        }
        return self._validate_response_model(CreateEntityResponse, entity_data)

    @allure.step("Получение сущности по ID")
    def get_entity(self, entity_id: int) -> BaseModel:
        response = self.request.request_get(f"/api/get/{entity_id}")
        self._validate_status_code(response, 200, "Не удалось получить сущность")
        return self._validate_response_model(CreateEntityResponse, response.json())

    @allure.step("Удаление сущности по ID")
    def delete_entity(self, entity_id: int) -> None:
        response = self.request.request_delete(f"/api/delete/{entity_id}")
        self._validate_status_code(response, 204, "Не удалось удалить сущность")

    @allure.step("Получение всех сущностей")
    def get_all_entities(self) -> list[BaseModel]:
        response = self.request.request_post("/api/getAll", {})
        self._validate_status_code(response, 200, "Не удалось получить все сущности")

        list_of_all_entities = response.json()
        entities = list_of_all_entities.get("entity", [])

        return [
            self._validate_response_model(CreateEntityResponse, entity)
            for entity in entities
        ]

    @allure.step("Обновление сущности по ID")
    def patch_entity(self, entity_id: int) -> BaseModel:
        response = self.request.request_patch(
            f"/api/patch/{entity_id}", UPDATE_ENTITY_DATA
        )
        self._validate_status_code(response, 204, "Не удалось обновить сущность")

        updated_data = {
            "id": entity_id,
            "title": UPDATE_ENTITY_DATA["title"],
            "verified": UPDATE_ENTITY_DATA["verified"]
        }
        return self._validate_response_model(CreateEntityResponse, updated_data)
