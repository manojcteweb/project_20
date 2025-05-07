import logging
from flask import Flask, request, jsonify
from pymongo import MongoClient

# Assuming CreditCheckService and DocumentVerificationService are defined in their respective modules
from credit_check_service import CreditCheckService
from document_verification_service import DocumentVerificationService

app = Flask(__name__)

# Setup MongoDB client
client = MongoClient('mongodb://localhost:27017/')
db = client['loan_application_db']

# Initialize services
credit_check_service = CreditCheckService(db)
document_verification_service = DocumentVerificationService(db)

class LoanApplicationController:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def submit_application(self, user_id, documents):
        self.logger.info(f"Submitting loan application for user: {user_id}")

        # Step 1: Verify documents
        verification_result = document_verification_service.verify_documents(user_id, documents)
        if verification_result['status'] != 'verified':
            self.logger.warning(f"Document verification failed for user: {user_id}")
            return jsonify({"error": "Document verification failed", "status": verification_result['status']}), 400

        # Step 2: Initiate credit check
        credit_check_result = credit_check_service.initiate_credit_check(user_id)

        # Return success response
        self.logger.info(f"Loan application submitted successfully for user: {user_id}")
        return jsonify({"message": "Loan application submitted successfully", "credit_check_status": credit_check_result['status']}), 200

# Flask route to handle loan application submission
@app.route('/submit_loan_application', methods=['POST'])
def submit_loan_application():
    data = request.json
    user_id = data.get('user_id')
    documents = data.get('documents')

    if not user_id or not documents:
        return jsonify({"error": "User ID and documents are required"}), 400

    controller = LoanApplicationController()
    return controller.submit_application(user_id, documents)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True)