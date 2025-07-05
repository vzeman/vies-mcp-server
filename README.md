# VIES MCP Server

A Model Context Protocol (MCP) server for validating EU VAT IDs using the VIES (VAT Information Exchange System) service.

## Custom MCP Server Development
We develop custom MCP Servers for our customers. If you need your own MCP server for your system similar to this MCP server, please contact us (https://www.flowhunt.io/contact/).
Read more how we develop MCP Servers for our customers: https://www.flowhunt.io/services/mcp-server-development/


## Demo

![VIES MCP Server Demo](demo.gif)

## Why VAT ID Validation as an LLM Tool?

Integrating VAT ID validation as an LLM tool provides significant advantages for business automation:

### Real-time Data Accuracy
- **Live validation**: LLMs can verify VAT IDs against the official EU database in real-time, ensuring data accuracy
- **Company details**: Automatically retrieve official company names and addresses, reducing manual data entry errors
- **Compliance assurance**: Ensure VAT IDs are valid before processing transactions or creating records

### Business Process Automation
- **ERP Integration**: When connecting systems like Odoo, SAP, or other ERP platforms, the LLM can automatically:
  - Validate VAT IDs before creating new contacts or customers
  - Auto-populate company information from official sources
  - Flag invalid or expired VAT numbers for review
  
- **Invoice Processing**: Automatically verify supplier VAT IDs during invoice processing workflows
- **Customer Onboarding**: Streamline KYC/KYB processes by validating business customers' VAT information

### Intelligent Decision Making
- **Context-aware validation**: LLMs can understand when VAT validation is needed based on conversation context
- **Error handling**: Provide meaningful explanations when validation fails (e.g., incorrect format, expired number)
- **Cross-border transactions**: Help determine correct tax treatment based on validated VAT status

### Example Use Cases
1. **Automated Contact Creation**: "Create a new customer in Odoo with VAT ID DE123456789" - The LLM validates the VAT ID and retrieves the official company details before creating the contact
2. **Bulk Import Validation**: Process spreadsheets of customer data, validating all VAT IDs before import
3. **Compliance Reporting**: Generate reports of all customers with invalid or missing VAT IDs
4. **Smart Forms**: Build conversational interfaces that validate VAT IDs as users provide them

## Features

- Validate EU VAT IDs through the official VIES REST API
- Get company information (name and address) when available
- List all supported EU countries
- Built with Python and MCP SDK

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/vies-mcp-server.git
cd vies-mcp-server

# Install the package
pip install -e .
```

## Usage

### Running the server

The server can be run directly:

```bash
python -m vies_mcp_server
```

Or using the installed script:

```bash
vies-mcp-server
```

### Available Tools

1. **validate_vat**: Validate an EU VAT ID
   - Input: `vat_id` (string) - The VAT ID to validate (e.g., "DE123456789")
   - Returns: Validation result including validity status, company name, and address (if available)

2. **get_eu_countries**: Get list of EU countries that support VIES VAT validation
   - No input required
   - Returns: List of country codes and names

### Integration with Claude Desktop

Add the following to your Claude Desktop configuration:

```json
{
  "mcpServers": {
    "vies": {
      "command": "/path/to/vies-mcp-server/venv/bin/python",
      "args": ["-m", "vies_mcp_server"],
      "cwd": "/path/to/vies-mcp-server"
    }
  }
}
```

### Example Usage

Once integrated with your MCP client, you can:

1. Validate a German VAT ID:
   ```
   validate_vat("DE123456789")
   ```

2. Get list of supported countries:
   ```
   get_eu_countries()
   ```

## Supported Countries

The server supports VAT validation for all EU member states:
- AT (Austria)
- BE (Belgium)
- BG (Bulgaria)
- CY (Cyprus)
- CZ (Czech Republic)
- DE (Germany)
- DK (Denmark)
- EE (Estonia)
- EL (Greece)
- ES (Spain)
- FI (Finland)
- FR (France)
- HR (Croatia)
- HU (Hungary)
- IE (Ireland)
- IT (Italy)
- LT (Lithuania)
- LU (Luxembourg)
- LV (Latvia)
- MT (Malta)
- NL (Netherlands)
- PL (Poland)
- PT (Portugal)
- RO (Romania)
- SE (Sweden)
- SI (Slovenia)
- SK (Slovakia)

## API Reference

The server uses the official EU VIES REST API:
- Base URL: https://ec.europa.eu/taxation_customs/vies/rest-api/
- Documentation: https://ec.europa.eu/taxation_customs/vies/#/vat-validation

## Error Handling

The server handles various error cases:
- Invalid country codes
- Invalid VAT number formats
- Network timeouts
- API errors
- Invalid responses

All errors are returned with descriptive messages to help diagnose issues.

## Development

### Requirements

- Python 3.9+
- MCP SDK
- httpx

### Running tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
