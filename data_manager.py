import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os
load_dotenv()

SHEETY_ENDPOINT = "YOUR_SHEETY_ENDPOINT"


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.sheety_username = os.getenv("SHEETY_USERNAME")
        self.sheety_password = os.getenv("SHEETY_PASSWORD")
        self.destination_data = {}

    def get_destination_data(self):
        response = requests.get(url=SHEETY_ENDPOINT,
                                auth=HTTPBasicAuth(self.sheety_username, self.sheety_password))
        response.raise_for_status()
        self.destination_data = response.json()["prices"]
        return self.destination_data

    def update_destination_codes(self):
        for row in self.destination_data:
            updated_row = {
                "price": {"iataCode": row["iataCode"]}
            }
            requests.put(url=f"{SHEETY_ENDPOINT}/{row['id']}",
                         json=updated_row,
                         auth=HTTPBasicAuth(self.sheety_username, self.sheety_password))

