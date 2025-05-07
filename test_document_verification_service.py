import pytest
from unittest.mock import MagicMock, patch
from document_verification_service import DocumentVerificationService

class TestDocumentVerificationService:
    @pytest.fixture
    def mock_db(self):
        return MagicMock()

    @pytest.fixture
    def document_verification_service(self, mock_db):
        return DocumentVerificationService(mock_db)

    @patch('notification_service.NotificationService.send_verification_result')
    def test_verify_documents(self, mock_send_notification, document_verification_service, mock_db):
        user_id = "user123"
        documents = {"id": True, "passport": True}

        # Call the method under test
        result = document_verification_service.verify_documents(user_id, documents)

        # Verify that the documents were verified
        assert result["user_id"] == user_id
        assert result["status"] == "verified"

        # Verify that the database insert was called
        mock_db.document_verifications.insert_one.assert_called_once_with({
            "user_id": user_id,
            "status": "verified",
            "documents": documents,
            "timestamp": result["timestamp"]  # We can't predict the exact timestamp
        })

        # Verify that the notification service was called
        mock_send_notification.assert_called_once_with(user_id, "verified")

    @patch('notification_service.NotificationService.send_verification_result')
    def test_flag_incomplete_or_fraudulent(self, mock_send_notification, document_verification_service, mock_db):
        user_id = "user123"

        # Setup the mock to return an incomplete verification record
        mock_db.document_verifications.find_one.return_value = {
            "user_id": user_id,
            "status": "incomplete"
        }

        # Call the method under test
        result = document_verification_service.flag_incomplete_or_fraudulent(user_id)

        # Verify that the documents were flagged
        assert result["user_id"] == user_id
        assert result["status"] == "flagged"
        assert result["flag_reason"] == "Incomplete or fraudulent documents detected"

        # Verify that the database update was called
        mock_db.document_verifications.update_one.assert_called_once_with(
            {"user_id": user_id},
            {"$set": {"status": "flagged", "flag_reason": "Incomplete or fraudulent documents detected"}}
        )

        # Verify that the notification service was called
        mock_send_notification.assert_called_once_with(user_id, "flagged")