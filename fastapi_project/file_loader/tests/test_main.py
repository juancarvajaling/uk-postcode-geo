import csv
import io
import os

from fastapi import status

from .conftests import (client, file_without_column_names,
                        file_without_content, right_file,
                        file_only_column_names, file_with_wrong_rows,
                        file_multiple_errors, file_no_postcodes)

POSTCODE_URL = os.environ.get('POSTCODE_URL')
DJANGO_PROJECT_URL = os.environ.get('DJANGO_PROJECT_URL')


def test_right_request(requests_mock, client, right_file):
    requests_mock.get(
        POSTCODE_URL,
        json={'status': 200, 'result': [{'postcode': 'MT 900'}]},
    )
    requests_mock.post(
        f'{DJANGO_PROJECT_URL}/api/postcode/postcodes/',
        json={'id': 1},
    )
    requests_mock.post(
        f'{DJANGO_PROJECT_URL}/api/postcode/coordinates/',
        status_code=status.HTTP_201_CREATED,
    )
    # to avoid mock this endpoint
    requests_mock.post('/postcode-geo', real_http=True)

    file_name, expected_response = right_file
    data = {'file': (file_name, open(file_name, 'rb'))}
    res = client.post('/postcode-geo', files=data)

    assert res.status_code == status.HTTP_200_OK
    assert res.json() == expected_response


def test_wrong_column_names(requests_mock, client, file_without_column_names):
    requests_mock.get(
        POSTCODE_URL,
        json={'status': 200, 'result': [{'postcode': 'MT 900'}]},
    )
    requests_mock.post(
        f'{DJANGO_PROJECT_URL}/api/postcode/postcodes/',
        json={'id': 1},
    )
    requests_mock.post(
        f'{DJANGO_PROJECT_URL}/api/postcode/coordinates/',
        status_code=status.HTTP_201_CREATED,
    )
    # to avoid mock this endpoint
    requests_mock.post('/postcode-geo', real_http=True)

    file_name, expected_response = file_without_column_names
    data = {'file': (file_name, open(file_name, 'rb'))}
    res = client.post('/postcode-geo', files=data)

    assert res.status_code == status.HTTP_200_OK
    assert res.json() == expected_response


def test_no_content(requests_mock, client, file_without_content):
    # to avoid mock this endpoint
    requests_mock.post('/postcode-geo', real_http=True)

    file_name, expected_response = file_without_content
    data = {'file': (file_name, open(file_name, 'rb'))}
    res = client.post('/postcode-geo', files=data)

    assert res.status_code == status.HTTP_200_OK
    assert res.json() == expected_response


def test_only_column_names(requests_mock, client, file_only_column_names):
    # to avoid mock this endpoint
    requests_mock.post('/postcode-geo', real_http=True)

    file_name, expected_response = file_only_column_names
    data = {'file': (file_name, open(file_name, 'rb'))}
    res = client.post('/postcode-geo', files=data)

    assert res.status_code == status.HTTP_200_OK
    assert res.json() == expected_response


def test_wrong_rows(requests_mock, client, file_with_wrong_rows):
    requests_mock.get(
        POSTCODE_URL,
        json={'status': 400, 'error': 'Invalid longitude/latitude submitted'},
    )
    # to avoid mock this endpoint
    requests_mock.post('/postcode-geo', real_http=True)

    file_name, expected_response = file_with_wrong_rows
    data = {'file': (file_name, open(file_name, 'rb'))}
    res = client.post('/postcode-geo', files=data)

    assert res.status_code == status.HTTP_200_OK
    assert res.json() == expected_response


def test_no_postcode(requests_mock, client, file_no_postcodes):
    requests_mock.get(
        POSTCODE_URL,
        json={'status': 200, 'result': None},
    )
    # to avoid mock this endpoint
    requests_mock.post('/postcode-geo', real_http=True)

    file_name, expected_response = file_no_postcodes
    data = {'file': (file_name, open(file_name, 'rb'))}
    res = client.post('/postcode-geo', files=data)

    assert res.status_code == status.HTTP_200_OK
    assert res.json() == expected_response


def test_multiple_errors(requests_mock, client, file_multiple_errors):
    requests_mock.get(
        POSTCODE_URL,
        json={'status': 400, 'error': 'Invalid longitude/latitude submitted'},
    )
    # to avoid mock this endpoint
    requests_mock.post('/postcode-geo', real_http=True)

    file_name, expected_response = file_multiple_errors
    data = {'file': (file_name, open(file_name, 'rb'))}
    res = client.post('/postcode-geo', files=data)

    assert res.status_code == status.HTTP_200_OK
    assert res.json() == expected_response


def test_invalid_file(client):
    file_name = './file_loader/tests/invalid_csv_file.jpg'
    expected_response = {'message': 'The file could not be read'}
    data = {'file': (file_name, open(file_name, 'rb'))}
    res = client.post('/postcode-geo', files=data)

    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert res.json() == expected_response
