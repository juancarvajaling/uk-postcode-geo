import pytest
import csv
import json
from fastapi.testclient import TestClient

from file_loader.main import app


@pytest.fixture(scope='module')
def client():
    client = TestClient(app)
    return client


@pytest.fixture(scope='module')
def right_file():
    file_name = 'postcode_geo_test.csv'
    rows = [
        ['lat', 'lon'],
        [52.923454, -1.474217],
        [53.457321, -2.262773],
        [50.871446, -0.729985]
    ]
    with open(file_name, 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerows(rows)

    expected_response = {'message': 'the file was processed successfully'}

    return file_name, expected_response


@pytest.fixture(scope='module')
def file_without_column_names():
    file_name = 'postcode_geo_test.csv'
    rows = [
        [52.923454, -1.474217],
        [53.457321, -2.262773],
        [50.871446, -0.729985]
    ]
    with open(file_name, 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerows(rows)

    expected_response = [{'message': 'Column names are not valid', 'rows': [1]}]

    return file_name, expected_response


@pytest.fixture(scope='module')
def file_without_content():
    file_name = 'postcode_geo_test.csv'
    rows = []
    with open(file_name, 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerows(rows)

    expected_response = [
        {'message': 'File without content to be proccessed', 'rows': [1]}
    ]

    return file_name, expected_response


@pytest.fixture(scope='module')
def file_only_column_names():
    file_name = 'postcode_geo_test.csv'
    rows = [['lat', 'lon']]
    with open(file_name, 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerows(rows)

    expected_response = [
        {'message': 'File without content to be proccessed', 'rows': [2]}
    ]

    return file_name, expected_response


@pytest.fixture(scope='module')
def file_with_wrong_rows():
    file_name = 'postcode_geo_test.csv'
    rows = [
        ['lat', 'lon'],
        ['hola', -1.474217],
        ['', 53.457321, -2.262773],
        ['', '']
    ]
    with open(file_name, 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerows(rows)

    expected_response = [
        {'message': 'Rows with wrong coordinates info', 'rows': [2, 3, 4]}
    ]

    return file_name, expected_response


@pytest.fixture(scope='module')
def file_no_postcodes():
    file_name = 'postcode_geo_test.csv'
    rows = [
        ['lat', 'lon'],
        [52.923454, -1.474217],
        [53.457321, -2.262773],
        [50.871446, -0.729985]
    ]
    with open(file_name, 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerows(rows)

    expected_response = [
        {'message': 'No associated postcode', 'rows': [2, 3, 4]}
    ]

    return file_name, expected_response


@pytest.fixture(scope='module')
def file_multiple_errors():
    file_name = 'postcode_geo_test.csv'
    rows = [
        ['hola', -1.474217],
        ['', 53.457321, -2.262773],
        ['', '']
    ]
    with open(file_name, 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerows(rows)

    expected_response = [
        {'message': 'Column names are not valid', 'rows': [1]},
        {'message': 'Rows with wrong coordinates info', 'rows': [2, 3]}
    ]

    return file_name, expected_response
