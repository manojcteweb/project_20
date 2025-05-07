import logging
from pymongo import MongoClient

class LoanModel:
    def __init__(self, db_uri='mongodb://localhost:27017/', db_name='loan_service'):
        self.logger = logging.getLogger('LoanModel')
        self.logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

        self.client = MongoClient(db_uri)
        self.db = self.client[db_name]
        self.loans_collection = self.db['loans']

    def get_loan_by_id(self, loan_id):
        """
        Retrieve loan data by loan ID.

        :param loan_id: ID of the loan
        :return: Loan data as a dictionary
        """
        self.logger.info(f"Retrieving loan data for loan ID: {loan_id}")
        loan_data = self.loans_collection.find_one({"loan_id": loan_id})
        if loan_data:
            self.logger.info(f"Loan data retrieved for loan ID: {loan_id}")
            return loan_data
        else:
            self.logger.warning(f"No loan data found for loan ID: {loan_id}")
            return None

    def update_loan_status(self, loan_id, status):
        """
        Update the status of a loan.

        :param loan_id: ID of the loan
        :param status: New status to be set
        :return: Boolean indicating if the update was successful
        """
        self.logger.info(f"Updating loan status for loan ID: {loan_id} to {status}")
        result = self.loans_collection.update_one(
            {"loan_id": loan_id},
            {"$set": {"status": status}}
        )
        if result.modified_count > 0:
            self.logger.info(f"Loan status updated for loan ID: {loan_id}")
            return True
        else:
            self.logger.warning(f"Failed to update loan status for loan ID: {loan_id}")
            return False
