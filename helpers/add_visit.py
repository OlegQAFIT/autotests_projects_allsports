import requests
import json
import uuid
import base64

def login_and_create_visit(phone_number, sms_code, gym_token, attraction_id):
    LOGIN_URL = "https://xn--d1aey.xn--k1aahcehedi.xn--90ais/api/v1/token"
    CREATE_VISIT_URL = "https://xn--d1aey.xn--k1aahcehedi.xn--90ais/api/v1/visit"

    api_token = str(uuid.uuid4())
    uuid_bytes = api_token.encode('utf-8')
    base64_encoded = base64.b64encode(uuid_bytes)
    base64_string = base64_encoded.decode('utf-8')

    payload = json.dumps({
        "phone": phone_number,
        "sms_token": sms_code,
        "api_token": base64_string,
        "instance_id": base64_string
    })
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    response = requests.post(LOGIN_URL, headers=headers, data=payload)

    if response.status_code == 200:
        print('LOGIN IS OK')
    else:
        print('LOGIN IS BROKEN. SEE RESPONSE')
        print(response.json())

    payload = json.dumps({
      "token": gym_token,
      "attraction_id": attraction_id,
      "lat": 0,
      "lng": 0
    })
    headers = {
      'Authorization': 'Bearer ' + api_token,
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }

    response = requests.post(CREATE_VISIT_URL, headers=headers, data=payload)

    if response.status_code == 201:
        print('Visit is created!!!')
    else:
        print('Visit is NOT created!!! SEE RESPONSE')
        print(response.json())

def test_login_and_create_visit():
    phone_number = "+375000000088"
    sms_code = "5566"
    gym_token = "https://holder.allsports.by/s/3b8b"
    attraction_id = 14225

    login_and_create_visit(phone_number, sms_code, gym_token, attraction_id)

def test_login_and_create_visit_without_foto():
    phone_number = "+375290000999"
    sms_code = "1734"
    gym_token = "https://holder.allsports.by/s/3b8b"
    attraction_id = 14225

    login_and_create_visit(phone_number, sms_code, gym_token, attraction_id)