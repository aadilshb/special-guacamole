from fastapi import FastAPI, HTTPException # type: ignore
from pydantic import BaseModel # type: ignore
import requests # type: ignore
import json

app = FastAPI()

class WhatsAppMessageRequest(BaseModel):
    body_parameters: list[str]

MOBILE_NUMBER = "YOUR_MOBILE_NUMBER" #replace with mobile number
TEMPLATE_NAME = "mini_proj"
LANGUAGE_CODE = "en_US"
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"  # Replace with your actual access token

def create_whatsapp_request(body_parameters):
    whatsapp_request_data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": MOBILE_NUMBER,
        "type": "template",
        "template": {
            "name": TEMPLATE_NAME,
            "language": {"code": LANGUAGE_CODE},
            "components": [
                {
                    "type": "body",
                    "parameters": [{"type": "text", "text": param} for param in body_parameters]
                }
            ]
        }
    }
    return whatsapp_request_data

@app.post("/send_whatsapp_message/")
async def send_whatsapp_message(request: WhatsAppMessageRequest):
    try:
        whatsapp_request_data = create_whatsapp_request(request.body_parameters)
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))

    api_url = "url"#replace with url

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.post(api_url, headers=headers, data=json.dumps(whatsapp_request_data))
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    
    return response.json()

if __name__ == "__main__":
    import uvicorn # type: ignore
    uvicorn.run(app, host="0.0.0.0", port=8000)
