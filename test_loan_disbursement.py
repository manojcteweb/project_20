import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from flask.testing import FlaskClient
from loan_disbursement_service import LoanDisbursementService
from loan_disbursement_controller import LoanDisbursementController

@pytest.fixture
def app() -> Flask:
    app = Flask(__name__)
    app.testing = True
    return app

@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()

@pytest.fixture
@patch('loan_disbursement_service.LoanDisbursementService')
def controller(mock_service) -> LoanDisbursementController:
    return LoanDisbursementController()

@patch('loan_disbursement_service.LoanDisbursementService.disburse_loan')
def test_disburse_loan_success(mock_disburse_loan, client: FlaskClient, controller: LoanDisbursementController):
    mock_disburse_loan.return_value = {'status': 'success', 'message': 'Loan disbursed successfully.'}

    response = client.post('/disburse', json={
        'loan_id': 'loan123',
        'amount': 1000,
        'account_number': 'account456'
    })

    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert response.json['message'] == 'Loan disbursed successfully.'

@patch('loan_disbursement_service.LoanDisbursementService.disburse_loan')
def test_disburse_loan_security_failure(mock_disburse_loan, client: FlaskClient, controller: LoanDisbursementController):
    mock_disburse_loan.return_value = {'status': 'failed', 'message': 'Security validation failed.'}

    response = client.post('/disburse', json={
        'loan_id': '',
        'amount': 1000,
        'account_number': 'account456'
    })

    assert response.status_code == 200
    assert response.json['status'] == 'failed'
    assert response.json['message'] == 'Security validation failed.'

@patch('loan_disbursement_service.LoanDisbursementService.disburse_loan')
def test_disburse_loan_approval_failure(mock_disburse_loan, client: FlaskClient, controller: LoanDisbursementController):
    mock_disburse_loan.return_value = {'status': 'failed', 'message': 'Loan approval status verification failed.'}

    response = client.post('/disburse', json={
        'loan_id': 'loan123',
        'amount': 1000,
        'account_number': 'account456'
    })

    assert response.status_code == 200
    assert response.json['status'] == 'failed'
    assert response.json['message'] == 'Loan approval status verification failed.'

@patch('loan_disbursement_service.LoanDisbursementService.disburse_loan')
def test_disburse_loan_bank_details_failure(mock_disburse_loan, client: FlaskClient, controller: LoanDisbursementController):
    mock_disburse_loan.return_value = {'status': 'failed', 'message': 'Dealer bank details verification failed.'}

    response = client.post('/disburse', json={
        'loan_id': 'loan123',
        'amount': 1000,
        'account_number': 'account456'
    })

    assert response.status_code == 200
    assert response.json['status'] == 'failed'
    assert response.json['message'] == 'Dealer bank details verification failed.'

@patch('loan_disbursement_service.LoanDisbursementService.disburse_loan')
def test_disburse_loan_request_exception(mock_disburse_loan, client: FlaskClient, controller: LoanDisbursementController):
    mock_disburse_loan.return_value = {'status': 'failed', 'message': 'Error during disbursement'}

    response = client.post('/disburse', json={
        'loan_id': 'loan123',
        'amount': 1000,
        'account_number': 'account456'
    })

    assert response.status_code == 200
    assert response.json['status'] == 'failed'
    assert 'Error during disbursement' in response.json['message']
