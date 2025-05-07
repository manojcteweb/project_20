import pytest
from unittest.mock import patch, MagicMock
from services.notification_service import NotificationService

@pytest.fixture
def notification_service():
    return NotificationService(email_endpoint="http://email.service/send", sms_endpoint="http://sms.service/send")

@patch('services.notification_service.requests.post')
def test_send_email_notification(mock_post, notification_service):
    # Mock the response to simulate a successful email send
    mock_post.return_value.raise_for_status = MagicMock()
    email_data = {'to': 'customer@example.com', 'subject': 'Loan Offer', 'body': 'Your loan offer details...'}
    
    # Call the send_email_notification method
    notification_service.send_email_notification(email_data)
    
    # Verify that the post request was made with the correct parameters
    mock_post.assert_called_once_with(notification_service.email_endpoint, json=email_data)

@patch('services.notification_service.requests.post')
def test_send_sms_notification(mock_post, notification_service):
    # Mock the response to simulate a successful SMS send
    mock_post.return_value.raise_for_status = MagicMock()
    sms_data = {'to': '+1234567890', 'message': 'Your loan offer details...'}
    
    # Call the send_sms_notification method
    notification_service.send_sms_notification(sms_data)
    
    # Verify that the post request was made with the correct parameters
    mock_post.assert_called_once_with(notification_service.sms_endpoint, json=sms_data)