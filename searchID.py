import json
import random
import pytest

class SearchAPI:
    def __init__(self, json_response):
        self.json_response = json_response

    def search_id(self):
        try:
            data = json.loads(self.json_response)
        except json.JSONDecodeError:
            pytest.fail("SearchAPI: Не удалось распарсить JSON")
            return None

        brands = data.get('brands', None)
        if brands is None:
            pytest.fail("SearchAPI: В ответе отсутствует ключ 'brands'")
            return None

        if not isinstance(brands, list):
            pytest.fail("SearchAPI: 'brands' не является списком")
            return None

        if not brands:
            pytest.fail("SearchAPI: Список 'brands' пуст")
            return None

        random_brand = random.choice(brands)

        # Возвращаем список брендов без выбранного случайного бренда
        updated_brands = [brand for brand in brands if brand.get('id') != random_brand.get('id')]

        # Можно вернуть и выбранный бренд, если нужно
        return {
            "selected_brand": random_brand,
            "updated_brands": updated_brands
        }
