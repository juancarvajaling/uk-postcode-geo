import os
import csv
import requests


async def set_postcode_from_geo(file_name):
    POSTCODE_URL = os.environ.get('POSTCODE_URL')
    DJANGO_PROJECT_URL = os.environ.get('DJANGO_PROJECT_URL')
    with open(file_name, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                continue

            res_get = requests.get(
                POSTCODE_URL,
                params={'lat': row[0], 'lon': row[1]}
            )
            res_get = res_get.json()
            postcode_list = []
            for result in res_get['result']:
                result['code'] = result['postcode']
                res_post = requests.post(
                    f'{DJANGO_PROJECT_URL}/api/postcode/postcodes/',
                    data=result
                )
                res_post = res_post.json()
                postcode_list.append(res_post['id'])

            res_post = requests.post(
                f'{DJANGO_PROJECT_URL}/api/postcode/coordinates/',
                data={'lat': row[0], 'lon': row[1], 'postcodes': postcode_list}
            )
