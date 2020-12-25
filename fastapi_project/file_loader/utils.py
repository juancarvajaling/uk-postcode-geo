import os
import csv
import requests

POSTCODE_URL = os.environ.get('POSTCODE_URL')
DJANGO_PROJECT_URL = os.environ.get('DJANGO_PROJECT_URL')


async def process_coordinates_file(file_name):
    '''
    Process a csv file with coordinates located in UK to obtain and save the
    related nearest postcodes. Only csv file will be proccessed and only the
    right info will be save. So the file should have the following format:
    - Only the 2 first column of the file must contain info.
    - The name of the first column must be "lat", and the second one "lon".
    - The first column must only have latitude info.
    - The second column must only have longitud info.

    Parameters:
    file_name (str): name of file to be grouped_error.

    Returns:
    List: errors found precessing the csv file.
    '''
    issues = 0
    column_names_issue = False
    errors = []
    with open(file_name, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        row_count = 1
        for row in csv_reader:
            error = process_row(row, row_count)
            row_count += 1
            if error is not None:
                errors.append(error)

    if (row_count <= 2):
        errors.append({'type': 3, 'row': row_count})

    grouped_errors = set_grouped_errors(errors)
    return grouped_errors


def process_row(row, row_count):
    '''
    Verify if the row is the first one, request the postcodes nearest to the
    readed coordinates y send the related info to Django Project.

    Parameters:
    row (List): list with the coordinate info
    row_count (int): current row precessed

    Returns:
    dict: error found processing row. The key is the type of error and value
    is the row number where it was found.
    '''
    error = None
    if row_count == 1:
        if row[0] != 'lat' or row[1] != 'lon':
            error = {'type': 1, 'row': row_count}

        return error

    res_get = requests.get(POSTCODE_URL, params={'lat': row[0], 'lon': row[1]})
    res_get = res_get.json()
    if res_get['status'] != 200:
        return {'type': 2, 'row': row_count}

    postcode_list = []
    for result in res_get['result']:
        result['code'] = result['postcode']
        res_post = requests.post(
            f'{DJANGO_PROJECT_URL}/api/postcode/postcodes/', data=result
        )
        res_post = res_post.json()
        postcode_list.append(res_post['id'])

    res_post = requests.post(
        f'{DJANGO_PROJECT_URL}/api/postcode/coordinates/',
        data={'lat': row[0], 'lon': row[1], 'postcodes': postcode_list}
    )
    return error


def set_grouped_errors(errors):
    '''
    Group a list of errors according to the following types of error:
    1: The file have wrong column names
    2: Row with wrong coordinate info.
    3: File without content.

    Parameters:
    errors (List): list of errors to be.

    Returns:
    List: list of errors grouped.
    '''
    types_error = {
        1: {'message': 'Column names are not valid', 'rows': []},
        2: {'message': 'Rows with wrong coordinates info', 'rows': []},
        3: {'message': 'File without content to be proccessed', 'rows': []}
    }
    for error in errors:
        types_error[error['type']]['rows'].append(error['row'])

    grouped_errors = []
    for i in range(1, 4):
        if types_error[i]['rows']:
            grouped_errors.append(types_error[i])

    return grouped_errors
