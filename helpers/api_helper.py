from typing import Dict, List

import allure
import time  # Для использования time.sleep()
from pydantic import BaseModel

from api.base_request import BaseAPI
from api.data import CREATE_ENTITY_DATA, UPDATE_ENTITY_DATA


class CreateEntityResponse(BaseModel):
    id: int
    title: str
    verified: bool


class APIHelper:
    def __init__(self):
        self.request = BaseAPI()

    @allure.step("Создание новой сущности")
    def create_entity(self, data: Dict) -> CreateEntityResponse:
        response = self.request.request_post("/api/create", data)
        assert response.status_code == 200, \
            f"Failed to create entity: {response.text}"
        return CreateEntityResponse(
            id=int(response.text),
            title=CREATE_ENTITY_DATA["title"],
            verified=CREATE_ENTITY_DATA["verified"],
        )

    @allure.step("Получение сущности по ID")
    def get_entity(self, entity_id: int) -> CreateEntityResponse:
        response = self.request.request_get(f"/api/get/{entity_id}")
        assert response.status_code == 200, \
            f"Failed to get entity: {response.text}"
        return CreateEntityResponse(
            id=entity_id,
            title=CREATE_ENTITY_DATA["title"],
            verified=CREATE_ENTITY_DATA["verified"],
        )

    @allure.step("Удаление сущности по ID")
    def delete_entity(self, entity_id: int) -> bool:
        # Задержка для того, чтобы сервер успел сохранить данные (если это необходимо)
        time.sleep(3)
        # Проверка, что сущность существует перед удалением
        try:
            entity = self.get_entity(entity_id)
        except AssertionError:
            raise AssertionError(f"Entity with ID {entity_id} not found before delete")

        # Выполнение удаления сущности
        response = self.request.request_delete(f"/api/delete/{entity_id}")

        # Проверка успешного удаления
        assert response.status_code == 204, \
            f"Failed to delete entity. Status code: {response.status_code}, Response: {response.text}"

        return True

    @allure.step("Получение всех сущностей")
    def get_all_entities(self) -> List[CreateEntityResponse]:
        response = self.request.request_post("/api/getAll", {})
        assert response.status_code == 200, \
            f"Failed to create entity: {response.text}"
        list_of_all_entities = response.json()
        entities = list_of_all_entities.get("entity", [])
        return [CreateEntityResponse(**entity) for entity in entities]

    @allure.step("Обновление сущности по ID")
    def patch_entity(
        self,
        entity_id: int,
        update_data: Dict
    ) -> CreateEntityResponse:
        response = self.request.request_patch(
            f"/api/patch/{entity_id}", update_data
        )
        assert response.status_code == 204, \
            f"Failed to update entity:{response.json()}"
        return CreateEntityResponse(
            id=entity_id,
            title=UPDATE_ENTITY_DATA["title"],
            verified=UPDATE_ENTITY_DATA["verified"],
        )
