import pytest
from unittest.mock import MagicMock, patch
from notification_service import NotificationService

class TestNotificationService:
    @pytest.fixture
    def notification_service(self):
        return NotificationService()

    @patch('notification_service.NotificationService._send_email_or_sms')
    def test_send_credit_check_result(self, mock_send_email_or_sms, notification_service):
        user_id = "user123"
        result = "approved"

        # Call the method under test
        notification = notification_service.send_credit_check_result(user_id, result)

        # Verify that the notification was created correctly
        assert notification["user_id"] == user_id
        assert notification["type"] == "credit_check"
        assert notification["result"] == result

        # Verify that the email or SMS was sent
        formatted_message = f"Credit Check Result for User {user_id}: {result}"
        mock_send_email_or_sms.assert_called_once_with(user_id, formatted_message)

    @patch('notification_service.NotificationService._send_email_or_sms')
    def test_send_verification_result(self, mock_send_email_or_sms, notification_service):
        user_id = "user123"
        status = "verified"

        # Call the method under test
        notification = notification_service.send_verification_result(user_id, status)

        # Verify that the notification was created correctly
        assert notification["user_id"] == user_id
        assert notification["type"] == "document_verification"
        assert notification["status"] == status

        # Verify that the email or SMS was sent
        formatted_message = f"Document Verification Result for User {user_id}: {status}"
        mock_send_email_or_sms.assert_called_once_with(user_id, formatted_message)