import logging
import requests
from models import LoanModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LoanApprovalService:
    def __init__(self):
        self.loan_model = LoanModel()
        self.credit_check_endpoint = "http://creditcheck.service/check"

    def evaluate_documents(self, customer_id):
        """
        Evaluate the provided documents for loan approval by fetching them from the database.
        """
        logger.info("Fetching documents for customer ID: %s", customer_id)
        
        # Fetch documents from the database using LoanModel
        documents = self.loan_model.get_documents(customer_id)
        
        # Placeholder logic for document evaluation
        evaluation_result = all(documents.values())  # Assume all documents must be present
        logger.info("Document evaluation result for customer ID %s: %s", customer_id, evaluation_result)
        return evaluation_result

    def check_creditworthiness(self, customer_id):
        """
        Check the creditworthiness of the applicant by performing a credit check using an external service.
        """
        logger.info("Performing credit check for customer ID: %s", customer_id)
        try:
            response = requests.post(self.credit_check_endpoint, json={"customer_id": customer_id})
            response.raise_for_status()
            credit_data = response.json()
            is_creditworthy = credit_data.get('creditworthy', False)
            logger.info("Credit check result for customer ID %s: %s", customer_id, is_creditworthy)
            return is_creditworthy
        except requests.exceptions.RequestException as e:
            logger.error("Failed to perform credit check for customer ID %s: %s", customer_id, e)
            return False

    def approve_loan(self, customer_id):
        """
        Approve the loan based on document evaluation and creditworthiness.
        """
        logger.info("Approving loan for customer ID: %s", customer_id)
        documents_ok = self.evaluate_documents(customer_id)
        creditworthy = self.check_creditworthiness(customer_id)
        loan_approved = documents_ok and creditworthy
        logger.info("Loan approval result for customer ID %s: %s", customer_id, loan_approved)
        return loan_approved
