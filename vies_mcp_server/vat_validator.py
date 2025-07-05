import httpx
import json
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class VATValidationResult:
    """Result of VAT validation from VIES service"""
    is_valid: bool
    country_code: str
    vat_number: str
    request_date: Optional[str] = None
    name: Optional[str] = None
    address: Optional[str] = None
    error_message: Optional[str] = None


class VATValidationError(Exception):
    """Exception raised when VAT validation fails"""
    pass


class VIESValidator:
    """Validates EU VAT IDs using the VIES REST API"""
    
    BASE_URL = "https://ec.europa.eu"
    TIMEOUT = 10
    
    def __init__(self):
        self.client = httpx.Client(
            base_url=self.BASE_URL,
            timeout=self.TIMEOUT,
            follow_redirects=False,
            verify=False  # Note: In production, you should use proper SSL verification
        )
    
    def validate_vat(self, vat_id: str) -> VATValidationResult:
        """
        Validate a VAT ID using the VIES REST API
        
        Args:
            vat_id: The VAT ID to validate (e.g., "DE123456789")
            
        Returns:
            VATValidationResult with validation details
            
        Raises:
            VATValidationError: If validation request fails
        """
        # Extract country code and VAT number
        if len(vat_id) < 3:
            raise VATValidationError("VAT ID too short")
        
        country_code = vat_id[:2].upper()
        vat_number = vat_id[2:]
        
        # Validate country code (basic check)
        valid_countries = [
            "AT", "BE", "BG", "CY", "CZ", "DE", "DK", "EE", "EL", "ES",
            "FI", "FR", "HR", "HU", "IE", "IT", "LT", "LU", "LV", "MT",
            "NL", "PL", "PT", "RO", "SE", "SI", "SK"
        ]
        
        if country_code not in valid_countries:
            raise VATValidationError(f"Invalid country code: {country_code}")
        
        try:
            # Make request to VIES REST API
            response = self.client.get(
                f"/taxation_customs/vies/rest-api/ms/{country_code}/vat/{vat_number}"
            )
            response.raise_for_status()
            
            # Parse response
            data = response.json()
            
            # Check for user errors
            if "userError" in data:
                if data["userError"] != "VALID":
                    error_message = data.get("userError", "Unknown error")
                    return VATValidationResult(
                        is_valid=False,
                        country_code=country_code,
                        vat_number=vat_number,
                        error_message=error_message
                    )
            
            # Extract validation result
            is_valid = data.get("isValid", False)
            
            return VATValidationResult(
                is_valid=is_valid,
                country_code=country_code,
                vat_number=vat_number,
                request_date=data.get("requestDate"),
                name=data.get("name"),
                address=data.get("address")
            )
            
        except httpx.HTTPStatusError as e:
            raise VATValidationError(f"HTTP error: {e.response.status_code}")
        except httpx.RequestError as e:
            raise VATValidationError(f"Request error: {str(e)}")
        except json.JSONDecodeError as e:
            raise VATValidationError(f"Invalid JSON response: {str(e)}")
        except Exception as e:
            raise VATValidationError(f"Validation failed: {str(e)}")
    
    def __del__(self):
        """Clean up HTTP client"""
        if hasattr(self, 'client'):
            self.client.close()