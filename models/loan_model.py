import logging
from pymongo import MongoClient
from config import MONGO_URI, DATABASE_NAME

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LoanModel:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[DATABASE_NAME]
        self.collection = self.db['loan_offers']

    def save_loan_offer(self, loan_offer):
        """
        Save a loan offer to the database.
        """
        logger.info("Saving loan offer to the database: %s", loan_offer)
        result = self.collection.insert_one(loan_offer)
        logger.info("Loan offer saved with ID: %s", result.inserted_id)
        return result.inserted_id

    def get_applicant_data(self, customer_id):
        """
        Retrieve applicant data from the database using customer ID.
        """
        logger.info("Fetching applicant data for customer ID: %s", customer_id)
        applicant_data = self.collection.find_one({"customer_id": customer_id})
        if applicant_data:
            logger.info("Applicant data found: %s", applicant_data)
        else:
            logger.warning("No applicant data found for customer ID: %s", customer_id)
        return applicant_data

    def save_loan_approval(self, customer_id, approval_status):
        """
        Save the loan approval status to the database.
        """
        logger.info("Saving loan approval status for customer ID %s: %s", customer_id, approval_status)
        result = self.collection.update_one(
            {"customer_id": customer_id},
            {"$set": {"loan_approved": approval_status}}
        )
        if result.modified_count > 0:
            logger.info("Loan approval status updated for customer ID: %s", customer_id)
        else:
            logger.warning("Failed to update loan approval status for customer ID: %s", customer_id)
        return result.modified_count > 0
