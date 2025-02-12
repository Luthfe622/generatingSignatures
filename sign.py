import eth_account
from web3 import Web3
from eth_account.messages import encode_defunct

def sign(m):
    w3 = Web3()
    
    # Create an eth account
    account = eth_account.Account.create()
    eth_address = account.address
    private_key = account.key

    # Encode the message to be signed
    message = encode_defunct(text=m)

    # Generate signature
    signed_message = w3.eth.account.sign_message(message, private_key=private_key)

    assert isinstance(signed_message, eth_account.datastructures.SignedMessage)

    return eth_address, signed_message

# Example usage
if __name__ == "__main__":
    address, signature = sign("Hello, Ethereum!")
    print(f"Address: {address}")
    print(f"Signature: {signature}")
