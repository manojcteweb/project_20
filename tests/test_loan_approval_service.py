import pytest
from unittest.mock import patch, MagicMock
from services.loan_approval_service import LoanApprovalService

@pytest.fixture
def loan_approval_service():
    return LoanApprovalService()

@patch('services.loan_approval_service.LoanModel')
@patch('services.loan_approval_service.requests.post')
def test_approve_loan(mock_post, mock_loan_model, loan_approval_service):
    # Mock the get_documents method to return a set of documents
    mock_loan_model.return_value.get_documents.return_value = {'doc1': True, 'doc2': True}
    
    # Mock the response to simulate a successful credit check
    mock_post.return_value.json.return_value = {'creditworthy': True}
    mock_post.return_value.raise_for_status = MagicMock()
    
    # Define a sample customer ID
    customer_id = '123'
    
    # Call the approve_loan method
    loan_approved = loan_approval_service.approve_loan(customer_id)
    
    # Assertions to verify the loan approval result
    assert loan_approved is True
    
    # Verify that the get_documents method was called once with the correct customer ID
    mock_loan_model.return_value.get_documents.assert_called_once_with(customer_id)
    
    # Verify that the post request was made with the correct parameters
    mock_post.assert_called_once_with(loan_approval_service.credit_check_endpoint, json={'customer_id': customer_id})