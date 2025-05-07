import logging
from pymongo import MongoClient

class DealerModel:
    def __init__(self, db_uri='mongodb://localhost:27017/', db_name='loan_service'):
        self.logger = logging.getLogger('DealerModel')
        self.logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

        self.client = MongoClient(db_uri)
        self.db = self.client[db_name]
        self.dealers_collection = self.db['dealers']

    def get_dealer_by_id(self, dealer_id):
        """
        Retrieve dealer data by dealer ID.

        :param dealer_id: ID of the dealer
        :return: Dealer data as a dictionary
        """
        self.logger.info(f"Retrieving dealer data for dealer ID: {dealer_id}")
        dealer_data = self.dealers_collection.find_one({"dealer_id": dealer_id})
        if dealer_data:
            self.logger.info(f"Dealer data retrieved for dealer ID: {dealer_id}")
            return dealer_data
        else:
            self.logger.warning(f"No dealer data found for dealer ID: {dealer_id}")
            return None

    def update_dealer_status(self, dealer_id, status):
        """
        Update the status of a dealer.

        :param dealer_id: ID of the dealer
        :param status: New status to be set
        :return: Boolean indicating if the update was successful
        """
        self.logger.info(f"Updating dealer status for dealer ID: {dealer_id} to {status}")
        result = self.dealers_collection.update_one(
            {"dealer_id": dealer_id},
            {"$set": {"status": status}}
        )
        if result.modified_count > 0:
            self.logger.info(f"Dealer status updated for dealer ID: {dealer_id}")
            return True
        else:
            self.logger.warning(f"Failed to update dealer status for dealer ID: {dealer_id}")
            return False
