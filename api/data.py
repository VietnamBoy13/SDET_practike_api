from faker import Faker
import random

fake = Faker('ru_RU')

def generate_entity_data(is_update: bool = False) -> dict:
    title_prefix = "UPDATE_" if is_update else ""
    return {
        "addition": {
            "additional_info": fake.sentence(nb_words=3),
            "additional_number": random.randint(1, 1000)
        },
        "important_numbers": random.sample(range(10, 100), 3),
        "title": f"{title_prefix}SDET_API_TEST_{fake.unique.word()}",
        "verified": random.choice([True, False])
    }

CREATE_ENTITY_DATA = generate_entity_data()
UPDATE_ENTITY_DATA = generate_entity_data(is_update=True)
