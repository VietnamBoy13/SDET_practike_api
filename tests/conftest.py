import pytest
from api.data import CREATE_ENTITY_DATA
from helpers.api_helper import APIHelper


@pytest.fixture(scope="function")
def api():
    """Фикстура для инициализации API хелпера"""
    return APIHelper()


@pytest.fixture(scope="function")
def created_entity(api):
    """
    Фикстура для создания сущности перед тестом и её удаления после.
    Возвращает полную сущность.
    """
    entity = api.create_entity(CREATE_ENTITY_DATA)
    yield entity
    api.delete_entity(entity.id)


@pytest.fixture(scope="function")
def created_entity_id(created_entity):
    """
    Фикстура для получения только ID созданной сущности.
    """
    return created_entity.id

