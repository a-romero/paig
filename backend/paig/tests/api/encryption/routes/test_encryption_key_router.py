from unittest.mock import AsyncMock, patch

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from core.controllers.paginated_response import create_pageable_response
from api.encryption.api_schemas.encryption_key import EncryptionKeyView
from api.encryption.controllers.encryption_key_controller import EncryptionKeyController
from api.encryption.database.db_models.encryption_key_model import EncryptionKeyType, EncryptionKeyStatus

dummy_encryption_key_view = EncryptionKeyView(
    id=1,
    status=1,
    create_time="2021-01-01T00:00:00Z",
    update_time="2021-01-01T00:00:00Z",
    public_key="public_key",
    private_key="private_key",
    key_status=EncryptionKeyStatus.ACTIVE,
    key_type=EncryptionKeyType.MSG_PROTECT_SHIELD
)


@pytest.fixture()
def mock_encryption_key_controller():
    mock_encryption_key_controller = AsyncMock(spec=EncryptionKeyController)

    mock_encryption_key_controller.list_encryption_keys.return_value = create_pageable_response(
        content=[dummy_encryption_key_view],
        total_elements=1,
        page_number=1,
        size=10,
        sort=["id"]
    )

    mock_encryption_key_controller.create_encryption_key.return_value = dummy_encryption_key_view
    mock_encryption_key_controller.get_encryption_key_by_id.return_value = dummy_encryption_key_view
    mock_encryption_key_controller.get_public_encryption_key_by_id.return_value = dummy_encryption_key_view
    mock_encryption_key_controller.get_active_encryption_key_by_type.return_value = dummy_encryption_key_view
    mock_encryption_key_controller.disable_passive_encryption_key.return_value = dummy_encryption_key_view
    mock_encryption_key_controller.delete_disabled_encryption_key.return_value = dummy_encryption_key_view

    return mock_encryption_key_controller


def test_list_encryption_keys_success(mock_encryption_key_controller):
    def get_mock_controller():
        return mock_encryption_key_controller

    with patch("api.encryption.controllers.encryption_key_controller.EncryptionKeyController", get_mock_controller):
        from api.encryption.routes.encryption_key_router import encryption_key_router
        from server import app

        # Create client
        app.include_router(encryption_key_router, prefix="/keys")
        client = TestClient(app)

        response = client.get("http://localhost:9090/keys")
        assert response.status_code == status.HTTP_200_OK
        assert "content" in response.json()


def test_create_encryption_key_success(mock_encryption_key_controller):
    mock_encryption_key_controller.create_encryption_key.return_value = {
        "id": 1,
        "key_type": EncryptionKeyType.MSG_PROTECT_SHIELD,
        "status": EncryptionKeyStatus.ACTIVE,
        # add more fields as needed based on EncryptionKey schema
    }

    def get_mock_controller():
        return mock_encryption_key_controller

    with patch("api.encryption.controllers.encryption_key_controller.EncryptionKeyController", get_mock_controller):
        from api.encryption.routes.encryption_key_router import encryption_key_router
        from server import app

        # Create client
        app.include_router(encryption_key_router, prefix="/keys")
        client = TestClient(app)

        response = client.post("http://localhost:9090/keys/generate")
        assert response.status_code == status.HTTP_201_CREATED
        assert "id" in response.json()


def test_get_encryption_key_success(mock_encryption_key_controller):
    mock_encryption_key_controller.get_encryption_key_by_id.return_value = {
        "id": 1,
        "key_type": EncryptionKeyType.MSG_PROTECT_SHIELD,
        "status": EncryptionKeyStatus.ACTIVE,
        # add more fields as needed based on EncryptionKey schema
    }

    def get_mock_controller():
        return mock_encryption_key_controller

    with patch("api.encryption.controllers.encryption_key_controller.EncryptionKeyController", get_mock_controller):
        from api.encryption.routes.encryption_key_router import encryption_key_router
        from server import app

        # Create client
        app.include_router(encryption_key_router, prefix="/keys")
        client = TestClient(app)

        response = client.get("http://localhost:9090/keys/1")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == 1


def test_get_public_encryption_key_by_id_success(mock_encryption_key_controller):
    mock_encryption_key_controller.get_public_encryption_key_by_id.return_value = {
        "id": 1,
        "key_type": EncryptionKeyType.MSG_PROTECT_SHIELD,
        # add more fields as needed based on EncryptionKey schema
    }

    def get_mock_controller():
        return mock_encryption_key_controller

    with patch("api.encryption.controllers.encryption_key_controller.EncryptionKeyController", get_mock_controller):
        from api.encryption.routes.encryption_key_router import encryption_key_router
        from server import app

        # Create client
        app.include_router(encryption_key_router, prefix="/keys")
        client = TestClient(app)

        response = client.get("http://localhost:9090/keys/public/1")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == 1


def test_get_active_encryption_key_by_type_success(mock_encryption_key_controller):
    mock_encryption_key_controller.get_active_encryption_key_by_type.return_value = {
        "id": 1,
        "key_type": EncryptionKeyType.MSG_PROTECT_SHIELD,
        "status": EncryptionKeyStatus.ACTIVE,
        # add more fields as needed based on EncryptionKey schema
    }

    def get_mock_controller():
        return mock_encryption_key_controller

    with patch("api.encryption.controllers.encryption_key_controller.EncryptionKeyController", get_mock_controller):
        from api.encryption.routes.encryption_key_router import encryption_key_router
        from server import app

        # Create client
        app.include_router(encryption_key_router, prefix="/keys")
        client = TestClient(app)

        response = client.get("http://localhost:9090/keys/status/active")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == 1


def test_disable_passive_encryption_key_success(mock_encryption_key_controller):
    def get_mock_controller():
        return mock_encryption_key_controller

    with patch("api.encryption.controllers.encryption_key_controller.EncryptionKeyController", get_mock_controller):
        from api.encryption.routes.encryption_key_router import encryption_key_router
        from server import app

        # Create client
        app.include_router(encryption_key_router, prefix="/keys")
        client = TestClient(app)

        response = client.put("http://localhost:9090/keys/disable/1")
        assert response.status_code == status.HTTP_200_OK


def test_delete_encryption_key_success(mock_encryption_key_controller):
    def get_mock_controller():
        return mock_encryption_key_controller

    with patch("api.encryption.controllers.encryption_key_controller.EncryptionKeyController", get_mock_controller):
        from api.encryption.routes.encryption_key_router import encryption_key_router
        from server import app

        # Create client
        app.include_router(encryption_key_router, prefix="/keys")
        client = TestClient(app)

        response = client.delete("http://localhost:9090/keys/1")
        assert response.status_code == status.HTTP_204_NO_CONTENT