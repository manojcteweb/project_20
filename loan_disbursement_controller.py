import logging
from flask import Flask, request, jsonify
from loan_disbursement_service import LoanDisbursementService

app = Flask(__name__)

# Initialize the LoanDisbursementService
loan_service = LoanDisbursementService()

class LoanDisbursementController:
    def __init__(self):
        self.logger = logging.getLogger('LoanDisbursementController')
        self.logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def disburse_loan(self):
        """
        Endpoint to disburse a loan.

        Expects JSON payload with 'loan_id', 'amount', and 'account_number'.
        """
        data = request.get_json()
        loan_id = data.get('loan_id')
        amount = data.get('amount')
        account_number = data.get('account_number')

        self.logger.info(f"Received disbursement request for loan ID: {loan_id}")

        # Call the service to disburse the loan
        result = loan_service.disburse_loan(loan_id, amount, account_number)

        return jsonify(result)

# Define the route for loan disbursement
@app.route('/disburse', methods=['POST'])
def disburse_loan():
    controller = LoanDisbursementController()
    return controller.disburse_loan()

if __name__ == '__main__':
    app.run(debug=True)