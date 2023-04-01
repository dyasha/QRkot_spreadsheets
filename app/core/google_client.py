from datetime import datetime
from aiogoogle import Aiogoogle
from aiogoogle.auth.creds import ServiceAccountCreds

from app.core.config import settings

FORMAT = "%Y/%m/%d %H:%M:%S"

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

INFO = {
    'type': settings.type,
    'project_id': settings.project_id,
    'private_key_id': settings.private_key_id,
    'private_key': settings.private_key,
    'client_email': settings.client_email,
    'client_id': settings.client_id,
    'auth_uri': settings.auth_uri,
    'token_uri': settings.token_uri,
    'auth_provider_x509_cert_url': settings.auth_provider_x509_cert_url,
    'client_x509_cert_url': settings.client_x509_cert_url
}

cred = ServiceAccountCreds(scopes=SCOPES, **INFO)


async def get_service():
    async with Aiogoogle(service_account_creds=cred) as aiogoogle:
        yield aiogoogle


async def generate_spreadsheet_body(
    locale: str,
    sheet_title: str,
    row_count: int,
    column_count: int
) -> str:
    now_date_time = datetime.now().strftime(FORMAT)
    spreadsheet_body = {
        'properties': {'title': f'Отчет от {now_date_time}',
                       'locale': locale},
        'sheets': [{'properties': {'sheetType': 'GRID',
                                   'sheetId': 0,
                                   'title': sheet_title,
                                   'gridProperties': {
                                       'rowCount': row_count,
                                       'columnCount': column_count}}}]
    }
    return spreadsheet_body


async def generate_table_values(
    main_line: list,
    col_names: list
) -> list[list, list, list]:
    now_date_time = datetime.now().strftime(FORMAT)
    table_values = [['Отчет от', now_date_time],
                    main_line,
                    col_names]
    return table_values