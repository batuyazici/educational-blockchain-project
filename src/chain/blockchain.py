'''
usage           : python blockchain.py
                  python blockchain.py -p 5000
                  python blockchain.py --port 5000
'''
from ecdsa import VerifyingKey, SECP256k1
from ecdsa.util import sigdecode_der
from ecdsa import VerifyingKey
from ecdsa.util import sigdecode_der
from collections import OrderedDict
import binascii
import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4
import requests
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS



miningSender = "COINBASE"
miningReward = 1
miningDifficulty = 2


class Blockchain:
    def __init__(self, port):
        self.transactions = []
        self.chain = []
        self.nodes = set()
        self.node_id = str(uuid4()).replace('-', '')
        self.createBlock(0, '00')  # Genesis block

        if port == 5000:
            # Add two more blocks with hardcoded transactions for demonstration
            self.submitTransaction("", miningSender, "1JStJkbYYHt6EYvwJX9vwaQg5g45BHH8Ca", miningReward, "")
            self.createBlock(self.proofOfWork(), self.hash(self.chain[-1]))

            self.submitTransaction("", miningSender, "1JadFvSuXJ4Yoq1SNNRfCNHjpag2QH8Rm8", miningReward, "")
            self.createBlock(self.proofOfWork(), self.hash(self.chain[-1]))



    def registerNode(self, nodeUrl):
        """
        Add a new node to the list of nodes
        """
        #Checking nodeUrl has valid format
        parsedUrl = urlparse(nodeUrl)
        if parsedUrl.netloc:
            self.nodes.add(parsedUrl.netloc)
        elif parsedUrl.path:
            # Accepts an URL without scheme like '192.168.0.5:5000'.
            self.nodes.add(parsedUrl.path)
        else:
            raise ValueError('Invalid URL')


    def verifyTransactionSignature(self, senderPublicKey, signature, transaction):
        """
        Verify the transaction signature using ECDSA
        """
        try:
            # Decode the public key from hex format
            publicKey = VerifyingKey.from_string(bytes.fromhex(senderPublicKey), curve=SECP256k1)

            # Create a SHA-256 hash of the transaction
            transactionHash = hashlib.sha256(str(transaction).encode('utf-8')).digest()

            # Verify the signature
            return publicKey.verify(binascii.unhexlify(signature), transactionHash, sigdecode=sigdecode_der)
            
        except Exception as e:
            print("Verification failed:", e)
            return False


    #blockchain.submitTransaction(senderPublicKey,senderAddress, recipientAddress, amount, signature)
    def submitTransaction(self,senderPublicKey, senderAddress, recipientAddress, amount, signature):
        """
        Add a transaction to transactions array if the signature verified
        """
        amount= float(amount)
        transaction = OrderedDict({ 
                                    'senderPublicKey': senderPublicKey,
                                    'senderAddress': senderAddress, 
                                    'recipientAddress': recipientAddress,
                                    'amount': amount,
                                    })

        #Reward for mining a block
        if senderAddress == miningSender:
            self.transactions.append(transaction)
            return len(self.chain) + 1
        #Manages transactions from wallet to another wallet
        else:
            transaction_verification = self.verifyTransactionSignature(senderPublicKey, signature, transaction)
            if transaction_verification:
                self.transactions.append(transaction)
                return len(self.chain) + 1
            else:
                return False


    def createBlock(self, nonce, previousHash):
        """
        Add a block of transactions to the blockchain
        """
        # Ensure that transactions are exactly as they were added
        # This list comprehension creates a deep copy of each OrderedDict in self.transactions
        transactions_copy = [OrderedDict(transaction) for transaction in self.transactions]

        # Constructing the block with the transactions
        block = {
            'blockNumber': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': transactions_copy,
            'nonce': nonce,
            'previousHash': previousHash
        }

        # Print the transactions being added to the block for verification
        print(f'Creating Block: {block["blockNumber"]}, Transactions: {transactions_copy}')

        # Reset the current list of transactions
        self.transactions = []

        # Append the new block to the chain
        self.chain.append(block)
        return block



    def hash(self, block):
        """
        Create a SHA-256 hash of a block
        """
        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        blockString = json.dumps(block, sort_keys=True).encode()
        
        return hashlib.sha256(blockString).hexdigest()


    def proofOfWork(self):
        """
        Proof of work algorithm
        """
        lastBlock = self.chain[-1]
        lastHash = self.hash(lastBlock)

        nonce = 0
        while self.validationProof(self.transactions, lastHash, nonce) is False:
            nonce += 1

        return nonce


    def validationProof(self, transactions, lastHash, nonce, difficulty=miningDifficulty):
        """
        Check if a hash amount satisfies the mining conditions. This function is used within the proofOfWork function.
        """
        formatted_transactions = [OrderedDict(sorted(transaction.items())) for transaction in transactions]
        guess = (str(formatted_transactions) + str(lastHash) + str(nonce)).encode('utf-8')
        guess_hash = hashlib.sha256(guess).hexdigest()
        print(f'Validation Proof: Transactions: {transactions}, LastHash: {lastHash}, Nonce: {nonce}, Guess Hash: {guess_hash}')
        return guess_hash[:difficulty] == '0' * difficulty
        




    def validationChain(self, chain):
        """
        check if a blockchain is valid
        """
        lastBlock = chain[0]
        currentIndex = 1

        while currentIndex < len(chain):
            # Print transactions at validation
            block = chain[currentIndex]

            print(f'Validating Block: {block["blockNumber"]}, Transactions: {block["transactions"]}')

            print(f'Validating Block: {currentIndex}, Previous Hash: {block["previousHash"]}, Current Hash: {self.hash(lastBlock)}')

            # Check that the hash of the block is correct
            if block['previousHash'] != self.hash(lastBlock):
                print('Invalid chain: Hash mismatch')
                return False
            transaction_elements = ['senderPublicKey', 'senderAddress', 'recipientAddress', 'amount']
            # Filter the transactions where recipient address is not 'COINBASE'
            non_coinbase_transactions = [tx for tx in block['transactions'] if tx.get('senderAddress') != 'COINBASE']

            if non_coinbase_transactions:
                # If there are non-'COINBASE' transactions, use them for validation
                formatted_transactions = [OrderedDict((k, tx[k]) for k in transaction_elements if k in tx) for tx in non_coinbase_transactions]
                if not self.validationProof(formatted_transactions, block['previousHash'], block['nonce'], miningDifficulty):
                    print('Invalid chain: Proof of Work failed')
                    return False
            else:
                # If there are no non-'COINBASE' transactions, use the standard method
                transactions = [OrderedDict((k, tx[k]) for k in transaction_elements if k in tx) for tx in block['transactions']]
                if not self.validationProof(transactions, block['previousHash'], block['nonce'], miningDifficulty):
                    print('Invalid chain: Proof of Work failed')
                    return False

            lastBlock = block
            currentIndex += 1

        print('Chain is valid')
        return True

    def resolveConflicts(self):
        """
        Resolve conflicts between blockchain's nodes
        by replacing our chain with the longest one in the network.
        """
        neighbours = self.nodes
        newChain = None

        # We're only looking for chains longer than ours
        maxLength = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            print('http://' + node + '/chain')
            response = requests.get('http://' + node + '/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > maxLength and self.validationChain(chain):
                    maxLength = length
                    newChain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if newChain:
            self.chain = newChain
            return True

        return False


# Instantiate the Node
app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('./index.html')

@app.route('/configure')
def configure():
    return render_template('./configure.html')



@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.form

    # Check that the required fields are in the POST'ed data
    required = ['senderPublicKey', 'senderAddress', 'recipientAddress', 'amount', 'signature']
    if not all(k in values for k in required):
        return jsonify({'message': 'Missing values','required':required,'values':values}), 400

    # Extracting transaction details
    senderPublicKey = values['senderPublicKey']
    senderAddress = values['senderAddress']
    recipientAddress = values['recipientAddress']
    amount = values['amount']
    signature = values['signature']

    # Submit the transaction to the blockchain
    transaction_result = blockchain.submitTransaction(senderPublicKey,senderAddress, recipientAddress, amount, signature)

    if transaction_result == False:
        response = {'message': 'Invalid Transaction!','values':values}
        return jsonify(response), 406
    else:
        response = {'message': 'Transaction will be added to Block ' + str(transaction_result)}
        return jsonify(response), 201

@app.route('/transactions/get', methods=['GET'])
def get_transactions():
    #Get transactions from transactions pool
    transactions = blockchain.transactions

    response = {'transactions': transactions}
    return jsonify(response), 200

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/mine', methods=['GET'])
def mine():
    # We run the proof of work algorithm to get the next proof...
    lastBlock = blockchain.chain[-1]
    nonce = blockchain.proofOfWork()

    # We must receive a reward for finding the proof.
    # Adding an empty string for senderPublicKey as it's a mining reward
    blockchain.submitTransaction(senderPublicKey="", 
                                  senderAddress=miningSender, 
                                  recipientAddress=blockchain.node_id, 
                                  amount=miningReward, 
                                  signature="")

    # Forge the new Block by adding it to the chain
    previousHash = blockchain.hash(lastBlock)
    block = blockchain.createBlock(nonce, previousHash)

    response = {
        'message': "New Block Forged",
        'blockNumber': block['blockNumber'],
        'transactions': block['transactions'],
        'nonce': block['nonce'],
        'previousHash': block['previousHash'],
    }
    return jsonify(response), 200




@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.form
    nodes = values.get('nodes').replace(" ", "").split(',')

    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.registerNode(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': [node for node in blockchain.nodes],
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolveConflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'newChain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }
    return jsonify(response), 200


@app.route('/nodes/get', methods=['GET'])
def get_nodes():
    nodes = list(blockchain.nodes)
    response = {'nodes': nodes}
    return jsonify(response), 200



if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port


    # Instantiate the Blockchain
    blockchain = Blockchain(port)
    app.run(host='127.0.0.1', port=port, debug=True)