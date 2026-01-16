import requests
import sys

def request_seed(student_id, repo_url):
    api_url = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws"
    with open("student_public.pem", "r") as f:
        public_key = f.read()
    payload = {
        "student_id": student_id,
        "github_repo_url": repo_url,
        "public_key": public_key
    }
    response = requests.post(api_url, json=payload)
    data = response.json()
    if data.get("status") == "success":
        with open("encrypted_seed.txt", "w") as f:
            f.write(data["encrypted_seed"])
        print("Success: encrypted_seed.txt created.")
    else:
        print(f"Error: {data}")

if __name__ == "__main__":
    request_seed(sys.argv[1], sys.argv[2])
