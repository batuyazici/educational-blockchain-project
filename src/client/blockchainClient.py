'''
usage           : python blockchainClient.py
                  python blockchainClient.py -p 8080
                  python blockchainClient.py --port 8080
'''

from ecdsa import SigningKey, SECP256k1
from ecdsa.util import sigencode_der
import hashlib
import base58
from collections import OrderedDict
import binascii
import requests
from flask import Flask, jsonify, request, render_template


class Transaction:

    def __init__(self, senderPublicKey, senderAddress, senderPrivateKey, recipientAddress, amount):
        self.senderAddress = senderAddress
        self.senderPublicKey = senderPublicKey
        self.senderPrivateKey = senderPrivateKey
        self.recipientAddress = recipientAddress
        self.amount = amount

    def toDict(self):
        return OrderedDict({
            'senderPublicKey': self.senderPublicKey,
            'senderAddress': self.senderAddress,
            'recipientAddress': self.recipientAddress,
            'amount': self.amount
        })

    def signTransaction(self):
        """
        Sign transaction with private key using ECDSA
        """
        # Decode the private key from hex format
        private_key = SigningKey.from_string(bytes.fromhex(self.senderPrivateKey), curve=SECP256k1)

        # Create a SHA-256 hash of the transaction
        transaction_hash = hashlib.sha256(str(self.toDict()).encode('utf-8')).digest()

        # Sign the transaction
        signature = private_key.sign_deterministic(transaction_hash, sigencode=sigencode_der)
        return binascii.hexlify(signature).decode('ascii')

def getFixedWallet(port):
    if port == '8080':
        return {
            'public_key': 'd3dedd55dcb298bc226f40361556d0b8569903a1919d4f03c12475a2bb17dfdb40f6b0761153d5002832c61ad98a47b1fa4642140cab5ea97409f0687b1c0703',
            'private_key': '92296adc8b08efa4d38459bcfc20871ae0a4f44dee6f7766ec70941ae0ae4dff',
            'bitcoin_address': '1JStJkbYYHt6EYvwJX9vwaQg5g45BHH8Ca',
        }
    elif port == '8081':
        return {
            'public_key': 'b9ff6504e5932328c5557c091eb4deb9264c6e9aca2a19701179f4bb5ec1f07a2d3156a130c9b0955f83a7e42bfc5c1e2bf16e2ef90db1ef599ee1d23736de11',
            'private_key': '6cd9610cb4a061c35b23c94841b52904447c27045eae728fe96cd617144c1704',
            'bitcoin_address': '1JadFvSuXJ4Yoq1SNNRfCNHjpag2QH8Rm8',
            'balance': '2'
        }
    else:
        return None

app = Flask(__name__)

@app.route('/make/transaction')
def makeTransaction():
    port = request.host.split(':')[1]
    fixedWallet = getFixedWallet(port) if port in ['8080', '8081'] else {}
    fixed_wallet_json = jsonify(fixedWallet).data.decode('utf-8')
    return render_template('makeTransaction.html', fixed_wallet=fixed_wallet_json)


@app.route('/view/transactions')
def viewTransaction():
    return render_template('./viewTransactions.html')

@app.route('/wallet/new', methods=['GET'])
def newWallet():
    # Step 0: Create a new ECDSA private key
    private_key = SigningKey.generate(curve=SECP256k1)

    # Step 1: Get the corresponding public key
    public_key = private_key.get_verifying_key().to_string()

    # Step 2: Perform SHA-256 hashing on the public key
    sha256_public_key = hashlib.sha256(public_key).digest()

    # Step 3: Perform RIPEMD-160 hashing on the result of SHA-256
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(sha256_public_key)
    ripemd160_hash = ripemd160.digest()

    # Step 4: Add version byte in front of RIPEMD-160 hash
    version_byte = b'\x00'  # Version byte for Main Network
    extended_ripemd160_hash = version_byte + ripemd160_hash

    # Step 5 and 6: Perform double SHA-256 hash on the extended RIPEMD-160 result
    sha256_n1 = hashlib.sha256(extended_ripemd160_hash).digest()
    sha256_n2 = hashlib.sha256(sha256_n1).digest()

    # Step 7: Take the first 4 bytes of the second SHA-256 hash
    address_checksum = sha256_n2[:4]

    # Step 8: Add the 4 checksum bytes at the end of extended RIPEMD-160 hash
    binary_bitcoin_address = extended_ripemd160_hash + address_checksum

    # Step 9: Convert the result into a base58 string using Base58Check encoding
    bitcoin_address = base58.b58encode(binary_bitcoin_address)

    response = {
        'private_key': private_key.to_string().hex(),
        'public_key': public_key.hex(),
        'bitcoin_address': bitcoin_address.decode('utf-8')
    }

    return jsonify(response), 200

@app.route('/generate/transaction', methods=['POST'])
def generateTransaction():
    senderPublicKey = request.form['senderPublicKey']
    senderAddress = request.form['senderAddress']
    senderPrivateKey = request.form['senderPrivateKey']
    recipientAddress = request.form['recipientAddress']
    amount = request.form['amount']

    transaction = Transaction(senderPublicKey, senderAddress, senderPrivateKey, recipientAddress, amount)

    response = {
        'transaction': transaction.toDict(),
        'signature':transaction.signTransaction()
    }   
    return jsonify(response), 200


@app.route('/balance/<address>', methods=['GET'])
def getBalance(address):
    # Send a request to blockchain.py to get the full chain
    full_chain = requests.get('http://127.0.0.1:5000/chain').json()

    # Initialize balance
    balance = 0

    # Iterate through the blockchain
    for block in full_chain['chain']:
        for transaction in block['transactions']:
            # Convert amount to an integer
            amount = float(transaction['amount'])

            # Add balance if the address is the recipient
            if transaction['recipientAddress'] == address:
                balance += amount

            # Subtract balance if the address is the sender
            if transaction['senderAddress'] == address:
                balance -= amount

    return jsonify({'balance': balance}), 200

@app.route('/')
def index():
    port = request.host.split(':')[1]
    fixedWallet = getFixedWallet(port) if port in ['8080', '8081'] else {}
    fixed_wallet_json = jsonify(fixedWallet).data.decode('utf-8')
    return render_template('index.html', fixed_wallet=fixed_wallet_json)

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=8080, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='127.0.0.1', port=port, debug=True)