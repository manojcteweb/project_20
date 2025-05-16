import logging
from flask import Flask, request, jsonify
from services.credit_check_service import CreditCheckService
from services.document_verification_service import DocumentVerificationService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class LoanApplicationController:
    def __init__(self, credit_check_service, document_verification_service):
        self.credit_check_service = credit_check_service
        self.document_verification_service = document_verification_service

    def submit_application(self, customer_id):
        logger.info(f"Submitting loan application for customer {customer_id}")
        # Logic to submit loan application
        # This could involve initiating a credit check and verifying documents
        self.credit_check_service.initiate_credit_check(customer_id)
        self.document_verification_service.verify_documents(customer_id)
        return jsonify({"message": "Loan application submitted successfully"}), 200

    def check_credit_status(self, credit_check_id):
        logger.info(f"Checking credit status for credit check {credit_check_id}")
        # Logic to check credit status
        # This could involve querying the credit check status from the database
        # Example: status = self.credit_check_service.get_credit_status(credit_check_id)
        status = "pending"  # Placeholder for actual status
        return jsonify({"credit_check_id": credit_check_id, "status": status}), 200

    def verify_documents(self, customer_id):
        logger.info(f"Verifying documents for customer {customer_id}")
        # Logic to verify documents
        # This could involve checking the document verification status
        self.document_verification_service.verify_documents(customer_id)
        return jsonify({"message": "Documents verified successfully"}), 200

# Initialize services
credit_check_service = CreditCheckService(db_client=None)  # Replace None with actual DB client

document_verification_service = DocumentVerificationService(db_client=None)  # Replace None with actual DB client

# Initialize controller
loan_application_controller = LoanApplicationController(credit_check_service, document_verification_service)

# Define routes
@app.route('/submit_application/<customer_id>', methods=['POST'])
def submit_application(customer_id):
    return loan_application_controller.submit_application(customer_id)

@app.route('/check_credit_status/<credit_check_id>', methods=['GET'])
def check_credit_status(credit_check_id):
    return loan_application_controller.check_credit_status(credit_check_id)

@app.route('/verify_documents/<customer_id>', methods=['POST'])
def verify_documents(customer_id):
    return loan_application_controller.verify_documents(customer_id)

if __name__ == '__main__':
    app.run(debug=True)
