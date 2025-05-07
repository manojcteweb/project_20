import pytest
from unittest.mock import patch
from services.loan_offer_service import LoanOfferService

@pytest.fixture
def loan_offer_service():
    return LoanOfferService()

@patch('services.loan_offer_service.LoanModel')
def test_generate_loan_offer(mock_loan_model, loan_offer_service):
    # Mock the save_loan_offer method to return a mock ID
    mock_loan_model.return_value.save_loan_offer.return_value = 'mock_id'
    
    # Define sample customer data
    customer_data = {'id': '123'}
    
    # Call the generate_loan_offer method
    loan_offer = loan_offer_service.generate_loan_offer(customer_data)
    
    # Assertions to verify the loan offer details
    assert loan_offer['customer_id'] == '123'
    assert loan_offer['loan_amount'] == 10000
    assert loan_offer['interest_rate'] == 5.0
    assert loan_offer['term'] == 36
    
    # Verify that the save_loan_offer method was called once
    mock_loan_model.return_value.save_loan_offer.assert_called_once_with(loan_offer)

@patch('services.loan_offer_service.LoanModel')
def test_present_loan_offer(mock_loan_model, loan_offer_service):
    # Define a sample loan offer
    loan_offer = {
        'customer_id': '123',
        'loan_amount': 10000,
        'interest_rate': 5.0,
        'term': 36
    }
    
    # Call the present_loan_offer method
    presentation = loan_offer_service.present_loan_offer(loan_offer)
    
    # Assertions to verify the presentation format
    assert 'Loan Offer Details' in presentation
    assert 'Customer ID: 123' in presentation
    assert 'Loan Amount: $10000' in presentation
    assert 'Interest Rate: 5.0%' in presentation
    assert 'Term: 36 months' in presentation
