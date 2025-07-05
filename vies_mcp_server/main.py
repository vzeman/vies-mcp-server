import asyncio
import logging
from typing import Any

from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

from .vat_validator import VIESValidator, VATValidationError

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create server instance
server = Server("vies-mcp-server")

# Create validator instance
validator = VIESValidator()


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools for VAT validation"""
    return [
        types.Tool(
            name="validate_vat",
            description="Validate an EU VAT ID using the VIES service",
            inputSchema={
                "type": "object",
                "properties": {
                    "vat_id": {
                        "type": "string",
                        "description": "The VAT ID to validate (e.g., 'DE123456789')",
                        "pattern": "^[A-Z]{2}[A-Z0-9]+$"
                    }
                },
                "required": ["vat_id"]
            }
        ),
        types.Tool(
            name="get_eu_countries",
            description="Get list of EU countries that support VIES VAT validation",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, 
    arguments: dict[str, Any]
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool execution"""
    
    if name == "validate_vat":
        vat_id = arguments.get("vat_id", "").strip()
        
        if not vat_id:
            return [types.TextContent(
                type="text",
                text="Error: VAT ID is required"
            )]
        
        try:
            # Run validation in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None, 
                validator.validate_vat, 
                vat_id
            )
            
            # Format response
            response_text = f"VAT Validation Result for {vat_id}:\n"
            response_text += f"Valid: {'Yes' if result.is_valid else 'No'}\n"
            response_text += f"Country Code: {result.country_code}\n"
            response_text += f"VAT Number: {result.vat_number}\n"
            
            if result.request_date:
                response_text += f"Request Date: {result.request_date}\n"
            if result.name:
                response_text += f"Company Name: {result.name}\n"
            if result.address:
                response_text += f"Company Address: {result.address}\n"
            if result.error_message:
                response_text += f"Error: {result.error_message}\n"
            
            return [types.TextContent(
                type="text",
                text=response_text
            )]
            
        except VATValidationError as e:
            return [types.TextContent(
                type="text",
                text=f"Validation Error: {str(e)}"
            )]
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return [types.TextContent(
                type="text",
                text=f"Unexpected error: {str(e)}"
            )]
    
    elif name == "get_eu_countries":
        countries = {
            "AT": "Austria",
            "BE": "Belgium",
            "BG": "Bulgaria",
            "CY": "Cyprus",
            "CZ": "Czech Republic",
            "DE": "Germany",
            "DK": "Denmark",
            "EE": "Estonia",
            "EL": "Greece",
            "ES": "Spain",
            "FI": "Finland",
            "FR": "France",
            "HR": "Croatia",
            "HU": "Hungary",
            "IE": "Ireland",
            "IT": "Italy",
            "LT": "Lithuania",
            "LU": "Luxembourg",
            "LV": "Latvia",
            "MT": "Malta",
            "NL": "Netherlands",
            "PL": "Poland",
            "PT": "Portugal",
            "RO": "Romania",
            "SE": "Sweden",
            "SI": "Slovenia",
            "SK": "Slovakia"
        }
        
        response_text = "EU Countries supporting VIES VAT validation:\n\n"
        for code, name in sorted(countries.items()):
            response_text += f"{code} - {name}\n"
        
        return [types.TextContent(
            type="text",
            text=response_text
        )]
    
    else:
        return [types.TextContent(
            type="text",
            text=f"Unknown tool: {name}"
        )]


async def main():
    """Main entry point for the MCP server"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="vies-mcp-server",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())