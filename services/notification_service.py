import logging
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NotificationService:
    def __init__(self, email_endpoint, sms_endpoint):
        self.email_endpoint = email_endpoint
        self.sms_endpoint = sms_endpoint

    def send_email_notification(self, email_data):
        """
        Send an email notification.
        """
        logger.info("Sending email notification: %s", email_data)
        try:
            response = requests.post(self.email_endpoint, json=email_data)
            response.raise_for_status()
            logger.info("Email notification sent successfully.")
        except requests.exceptions.RequestException as e:
            logger.error("Failed to send email notification: %s", e)
            raise

    def send_sms_notification(self, sms_data):
        """
        Send an SMS notification.
        """
        logger.info("Sending SMS notification: %s", sms_data)
        try:
            response = requests.post(self.sms_endpoint, json=sms_data)
            response.raise_for_status()
            logger.info("SMS notification sent successfully.")
        except requests.exceptions.RequestException as e:
            logger.error("Failed to send SMS notification: %s", e)
            raise
