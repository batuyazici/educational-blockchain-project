from ecdsa import SigningKey, VerifyingKey, SECP256k1
from ecdsa.util import sigencode_der, sigdecode_der
import hashlib
import binascii
from collections import OrderedDict

# Provided Key Pair in Hex Format
private_key_hex = "5b6d8849570bf7447fcb85d48cb15219134eca8825f76bf3ed19f2cc37b89d52"
public_key_hex = "ed56dd4d02f8ab7e088ed63b3b77a82f33c7241b543aab240a58ef8faa289b7d74ac690911cc5d0029615ad93205a9e0e437d53c8f698139cc35c6dd6daff1e5"

# Convert Hex Strings to Key Objects
private_key = SigningKey.from_string(bytes.fromhex(private_key_hex), curve=SECP256k1)
public_key = VerifyingKey.from_string(bytes.fromhex(public_key_hex), curve=SECP256k1)

# Transaction Data
transaction = OrderedDict({
    'sender_address': 'sender123',
    'recipient_address': 'recipient456',
    'amount': 100
})

# Sign Transaction
def sign_transaction(private_key, transaction):
    transaction_hash = hashlib.sha256(str(transaction).encode('utf-8')).digest()
    signature = private_key.sign_deterministic(transaction_hash, sigencode=sigencode_der)
    return binascii.hexlify(signature).decode('ascii')

# Verify Signature
# Verify Signature
def verify_transaction_signature(public_key, signature, transaction):
    try:
        transaction_hash = hashlib.sha256(str(transaction).encode('utf-8')).digest()
        verification_result = public_key.verify(binascii.unhexlify(signature), transaction_hash, sigdecode=sigdecode_der)
        return verification_result, None  # Return None if no error
    except Exception as e:
        return False, str(e)  # Return False and the error message if an exception occurs


# Test Signing and Verification
signature = sign_transaction(private_key, transaction)
verification_result, error = verify_transaction_signature(public_key, signature, transaction)

print("Signature:", signature)
print("Verification Result:", verification_result)
if not verification_result:
    print("Error:", error)
