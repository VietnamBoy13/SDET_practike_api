import allure
from api.data import CREATE_ENTITY_DATA, UPDATE_ENTITY_DATA


@allure.story("Создание новой сущности")
@allure.title("Проверка создания сущности через API")
@allure.tag("POST", "Создание")
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase("https://localhost:8080/api/create")
@allure.description(
    """
    Шаги:
    1. Отправить POST-запрос на создание сущности;
    2. Проверить, что код ответа - 200;
    3. Убедиться, что в ответе присутствует корректный ID, title и verified.
    """
)
def test_create_entity(self, api):
    created_entity = api.create_entity(CREATE_ENTITY_DATA)
    with allure.step("Проверяем, что ID - целое число"):
        assert isinstance(created_entity.id, int)
    with allure.step("Проверяем, что title - строка"):
        assert isinstance(created_entity.title, str)
    with allure.step("Проверяем, что verified - булево значение"):
        assert isinstance(created_entity.verified, bool)


@allure.story("Получение сущности по ID")
@allure.title("Проверка получения сущности")
@allure.tag("GET", "Получение")
@allure.severity(allure.severity_level.NORMAL)
@allure.testcase("https://localhost:8080/api/get/{id}")
@allure.description(
    """
    Шаги:
    1. Выполнить GET-запрос на получение сущности по ID;
    2. Проверить, что код ответа - 200;
    3. Убедиться, что данные соответствуют ожидаемым.
    """
)
def test_get_entity(self, api, created_entity_id):
    selected_entity = api.get_entity(created_entity_id)
    with allure.step("Проверяем совпадение ID"):
        assert selected_entity.id == created_entity_id
    with allure.step("Проверяем совпадение title"):
        assert selected_entity.title == CREATE_ENTITY_DATA["title"]
    with allure.step("Проверяем совпадение verified"):
        assert selected_entity.verified == CREATE_ENTITY_DATA["verified"]


@allure.story("Удаление сущности")
@allure.title("Проверка удаления сущности")
@allure.tag("DELETE", "Удаление")
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase("https://localhost:8080/api/delete/{id}")
@allure.description(
    """
    Шаги:
    1. Выполнить DELETE-запрос по ID сущности;
    2. Проверить, что код ответа - 204;
    3. Убедиться, что сущность удалена успешно.
    """
)
def test_delete_entity(self, api, created_entity_id):
    # Проверяем, что сущность существует перед удалением
    entity = api.get_entity(created_entity_id)
    assert entity.id == created_entity_id, "Entity not found before delete"

    # Удаляем сущность
    deletion_result = api.delete_entity(created_entity_id)

    # Проверяем, что сущность успешно удалена
    with allure.step("Проверяем успешное удаление"):
        assert deletion_result is True


@allure.story("Получение всех сущностей")
@allure.title("Проверка получения всех сущностей")
@allure.tag("GET", "Получение")
@allure.severity(allure.severity_level.MINOR)
@allure.testcase("https://localhost:8080/api/getAll")
@allure.description(
    """
    Шаги:
    1. Выполнить GET-запрос на получение всех сущностей;
    2. Проверить, что ответ содержит список сущностей;
    3. Проверить типы полей каждой сущности.
    """
)
def test_get_all_entities(self, api):
    # Получаем все сущности
    entities = api.get_all_entities()

    with allure.step("Проверяем, что список не пустой"):
        assert len(entities) > 0, "Не найдено ни одной сущности"

    # Выводим все сущности для отладки или отображения
    print(f"Total entities found: {len(entities)}")
    for entity in entities:
        # Печатаем информацию о каждой сущности
        print(f"Entity ID: {entity.id}, Title: {entity.title}, Verified: {entity.verified}")

        with allure.step(f"Проверяем типы полей для сущности ID {entity.id}"):
            assert isinstance(entity.id, int)
            assert isinstance(entity.title, str)
            assert isinstance(entity.verified, bool)


@allure.story("Обновление сущности")
@allure.title("Проверка обновления сущности")
@allure.tag("PATCH", "Обновление")
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase("https://localhost:8080/api/patch/{id}")
@allure.description(
    """
    Шаги:
    1. Отправить PATCH-запрос на обновление сущности;
    2. Проверить, что код ответа - 204;
    3. Проверить, что данные были обновлены корректно.
    """
)
def test_patch_entity(self, api, created_entity_id):
    updated_entity = api.patch_entity(created_entity_id, UPDATE_ENTITY_DATA)
    with allure.step("Проверяем ID сущности"):
        assert updated_entity.id == created_entity_id
    with allure.step("Проверяем обновлённый title"):
        assert updated_entity.title == UPDATE_ENTITY_DATA["title"]
    with allure.step("Проверяем обновлённый verified"):
        assert updated_entity.verified == UPDATE_ENTITY_DATA["verified"]
