import logging
import requests
from pwn import *

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LoanOfferService:
    def __init__(self):
        self.notification_endpoint = "http://notification.service/send"

    def generate_loan_offer(self, customer_data):
        """
        Generate a loan offer based on customer data.
        """
        logger.info("Generating loan offer for customer: %s", customer_data)
        # Placeholder logic for generating a loan offer
        loan_offer = {
            "customer_id": customer_data.get("id"),
            "loan_amount": 10000,
            "interest_rate": 5.0,
            "term": 36
        }
        logger.info("Loan offer generated: %s", loan_offer)
        return loan_offer

    def present_loan_offer(self, loan_offer):
        """
        Present the loan offer to the customer.
        """
        logger.info("Presenting loan offer: %s", loan_offer)
        # Placeholder logic for presenting a loan offer
        return f"Loan Offer: {loan_offer}"

    def send_notification(self, message):
        """
        Send a notification to the customer.
        """
        logger.info("Sending notification: %s", message)
        try:
            response = requests.post(self.notification_endpoint, json={"message": message})
            response.raise_for_status()
            logger.info("Notification sent successfully.")
        except requests.exceptions.RequestException as e:
            logger.error("Failed to send notification: %s", e)
            raise