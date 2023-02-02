#importing the necessary libraries
import hashlib
import json
from time import time
from uuid import uuid4
import binascii
#Defining the Blockchain class
class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        Create a new Block in the Blockchain
        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        # Reset the current list of transactions
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount, signature):
        """
        Creates a new transaction to go into the next mined Block
        :param sender: <str> Address of the Sender
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount
        :param signature: <str> Signature of the transaction
        :return: <int> The index of the Block that will hold this transaction
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            'signature': signature
        })
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block
        :param block: <dict> Block
        :return: <str>
        """
        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        """
        Simple Proof of Work Algorithm:
         - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
         - p is the previous proof, and p' is the new proof
        :param last_proof: <int>
        :return: <int>
        """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, False if not.
        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

#Defining the wallet class
class Wallet(object):
    def __init__(self):
        self.private_key = None
        self.public_key = None

    def generate_keys(self):
        """
        Generates a new pair of private and public keys
        """
        private_key = uuid4().hex
        public_key = uuid4().hex
        self.private_key = private_key
        self.public_key = public_key

    def sign_transaction(self, sender, recipient, amount):
        """
        Sign a transaction with the private key
        :param sender: <str> Address of the Sender
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount
        :return: <str> The signature
        """
        signature = self.private_key + sender + recipient + str(amount)
        return signature

    @staticmethod
    def verify_transaction(transaction):
        """
        Verify a transaction
        :param transaction: <dict> The transaction to verify
        :return: <bool> True if valid, False if not
        """
        public_key = transaction['sender']
        signature = transaction['signature']
        if public_key == signature:
            return True
        return False

# Create the Blockchain
blockchain = Blockchain()

# Create the wallet
wallet = Wallet()

# Generate a pair of keys
wallet.generate_keys()

# Create a new transaction
sender = wallet.public_key
recipient = 'Bob'
amount = 1
signature = wallet.sign_transaction(sender, recipient, amount)

# Add the transaction to the blockchain
blockchain.new_transaction(sender, recipient, amount, signature)

# Mine a new block
last_block = blockchain.last_block
last_proof = last_block['proof']
proof = blockchain.proof_of_work(last_proof)

# Forge the new Block by adding it to the chain
previous_hash = blockchain.hash(last_block)
block = blockchain.new_block(proof, previous_hash)

print('Block #{} has been added to the blockchain!'.format(block['index']))
########################################################################################################
# How can I see more output from the above?
# You can print out the contents of the block by adding the following code to the end of the program:

print(json.dumps(block, sort_keys=True, indent=4))

# How can I add more blocks?
# You can add more blocks by calling the new_block() function with the appropriate parameters. For example, to add a new block after the last one, you can use the following code:

last_block = blockchain.last_block
last_proof = last_block['proof']
proof = blockchain.proof_of_work(last_proof)
previous_hash = blockchain.hash(last_block)
block = blockchain.new_block(proof, previous_hash)

print('Block #{} has been added to the blockchain!'.format(block['index']))

print(json.dumps(block, sort_keys=True, indent=4))

# How can I see the info about block 1?
# You can print out the contents of the block by using the following code:
print('Block #1')
block_1 = blockchain.chain[0]
print(json.dumps(block_1, sort_keys=True, indent=4))
