import pytest
from unittest.mock import patch, MagicMock
from services.loan_offer_service import LoanOfferService
from services.loan_approval_service import LoanApprovalService

@pytest.fixture
def loan_offer_service():
    return LoanOfferService()

@pytest.fixture
def loan_approval_service():
    return LoanApprovalService()

@patch('services.loan_offer_service.LoanModel')
def test_generate_loan_offer(mock_loan_model, loan_offer_service):
    mock_loan_model.return_value.save_loan_offer.return_value = 'mock_id'
    customer_data = {'id': '123'}
    loan_offer = loan_offer_service.generate_loan_offer(customer_data)
    assert loan_offer['customer_id'] == '123'
    assert loan_offer['loan_amount'] == 10000
    assert loan_offer['interest_rate'] == 5.0
    assert loan_offer['term'] == 36

@patch('services.loan_offer_service.LoanModel')
def test_present_loan_offer(mock_loan_model, loan_offer_service):
    loan_offer = {
        'customer_id': '123',
        'loan_amount': 10000,
        'interest_rate': 5.0,
        'term': 36
    }
    presentation = loan_offer_service.present_loan_offer(loan_offer)
    assert 'Loan Offer Details' in presentation
    assert 'Customer ID: 123' in presentation
    assert 'Loan Amount: $10000' in presentation
    assert 'Interest Rate: 5.0%' in presentation
    assert 'Term: 36 months' in presentation

@patch('services.loan_approval_service.LoanModel')
@patch('services.loan_approval_service.requests.post')
def test_approve_loan(mock_post, mock_loan_model, loan_approval_service):
    mock_loan_model.return_value.get_documents.return_value = {'doc1': True, 'doc2': True}
    mock_post.return_value.json.return_value = {'creditworthy': True}
    mock_post.return_value.raise_for_status = MagicMock()
    customer_id = '123'
    loan_approved = loan_approval_service.approve_loan(customer_id)
    assert loan_approved is True

@patch('services.loan_approval_service.LoanModel')
@patch('services.loan_approval_service.requests.post')
def test_approve_loan_documents_missing(mock_post, mock_loan_model, loan_approval_service):
    mock_loan_model.return_value.get_documents.return_value = {'doc1': True, 'doc2': False}
    mock_post.return_value.json.return_value = {'creditworthy': True}
    mock_post.return_value.raise_for_status = MagicMock()
    customer_id = '123'
    loan_approved = loan_approval_service.approve_loan(customer_id)
    assert loan_approved is False

@patch('services.loan_approval_service.LoanModel')
@patch('services.loan_approval_service.requests.post')
def test_approve_loan_credit_check_fail(mock_post, mock_loan_model, loan_approval_service):
    mock_loan_model.return_value.get_documents.return_value = {'doc1': True, 'doc2': True}
    mock_post.return_value.json.return_value = {'creditworthy': False}
    mock_post.return_value.raise_for_status = MagicMock()
    customer_id = '123'
    loan_approved = loan_approval_service.approve_loan(customer_id)
    assert loan_approved is False
