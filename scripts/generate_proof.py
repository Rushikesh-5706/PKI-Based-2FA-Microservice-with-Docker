import base64
import sys
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from app.crypto_utils import sign_commit_pss

def generate_proof(commit_hash):
    signature = sign_commit_pss(commit_hash)
    with open("instructor_public.pem", "rb") as f:
        instr_pub = serialization.load_pem_public_key(f.read())
    encrypted_sig = instr_pub.encrypt(
        signature,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    print(base64.b64encode(encrypted_sig).decode('utf-8'))

if __name__ == "__main__":
    generate_proof(sys.argv[1])
