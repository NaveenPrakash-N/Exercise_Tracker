import os
from dotenv import load_dotenv
import requests
from datetime import datetime

load_dotenv()

GENDER = 'male'
WEIGHT_KG = 61
HEIGHT_CM = 150
AGE = 21

APP_ID = os.getenv('APP_ID')
API_KEY = os.getenv('API_KEY')
AUTH_TOKEN_SHEETY = os.getenv('AUTH_TOKEN_SHEETY')

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

exercise_text = input("Tell me which exercises you did: ")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

sheety_endpoint = 'https://api.sheety.co/c51d9268e8505285d35a1959b6cab7e8/myWorkouts/sheet1'

response = requests.post(exercise_endpoint, json=parameters, headers=headers)
result = response.json()

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

for exercise in result["exercises"]:
    sheet_inputs = {
        "sheet1": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }
    sheet_header = {
        'Authorization': AUTH_TOKEN_SHEETY
    }

    sheet_response = requests.post(url=sheety_endpoint, json=sheet_inputs, headers=sheet_header)
    print(sheet_response.text)
