from pymongo import MongoClient
from config import MONGO_URI, DATABASE_NAME

class LoanModel:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[DATABASE_NAME]
        self.collection = self.db['loan_offers']

    def save_loan_offer(self, loan_offer):
        result = self.collection.insert_one(loan_offer)
        return result.inserted_id