import logging
import requests
from models import LoanModel
from notification_service import NotificationService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LoanOfferService:
    def __init__(self):
        self.notification_service = NotificationService("http://notification.service/send")
        self.loan_model = LoanModel()

    def generate_loan_offer(self, customer_data):
        """
        Generate a loan offer based on customer data.
        """
        logger.info("Generating loan offer for customer: %s", customer_data)
        
        # Fetch applicant data (simulated here as customer_data is passed)
        # Placeholder logic for generating a loan offer
        loan_offer = {
            "customer_id": customer_data.get("id"),
            "loan_amount": 10000,
            "interest_rate": 5.0,
            "term": 36
        }
        
        # Store the loan offer using LoanModel
        loan_offer_id = self.loan_model.save_loan_offer(loan_offer)
        logger.info("Loan offer generated and stored with ID: %s", loan_offer_id)
        
        return loan_offer

    def present_loan_offer(self, loan_offer):
        """
        Present the loan offer to the customer.
        """
        logger.info("Presenting loan offer: %s", loan_offer)
        # Implementing the logic to present the loan offer details
        presentation = (
            f"Loan Offer Details:\n"
            f"Customer ID: {loan_offer['customer_id']}\n"
            f"Loan Amount: ${loan_offer['loan_amount']}\n"
            f"Interest Rate: {loan_offer['interest_rate']}%\n"
            f"Term: {loan_offer['term']} months\n"
        )
        logger.info("Loan offer presented: %s", presentation)
        return presentation

    def send_notification(self, message):
        """
        Send a notification to the customer using the NotificationService.
        """
        self.notification_service.send_notification(message)
