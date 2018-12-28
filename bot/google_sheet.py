import os

import httplib2
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

from bot import constants
from bot.models import Answer


def send_to_google_sheet(user):
    CREDENTIALS_FILE = os.path.abspath(constants.cred)  # имя файла с закрытым ключом

    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                                   ['https://www.googleapis.com/auth/spreadsheets'])
    httpAuth = credentials.authorize(httplib2.Http())

    service = discovery.build('sheets', 'v4', http=httpAuth)

    spreadsheet_id = '1TBYaFsOXI5SS9yhmMVFPZCXm9WqNBp4F9aHvFd2Aues'
    range_ = 'Лист1!A:A'

    # How the input data should be interpreted.
    value_input_option = 'USER_ENTERED'  # TODO: Update placeholder value.

    # How the input data should be inserted.
    insert_data_option = 'INSERT_ROWS'  # TODO: Update placeholder value.

    value_range_body = {
        "values": [list(map(lambda answer: answer.text, Answer.objects.filter(user=user)))],
    }
    request = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, range=range_,
                                                     valueInputOption=value_input_option,
                                                     insertDataOption=insert_data_option, body=value_range_body)
    response = request.execute()
