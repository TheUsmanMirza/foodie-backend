import pytest
from unittest.mock import patch, MagicMock
from ai_assistants.restaurant_reviews import RestaurantAssistant
from fastapi.testclient import TestClient
from app import app
from tests.mocks import DummyUser, DUMMY_RESPONSE, mock_restaurant_services, NoRestaurantUser, InvalidRestaurantUser

client = TestClient(app)

@patch('ai_assistants.restaurant_reviews.AgentExecutor')
@patch('ai_assistants.restaurant_reviews.OpenAIFunctionsAgent')
@patch('ai_assistants.restaurant_reviews.Pinecone')
@patch('ai_assistants.restaurant_reviews.HuggingFaceEmbeddings')
@patch('ai_assistants.restaurant_reviews.PineconeVectorStore')
@patch('ai_assistants.restaurant_reviews.ChatOpenAI')
def test_restaurant_assistant_init(mock_chat, mock_vectorstore, mock_embed, mock_pinecone, mock_agent, mock_executor, mock_restaurant_services):
    mock_chat.return_value = MagicMock()
    mock_vectorstore.return_value = MagicMock()
    mock_embed.return_value = MagicMock()
    mock_pinecone.return_value = MagicMock()
    mock_agent.from_agent_and_tools.return_value = MagicMock()
    mock_executor.from_agent_and_tools.return_value = MagicMock()
    assistant = RestaurantAssistant(restaurant_id='test_id')
    assert assistant.restaurant_context == 'Test context'
    assert assistant.agent is not None

def test_get_all_restaurants_name(monkeypatch):
    from restaurants import services
    monkeypatch.setattr(services, 'get_restaurant_name', lambda: ['Test Restaurant'])
    response = client.get('/get_all_restaurants_name')
    assert response.status_code == 200
    assert 'Test Restaurant' in response.json()

def test_get_restaurant_data(monkeypatch):
    from restaurants import services
    from users import utils
    monkeypatch.setattr(services, 'get_restaurant', lambda x: DUMMY_RESPONSE)
    app.dependency_overrides[utils.get_current_user] = lambda: DummyUser()
    response = client.get('/get_restaurant_data', headers={"Authorization": "Bearer testtoken"})
    assert response.status_code == 200
    assert response.json()['restaurant_name'] == 'Test Restaurant'
    app.dependency_overrides = {}  # Clean up

def test_get_restaurant_data_not_found(monkeypatch):
    from restaurants import services
    from users import utils
    def raise_404(_):
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Restaurant not found.")
    monkeypatch.setattr(services, 'get_restaurant', raise_404)
    app.dependency_overrides[utils.get_current_user] = lambda: DummyUser()
    response = client.get('/get_restaurant_data', headers={"Authorization": "Bearer testtoken"})
    assert response.status_code == 404
    assert response.json()['detail'] == 'Restaurant not found.'
    app.dependency_overrides = {}

def test_get_restaurant_data_internal_error(monkeypatch):
    from restaurants import services
    from users import utils
    def raise_500(_):
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail="Failed to fetch restaurant data.")
    monkeypatch.setattr(services, 'get_restaurant', raise_500)
    app.dependency_overrides[utils.get_current_user] = lambda: DummyUser()
    response = client.get('/get_restaurant_data', headers={"Authorization": "Bearer testtoken"})
    assert response.status_code == 500
    assert response.json()['detail'] == 'Failed to fetch restaurant data.'
    app.dependency_overrides = {}

def test_get_restaurant_data_unauthorized():
    response = client.get('/get_restaurant_data')
    assert response.status_code == 403 

def test_get_restaurant_data_user_without_restaurant_id(monkeypatch):
    from users import utils
    app.dependency_overrides[utils.get_current_user] = lambda: NoRestaurantUser()
    response = client.get('/get_restaurant_data', headers={"Authorization": "Bearer testtoken"})
    assert response.status_code == 400
    app.dependency_overrides = {}

def test_get_restaurant_data_invalid_restaurant_id_format(monkeypatch):
    from users import utils
    app.dependency_overrides[utils.get_current_user] = lambda: InvalidRestaurantUser()
    response = client.get('/get_restaurant_data', headers={"Authorization": "Bearer testtoken"})
    assert response.status_code == 422
    app.dependency_overrides = {} 