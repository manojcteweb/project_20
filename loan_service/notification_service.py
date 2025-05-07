import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NotificationService:
    def __init__(self, endpoint):
        self.endpoint = endpoint

    def send_notification(self, message):
        """
        Send a notification to the customer.
        """
        logger.info("Sending notification: %s", message)
        try:
            response = requests.post(self.endpoint, json={"message": message})
            response.raise_for_status()
            logger.info("Notification sent successfully.")
        except requests.exceptions.RequestException as e:
            logger.error("Failed to send notification: %s", e)
            raise