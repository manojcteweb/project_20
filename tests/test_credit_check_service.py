import pytest
from unittest.mock import MagicMock, patch
from credit_check_service import CreditCheckService

class TestCreditCheckService:
    @pytest.fixture
    def mock_db(self):
        return MagicMock()

    @pytest.fixture
    def credit_check_service(self, mock_db):
        return CreditCheckService(mock_db)

    @patch('notification_service.NotificationService.send_credit_check_result')
    def test_initiate_credit_check(self, mock_send_notification, credit_check_service, mock_db):
        user_id = "user123"
        
        # Mock external API call if any
        with patch('requests.post') as mock_post:
            mock_post.return_value.status_code = 200
            
            # Call the method under test
            result = credit_check_service.initiate_credit_check(user_id)

            # Verify that the credit check was initiated
            assert result["user_id"] == user_id
            assert result["status"] == "initiated"

            # Verify that the database insert was called
            mock_db.credit_checks.insert_one.assert_called_once_with({"user_id": user_id, "status": "initiated"})

            # Verify that the notification service was called
            mock_send_notification.assert_called_once_with(user_id, "initiated")

            # Verify that the external API was called
            mock_post.assert_called_once()