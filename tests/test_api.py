import allure
import pytest

from api.data import CREATE_ENTITY_DATA, UPDATE_ENTITY_DATA


@pytest.fixture
def created_entity(api):
    entity = api.create_entity()
    yield entity
    api.delete_entity(entity.id)


@allure.story("Создание новой сущности")
@allure.title("Проверка создания сущности через API")
@allure.tag("POST", "Создание")
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase("https://localhost:8080/api/create")
@allure.description(
    """
    (комментарий: сценарий должен быть полноценным — создание, проверка через GET и в списке, удаление)

    Шаги:
    1. Создать сущность;
    2. Проверить ID, title и verified;
    3. Получить сущность по ID и сверить данные;
    4. Убедиться, что сущность есть в списке всех;
    """
)
def test_create_entity(api, created_entity):
    with allure.step("Проверяем корректность созданной сущности"):
        assert created_entity.title == CREATE_ENTITY_DATA["title"], (
            f"Ошибка: title сущности не совпадает с ожидаемым. "
            f"Ожидалось: {CREATE_ENTITY_DATA['title']}, получено: {created_entity.title}"
        )
        assert created_entity.verified == CREATE_ENTITY_DATA["verified"], (
            f"Ошибка: verified сущности не совпадает с ожидаемым. "
            f"Ожидалось: {CREATE_ENTITY_DATA['verified']}, получено: {created_entity.verified}"
        )

    with allure.step("Проверяем получение по ID"):
        received = api.get_entity(created_entity.id)
        assert received == created_entity, (
            f"Ошибка: данные сущности по ID не совпадают. "
            f"Ожидалось: {created_entity}, получено: {received}"
        )

    with allure.step("Проверяем, что сущность есть в общем списке"):
        all_entities = api.get_all_entities()
        ids = [e.id for e in all_entities]
        assert created_entity.id in ids, (
            f"Ошибка: сущность с ID {created_entity.id} не найдена в списке всех сущностей."
        )


@allure.story("Получение сущности по ID")
@allure.title("Проверка получения сущности")
@allure.tag("GET", "Получение")
@allure.severity(allure.severity_level.NORMAL)
@allure.testcase("https://localhost:8080/api/get/{id}")
@allure.description(
    """
    Шаги:
    1. Создать сущность;
    2. Получить её по ID;
    3. Сравнить поля с оригинальными;
    """
)
def test_get_entity(api, created_entity):
    with allure.step("Получаем сущность по ID"):
        entity = api.get_entity(created_entity.id)

    with allure.step("Проверяем данные сущности"):
        assert entity == created_entity, (
            f"Ошибка: данные сущности по ID не совпадают. "
            f"Ожидалось: {created_entity}, получено: {entity}"
        )


@allure.story("Удаление сущности")
@allure.title("Проверка удаления сущности")
@allure.tag("DELETE", "Удаление")
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase("https://localhost:8080/api/delete/{id}")
@allure.description(
    """
    Шаги:
    1. Создать сущность;
    2. Удалить сущность;
    3. Убедиться, что она отсутствует в getAll и по ID;
    """
)
def test_delete_entity(api):
    entity = api.create_entity()

    with allure.step("Удаляем сущность"):
        api.delete_entity(entity.id)

    with allure.step("Проверяем, что сущность отсутствует в getAll"):
        all_entities = api.get_all_entities()
        ids = [e.id for e in all_entities]
        assert entity.id not in ids, (
            f"Ошибка: сущность с ID {entity.id} всё ещё присутствует в списке всех сущностей."
        )

    with allure.step("Проверяем, что get по ID возвращает ошибку"):
        with pytest.raises(AssertionError):
            api.get_entity(entity.id)


@allure.story("Получение всех сущностей")
@allure.title("Проверка получения всех сущностей")
@allure.tag("GET", "Получение")
@allure.severity(allure.severity_level.MINOR)
@allure.testcase("https://localhost:8080/api/getAll")
@allure.description(
    """
    Шаги:
    1. Создать сущность;
    2. Получить список всех сущностей;
    3. Проверить, что созданная сущность в списке;
    """
)
def test_get_all_entities(api, created_entity):
    with allure.step("Получаем список всех сущностей"):
        all_entities = api.get_all_entities()

    with allure.step("Проверяем, что в списке есть созданная сущность"):
        ids = [e.id for e in all_entities]
        assert created_entity.id in ids, (
            f"Ошибка: сущность с ID {created_entity.id} не найдена в списке всех сущностей."
        )


@allure.story("Обновление сущности")
@allure.title("Проверка обновления сущности")
@allure.tag("PATCH", "Обновление")
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase("https://localhost:8080/api/patch/{id}")
@allure.description(
    """
    (комментарий: сценарий — создать → обновить → получить → проверить)

    Шаги:
    1. Создать сущность;
    2. Обновить данные;
    3. Получить сущность по ID;
    4. Сравнить обновленные данные;
    """
)
def test_patch_entity(api, created_entity):
    with allure.step("Обновляем сущность"):
        updated = api.patch_entity(created_entity.id)

    with allure.step("Проверяем обновлённые данные"):
        assert updated.id == created_entity.id, (
            f"Ошибка: ID сущности после обновления не совпадает с ожидаемым. "
            f"Ожидалось: {created_entity.id}, получено: {updated.id}"
        )
        assert updated.title == UPDATE_ENTITY_DATA["title"], (
            f"Ошибка: title сущности после обновления не совпадает с ожидаемым. "
            f"Ожидалось: {UPDATE_ENTITY_DATA['title']}, получено: {updated.title}"
        )
        assert updated.verified == UPDATE_ENTITY_DATA["verified"], (
            f"Ошибка: verified сущности после обновления не совпадает с ожидаемым. "
            f"Ожидалось: {UPDATE_ENTITY_DATA['verified']}, получено: {updated.verified}"
        )

    with allure.step("Проверяем через get, что обновление применилось"):
        fetched = api.get_entity(created_entity.id)
        assert fetched == updated, (
            f"Ошибка: данные сущности после обновления не совпадают с ожидаемыми. "
            f"Ожидалось: {updated}, получено: {fetched}"
        )
