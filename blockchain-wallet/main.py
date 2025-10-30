from fastapi import FastAPI
from pydantic import BaseModel
from web3 import Web3
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get keys and URLs from .env
private_key = os.getenv("PRIVATE_KEY")
alchemy_url = os.getenv("ALCHEMY_API_URL")

# Connect to Alchemy (Sepolia testnet recommended)
web3 = Web3(Web3.HTTPProvider(alchemy_url))

# Check connection
if web3.is_connected():
    print("✅ Connected to blockchain")
else:
    print("❌ Connection failed")

# Initialize FastAPI app
app = FastAPI(title="Blockchain API")

# Pydantic model for transaction
class Transaction(BaseModel):
    to_address: str
    value: float   # in ETH

@app.get("/")
def root():
    return {"message": "Blockchain API is running"}

@app.get("/balance/{address}")
def get_balance(address: str):
    try:
        balance = web3.eth.get_balance(address)
        return {
            "address": address,
            "balance_eth": float(web3.from_wei(balance, "ether"))
        }
    except Exception as e:
        return {"error": str(e)}

@app.post("/send")
def send_transaction(tx: Transaction):
    try:
        # Load sender account from private key
        account = web3.eth.account.from_key(private_key)

        # Get current balance
        balance = web3.eth.get_balance(account.address)
        print("Wallet balance (ETH):", web3.from_wei(balance, "ether"))

        # Convert tx.value to Wei
        value_wei = web3.to_wei(tx.value, "ether")

        # Estimate gas dynamically
        gas_estimate = web3.eth.estimate_gas({
            "to": tx.to_address,
            "from": account.address,
            "value": value_wei
        })
        gas_price = web3.eth.gas_price
        total_needed = value_wei + gas_estimate * gas_price

        if total_needed > balance:
            return {
                "error": "Insufficient funds. Required: {} ETH, Available: {} ETH".format(
                    web3.from_wei(total_needed, "ether"),
                    web3.from_wei(balance, "ether")
                )
            }

        # Get current nonce
        nonce = web3.eth.get_transaction_count(account.address)

        # Build transaction
        transaction = {
            "to": tx.to_address,
            "value": value_wei,
            "gas": gas_estimate,
            "gasPrice": gas_price,
            "nonce": nonce,
            "chainId": 11155111
        }

        # Sign transaction
        signed_tx = web3.eth.account.sign_transaction(transaction, private_key)

        # Send transaction
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)

        return {"tx_hash": web3.to_hex(tx_hash)}

    except Exception as e:
        return {"error": str(e)}

@app.get("/transaction/{tx_hash}")
def get_transaction(tx_hash: str):
    try:
        tx = web3.eth.get_transaction(tx_hash)

        # Convert HexBytes and bytes to hex strings for JSON
        tx_dict = {}
        for k, v in tx.items():
            if isinstance(v, (bytes, bytearray)):
                tx_dict[k] = v.hex()
            else:
                tx_dict[k] = v

        return tx_dict

    except Exception as e:
        return {"error": str(e)}

