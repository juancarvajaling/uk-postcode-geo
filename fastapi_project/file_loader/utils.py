import csv
import requests


async def set_postcode_from_geo(file_name):
    with open(file_name, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                continue

            res = requests.get(
                'https://postcodes.io/postcodes',
                params={'lat': row[0], 'lon': row[1]}
            )
            print(res.json())
