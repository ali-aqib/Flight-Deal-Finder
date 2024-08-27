import os
import requests
from dotenv import load_dotenv
load_dotenv()

TOKKEN_ENDPOINT = "https://test.api.amadeus.com/v1/security/oauth2/token"
IATA_CODE_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
FLIGHT_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"


class FlightSearch:
    def __init__(self):
        self._api_key = os.getenv("FLIGHT_API_KEY")
        self._api_secret = os.getenv("FLIGHT_API_SECRET_CODE")
        self._token = self._get_new_token()

    def get_destination_code(self, city):
        header = {

            "Authorization": f"Bearer {self._token}"
        }
        parameters = {
            "keyword": city,
            "max": "2",
            "include": "AIRPORTS"
        }
        response = requests.get(url=IATA_CODE_ENDPOINT, headers=header, params=parameters)
        print(f"Status code: {response.status_code}. Airport IATA: {response.text}")
        try:
            code = response.json()["data"][0]["iataCode"]
        except KeyError:
            print(f"No flight found for the {city}")
            return "N/A"
        except IndexError:
            print(f"No flight found for the {city}")
            return "Not Found"
        return code

    def _get_new_token(self):
        header = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        body = {
            "grant_type": "client_credentials",
            "client_id": self._api_key,
            "client_secret": self._api_secret,
        }

        response = requests.post(url=TOKKEN_ENDPOINT, data=body, headers=header)
        print(self._api_key, self._api_secret)
        data = response.json()
        token = data["access_token"]
        print(f"Your token is {token}")
        print(f"Your token expires in {response.json()['expires_in']}")
        return token
    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        header = {
            "Authorization": f"Bearer {self._token}"
        }
        parameters = {
            "originLocationCode": origin_city_code,
            "destinationLocationCode": destination_city_code,
            "departureDate": from_time.strftime("%Y-%m-%d"),
            "returnDate": to_time.strftime("%Y-%m-%d"),
            "adults": 1,
            "nonStop": "true",
            "currencyCode": "GBP",
            "max": "10"
        }
        response = requests.get(url=FLIGHT_ENDPOINT, headers=header, params=parameters)
        if response.status_code != 200:
            print(f"check_flights() response code: {response.status_code}")
            print("There was a problem with the flight search.\n"
                  "For details on status codes, check the API documentation:\n"
                  "https://developers.amadeus.com/self-service/category/flights/api-doc/flight-offers-search/api"
                  "-reference")
            print("Response body:", response.text)
            return None
        return response.json()
