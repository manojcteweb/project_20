import logging
from flask import Blueprint, request, jsonify
from services.loan_offer_service import LoanOfferService
from services.loan_approval_service import LoanApprovalService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a Flask Blueprint for loan operations
loan_blueprint = Blueprint('loan', __name__)

# Initialize services
loan_offer_service = LoanOfferService()
loan_approval_service = LoanApprovalService()

@loan_blueprint.route('/create-loan-offer', methods=['POST'])
def create_loan_offer():
    """
    Endpoint to create a loan offer.
    """
    customer_data = request.json
    logger.info("Received request to create loan offer for customer: %s", customer_data)
    loan_offer = loan_offer_service.generate_loan_offer(customer_data)
    return jsonify(loan_offer), 201

@loan_blueprint.route('/approve-loan-application', methods=['POST'])
def approve_loan_application():
    """
    Endpoint to approve a loan application.
    """
    customer_id = request.json.get('customer_id')
    logger.info("Received request to approve loan application for customer ID: %s", customer_id)
    loan_approved = loan_approval_service.approve_loan(customer_id)
    return jsonify({'loan_approved': loan_approved}), 200