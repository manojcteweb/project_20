import logging
from pymongo import MongoClient

class ApplicationModel:
    def __init__(self, db):
        self.db = db
        self.logger = logging.getLogger(__name__)

    def update_credit_check_status(self, user_id, status, result=None):
        self.logger.info(f"Updating credit check status for user: {user_id}")
        update_data = {"status": status}
        if result is not None:
            update_data["result"] = result
        self.db.credit_checks.update_one(
            {"user_id": user_id},
            {"$set": update_data}
        )
        self.logger.info(f"Credit check status updated for user: {user_id} to {status}")

    def update_verification_status(self, user_id, status, flag_reason=None):
        self.logger.info(f"Updating verification status for user: {user_id}")
        update_data = {"status": status}
        if flag_reason is not None:
            update_data["flag_reason"] = flag_reason
        self.db.document_verifications.update_one(
            {"user_id": user_id},
            {"$set": update_data}
        )
        self.logger.info(f"Verification status updated for user: {user_id} to {status}")