import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.crypto_utils import decrypt_rsa_oaep
from app.totp_utils import generate_code, verify_code

app = FastAPI()
SEED_PATH = "/data/seed.txt"

class DecryptRequest(BaseModel):
    encrypted_seed: str

class VerifyRequest(BaseModel):
    code: str

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/decrypt-seed")
async def decrypt_seed_endpoint(req: DecryptRequest):
    try:
        hex_seed = decrypt_rsa_oaep(req.encrypted_seed)
        os.makedirs(os.path.dirname(SEED_PATH), exist_ok=True)
        with open(SEED_PATH, "w") as f:
            f.write(hex_seed)
        return {"status": "ok"}
    except Exception:
        raise HTTPException(status_code=500, detail="Decryption failed")

@app.get("/generate-2fa")
async def generate_2fa_endpoint():
    if not os.path.exists(SEED_PATH):
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")
    with open(SEED_PATH, "r") as f:
        seed = f.read().strip()
    code, valid_for = generate_code(seed)
    return {"code": code, "valid_for": valid_for}

@app.post("/verify-2fa")
async def verify_2fa_endpoint(req: VerifyRequest):
    if not os.path.exists(SEED_PATH):
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")
    if not req.code:
        raise HTTPException(status_code=400, detail="Missing code")
    with open(SEED_PATH, "r") as f:
        seed = f.read().strip()
    return {"valid": verify_code(seed, req.code)}
