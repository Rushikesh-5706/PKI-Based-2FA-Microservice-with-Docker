# PKI-Based 2FA Microservice

## Student Information

- **Name:** Rushikesh
- **Student ID:** 23MH1A4930
- **GitHub Repository:** https://github.com/Rushikesh-5706/PKI-Based-2FA-Microservice-with-Docker.git
- **Docker Image URL:** https://hub.docker.com/r/rushi5706/pki-based-2fa-microservice
## Student Public Key (RSA 4096-bit)
-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEA0XC1F77kB7Ke/VhzuXON
QMNIW7tcKs/8vaGrFAh4VIwHDtB6I/gvzIMtFjlCZeWeB5Gl9zc8R9bZFxFOIF8M
INl2U2WHionJYAzJ+mjkzdoYyC9Frx7gfruw8f5tLiSS+lVuqGSM1zZUmZXOm7IJ
5L3SNakZvIlTr2wBNiMdYY+sTdJn85XN8C1Em0MX2hlJm9LKsaxxmVXMCJJtsZgZ
Ms2cVsyDAPJzMSJbx8UOyTh6ZyFNc9EDviNWtMwc1Ue1DiwpRb/YCOFm76O5NaF/
OI4SaKO2efI/EsAkkw16aJXdUCJbc/A4Btb6SfECU2GQ9Y/OVjQkNIAYScFq7w+8
ikESz7tYqhmF97uMRX7YWAHQenDlVKffU+CFE30XlIFFuX9IF8PvIIp3IUE2F7U1
U8CoURFut028zdScEMyGoNp1ScmGDapcev19wzD/gxOA806sJ5Yk1GTFXokPdNgy
LEgb6RBU6J6zJqAekRfYUIavrh1HabHK4cLEM5+IrbuOB53cOBV3Fw3/Ovfb4Q0k
71MUBkEpkScRrV1I5d+FRhcrGWd4u2K3UuboynaUDM2ksvcYhuwAiNS5VnpppLhA
v5FQ1eqQd3eDf1hLihxosbkJBIIUplT//c8vT8sJ1QZJma0W/jL8nOwnUU9drlKj
xklLfg1KXQu+Bk8vHEChXqMCAwEAAQ==
-----END PUBLIC KEY-----

## Project Overview
This microservice implements a secure, containerized authentication system utilizing Public Key Infrastructure (PKI) and Time-based One-Time Password (TOTP) protocols. The system is engineered to handle cryptographic key management, persistent data storage across container lifecycles, and automated background task scheduling.

## Technical Implementation

- **Cryptographic Specifications:** RSA 4096-bit keys with public exponent 65537.
- **Asymmetric Encryption:** RSA/OAEP utilizing SHA-256 hash algorithm and MGF1.
- **Digital Signatures:** RSA-PSS with SHA-256 and maximum salt length for commit verification.
- **TOTP Protocol:** SHA-1 algorithm, 30-second time intervals, and 6-digit code generation.
- **System Environment:** UTC (Coordinated Universal Time) is enforced for all internal logs, timestamps, and API responses to ensure global synchronization.

## Infrastructure and Persistence
The service utilizes a multi-stage Docker build to optimize image security and size. Data integrity is maintained via Docker named volumes mounted at `/data` (for seed persistence) and `/cron` (for background logging). The cron configuration is optimized with LF line endings and explicit environment variable injection to ensure reliable execution in the Linux-based container environment.

---

## Evaluation Walkthrough

To verify the microservice against all technical requirements, please execute the following sequence:

### 1. Container Deployment
Pull the production image and launch the containerized environment:

```bash
docker pull rushi5706/pki-based-2fa-microservice:latest
docker run -d --name pki-2fa-app -p 8080:8080 -e TZ=UTC rushi5706/pki-based-2fa-microservice:latest
```

### 2. Secure Seed Decryption
Initialize the service by submitting the RSA-encrypted seed. The service will decrypt this using the student private key and store it in the persistent volume.

```bash
curl -X POST http://localhost:8080/decrypt-seed \
  -H "Content-Type: application/json" \
  -d '{"encrypted_seed": "B3xCkxwJ+fBWOTwGV2QEUdBDpO+0G20+MQiXJm/JvMsGq9ojM7d8Wg540OBSL93gFR7VdGLT8LSopnaT1ncYBO7E+SthqvkUh6DBKar7/paZlaDeK7KCzET45+mkwdfHTNL0eM1+774BSoCBeyo2UKKzc5hUThbhdqm3qnt4hyh4uX+QMJUB9mgrB5BZPuo3J36z3F/5yCB47nxwmpiFIgn9Z9zfZE8Mjo0V3UWX+HwgPtVw1yBZTEAmoCX4KnmpVhzZu1KMomtn3L0WlonPWTORF8FbeHJ2DEAOyy4kAtimvZ5QBR4bbuHaG4XJ7N17LaDwr/xUak8Gl3h/4zicRUE9sA9qEEw5jG84rhMjsPIWFx9pG+H75CpRRNdgogY4vOtWTXdxv5W9SnXWFTmv2CsCcPqW42IdiapLIqANYAb5FnihQZ2ck7X71OveH2CBDWzVLdSdnW+2Qm3hfk2gwReiBsSVosK1v4KhB2OyEmrfvDYYpizuiscJ34o3K3w38uu2/qb+KIpR3wLvC457xVzoLexlbaqZyGAz9jdJrr7OZhjDP89ye3WcRUJ1WYZ6Qdl28I+0Kr4Ua/IirTP9ApfCE2XaWE3gJLph6Z/cQnuD3vYvW6xKrh/wVCUCZBasBRagUYuHhCtRbR3/ZNExTWnLudWbwG7gC6b9UuSi1Ck="}'
  ```
  
### 3. Verification of Background Cron Job
Note: The cron daemon triggers on the start of every minute (00 seconds). After calling /decrypt-seed, please wait at least 65 seconds to allow the first cron cycle to complete before checking the log.

```bash
docker exec pki-2fa-app cat /cron/last_code.txt
  ```

### 4. Verification of Persistence
Restart the container to verify that the decrypted seed survives in the Docker volume:

```bash
docker restart pki-2fa-app
curl http://localhost:8080/generate-2fa
  ```

---

## Cryptographic Proof of Work

Note on Cryptographic Proof: The Commit Hash and Encrypted Signature for this specific submission are provided directly in the evaluation portal to ensure absolute synchronization with the final repository state.

---
