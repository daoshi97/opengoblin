#!/usr/bin/env python3
"""
TON Blockchain MCP Server
Provides TON blockchain interaction tools via MCP protocol.

Usage:
    python3 ton_mcp_server.py

Requires:
    pip install mcp tonpy
"""

import json
import sys
from tonpy import Tonapi, Wallet, Contract
from tonpy.exceptions import TonException

# Initialize client (uses TONCENTER_API_KEY from env)
api_key = __import__('os').getenv('TONCENTER_API_KEY', '')
testnet = __import__('os').getenv('TON_DEFAULT_NETWORK', 'testnet') == 'testnet'

client = None
if api_key:
    client = Tonapi(api_key=api_key, testnet=testnet)


def handle_request(method, params=None):
    """Handle incoming MCP requests."""
    params = params or {}

    if method == "initialize":
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "ton-mcp", "version": "1.0.0"}
        }

    elif method == "tools/list":
        return {
            "tools": [
                {
                    "name": "get_balance",
                    "description": "Get TON wallet balance",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "address": {"type": "string", "description": "TON address (0:...)"}
                        },
                        "required": ["address"]
                    }
                },
                {
                    "name": "get_account_info",
                    "description": "Get TON account information",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "address": {"type": "string", "description": "TON address (0:...)"}
                        },
                        "required": ["address"]
                    }
                },
                {
                    "name": "send_ton",
                    "description": "Send TON from wallet to address",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "to_address": {"type": "string"},
                            "amount": {"type": "integer", "description": "Amount in nanoTON"},
                            "payload": {"type": "string", "description": "Optional message body"}
                        },
                        "required": ["to_address", "amount"]
                    }
                },
                {
                    "name": "deploy_contract",
                    "description": "Deploy a smart contract to TON",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "code_cell": {"type": "string", "description": "Base64 encoded code cell"},
                            "data_cell": {"type": "string", "description": "Base64 encoded data cell"}
                        },
                        "required": ["code_cell", "data_cell"]
                    }
                },
                {
                    "name": "run_get_method",
                    "description": "Run a read-only get method on a contract",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "address": {"type": "string"},
                            "method": {"type": "string"},
                            "stack": {"type": "array", "description": "Stack items as list"}
                        },
                        "required": ["address", "method"]
                    }
                }
            ]
        }

    elif method == "tools/call":
        tool = params.get("name")
        args = params.get("arguments", {})

        try:
            if tool == "get_balance":
                result = client.get_balance(args["address"])
                return {"result": result}

            elif tool == "get_account_info":
                result = client.get_address_info(args["address"])
                return {"result": result}

            elif tool == "send_ton":
                if not client:
                    return {"error": "TONCENTER_API_KEY not set"}
                # Requires wallet setup
                return {"result": {"status": "requires_wallet_setup"}}

            elif tool == "deploy_contract":
                if not client:
                    return {"error": "TONCENTER_API_KEY not set"}
                return {"result": {"status": "requires_wallet_setup"}}

            elif tool == "run_get_method":
                result = client.run_get_method(args["address"], args["method"], args.get("stack", []))
                return {"result": result}

            else:
                return {"error": f"Unknown tool: {tool}"}

        except TonException as e:
            return {"error": {"code": e.code, "message": e.message}}
        except Exception as e:
            return {"error": str(e)}

    elif method == "notifications/initialized":
        return None

    else:
        return {"error": f"Unknown method: {method}"}


def main():
    """Read JSON-RPC requests from stdin and write responses to stdout."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
            response = handle_request(
                request.get("method"),
                request.get("params")
            )
            if response is not None:
                print(json.dumps({"jsonrpc": "2.0", **response, "id": request.get("id")}))
                sys.stdout.flush()
        except json.JSONDecodeError:
            continue


if __name__ == "__main__":
    main()
