import pytest

# Dummy user for authentication
class DummyUser:
    restaurant_id = 'test_id'
    is_deleted = False

# Dummy response for restaurant data
DUMMY_RESPONSE = {
    'restaurant_id': 'test_id',
    'restaurant_name': 'Test Restaurant',
    'cuisine': 'Italian',
    'overall_rating': 4.5,
    'total_review_counts': 10,
    'five_stars': 5,
    'four_stars': 3,
    'three_stars': 2,
    'two_stars': 0,
    'one_stars': 0
}

class NoRestaurantUser:
    restaurant_id = None
    is_deleted = False

class InvalidRestaurantUser:
    restaurant_id = 'not-a-uuid'
    is_deleted = False

@pytest.fixture
def mock_restaurant_services(monkeypatch):
    monkeypatch.setattr('ai_assistants.restaurant_reviews.services.fetch_restaurant_context', lambda x: 'Test context') 