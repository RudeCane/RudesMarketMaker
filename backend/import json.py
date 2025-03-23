import json
import os
from web3 import Web3
from dotenv import load_dotenv
from uniswap import Uniswap  # Use `pip install uniswap-python`

# Load environment variables
load_dotenv()

# Configuration
INFURA_URL = os.getenv("INFURA_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")
USDC_ADDRESS = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"  # Example: USDC Mainnet
NATIVE_TOKEN_ADDRESS = "0xC02aaa39b223FE8D0A0e5C4F27eAD9083C756Cc2"  # Example: WETH Mainnet
UNISWAP_V3_ROUTER = "0xE592427A0AEce92De3Edee1F18E0157C05861564"  # Uniswap v3 Router

# Connect to Ethereum
w3 = Web3(Web3.HTTPProvider(INFURA_URL))

if not w3.is_connected():
    raise Exception("Failed to connect to Ethereum network")

print(f"Connected to Ethereum: {w3.is_connected()}")

# Initialize Uniswap
uniswap = Uniswap(address=WALLET_ADDRESS, private_key=PRIVATE_KEY, version=3, provider=INFURA_URL)

def get_price(token_in, token_out):
    """Fetches the latest price of token_in/token_out from Uniswap v3."""
    try:
        price = uniswap.get_price_input(token_in, token_out, 10**6)  # Query price for 1 unit (adjust decimals)
        print(f"Price of {token_in} -> {token_out}: {price}")
        return price
    except Exception as e:
        print(f"Error fetching price: {e}")
        return None

def provide_liquidity(token_a, token_b, amount_a, amount_b):
    """Adds liquidity to Uniswap v3 pool."""
    try:
        tx = uniswap.add_liquidity(token_a, token_b, amount_a, amount_b)
        print(f"Liquidity added: {tx}")
        return tx
    except Exception as e:
        print(f"Error adding liquidity: {e}")
        return None

def execute_trade(token_in, token_out, amount):
    """Swaps a given amount of token_in for token_out."""
    try:
        tx = uniswap.make_trade(token_in, token_out, amount)
        print(f"Trade executed: {tx}")
        return tx
    except Exception as e:
        print(f"Trade failed: {e}")
        return None

# Example: Market Making Strategy
def market_make():
    """Simple market-making loop."""
    amount_in = 10 * 10**6  # Adjust based on token decimals (e.g., 10 USDC)
    
    price_native_usdc = get_price(NATIVE_TOKEN_ADDRESS, USDC_ADDRESS)
    price_usdc_native = get_price(USDC_ADDRESS, NATIVE_TOKEN_ADDRESS)
    
    if price_native_usdc and price_usdc_native:
        spread = abs(price_native_usdc - (1 / price_usdc_native))
        print(f"Current spread: {spread}")

        if spread > 0.01:  # Arbitrary threshold to execute trades
            print("Executing market-making trade...")
            execute_trade(NATIVE_TOKEN_ADDRESS, USDC_ADDRESS, amount_in)
            execute_trade(USDC_ADDRESS, NATIVE_TOKEN_ADDRESS, amount_in)

# Run the market maker
if __name__ == "__main__":
    market_make()
