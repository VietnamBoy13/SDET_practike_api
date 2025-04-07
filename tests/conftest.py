import pytest
from api.data import CREATE_ENTITY_DATA
from helpers.api_helper import APIHelper


@pytest.fixture(scope="function")
def api():
    return APIHelper()


@pytest.fixture()
def created_entity_id(api):
    entity = api.create_entity(CREATE_ENTITY_DATA)
    yield entity.id
