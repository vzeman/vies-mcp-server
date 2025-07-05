#!/usr/bin/env python3
from vies_mcp_server.vat_validator import VIESValidator, VATValidationError

def test_vat_id(vat_id):
    validator = VIESValidator()
    
    print(f"\nValidating VAT ID: {vat_id}")
    print("-" * 40)
    
    try:
        result = validator.validate_vat(vat_id)
        
        print(f"Valid: {'Yes' if result.is_valid else 'No'}")
        print(f"Country Code: {result.country_code}")
        print(f"VAT Number: {result.vat_number}")
        
        if result.request_date:
            print(f"Request Date: {result.request_date}")
        if result.name:
            print(f"Company Name: {result.name}")
        if result.address:
            print(f"Company Address: {result.address}")
        if result.error_message:
            print(f"Error: {result.error_message}")
            
    except VATValidationError as e:
        print(f"Validation Error: {str(e)}")
    except Exception as e:
        print(f"Unexpected Error: {str(e)}")

if __name__ == "__main__":
    # Test the Czech VAT ID
    test_vat_id("CZ22323074")