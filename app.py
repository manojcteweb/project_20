import logging
from flask import Flask, jsonify, request
from services.loan_offer_service import LoanOfferService
from services.loan_approval_service import LoanApprovalService
from utils.logging_config import setup_logging

# Initialize logger
logger = setup_logging()

# Initialize Flask app
app = Flask(__name__)

# Initialize services
loan_offer_service = LoanOfferService()
loan_approval_service = LoanApprovalService()

@app.route('/create-loan-offer', methods=['POST'])
def create_loan_offer():
    """
    Endpoint to create a loan offer.
    """
    customer_data = request.json
    logger.info("Received request to create loan offer for customer: %s", customer_data)
    loan_offer = loan_offer_service.generate_loan_offer(customer_data)
    presentation = loan_offer_service.present_loan_offer(loan_offer)
    return jsonify({'loan_offer': loan_offer, 'presentation': presentation}), 201

@app.route('/approve-loan-application', methods=['POST'])
def approve_loan_application():
    """
    Endpoint to approve a loan application.
    """
    customer_id = request.json.get('customer_id')
    logger.info("Received request to approve loan application for customer ID: %s", customer_id)
    loan_approved = loan_approval_service.approve_loan(customer_id)
    return jsonify({'loan_approved': loan_approved}), 200

@app.route('/loan/offer/<applicant_id>', methods=['GET'])
def get_loan_offer(applicant_id):
    """
    Endpoint to get a loan offer for a specific applicant.
    """
    logger.info("Received request to get loan offer for applicant ID: %s", applicant_id)
    applicant_data = loan_offer_service.loan_model.get_applicant_data(applicant_id)
    if not applicant_data:
        return jsonify({'error': 'Applicant not found'}), 404
    loan_offer = loan_offer_service.generate_loan_offer(applicant_data)
    presentation = loan_offer_service.present_loan_offer(loan_offer)
    return jsonify({'loan_offer': loan_offer, 'presentation': presentation}), 200

@app.route('/loan/approve/<applicant_id>', methods=['POST'])
def approve_loan(applicant_id):
    """
    Endpoint to approve a loan application for a specific applicant.
    """
    logger.info("Received request to approve loan for applicant ID: %s", applicant_id)
    loan_approved = loan_approval_service.approve_loan(applicant_id)
    return jsonify({'loan_approved': loan_approved}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
