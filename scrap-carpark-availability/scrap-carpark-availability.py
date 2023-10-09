# Run with: python scrap-carpark-availability.py
import requests
import json

carpark_api = requests.get("https://api.data.gov.sg/v1/transport/carpark-availability")
data = carpark_api.json()

# Save the JSON data to a file
with open('carpark_data.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)

print('JSON data saved to carpark_data.json')