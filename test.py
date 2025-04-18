import requests

# The code to verify
code_to_verify = "3537"

# Flask server URL
url = "http://127.0.0.1:5000//verify_and_display"

# Send the code as a POST request
response = requests.post(url, json={'code': code_to_verify})

# Handle the response
if response.status_code == 200:
    print("Code verified successfully!")
elif response.status_code == 401:
    print("Invalid code!")
else:
    print(f"Error: {response.json().get('message')}")