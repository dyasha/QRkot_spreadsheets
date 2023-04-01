from aiogoogle import Aiogoogle

from app.core.config import settings
from app.core.google_client import (generate_spreadsheet_body,
                                    generate_table_values)

ROW_COUNT = 100
COLUMN_COUNT = 3


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = await generate_spreadsheet_body(
        locale='ru_RU',
        sheet_title='Лист1',
        row_count=ROW_COUNT,
        column_count=COLUMN_COUNT
    )
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheet_id = response['spreadsheetId']
    return spreadsheet_id


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheet_id: str,
        projects: list,
        wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = await generate_table_values(
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание'])

    for pro in projects:
        date = pro['close'] - pro['open']
        new_row = [str(pro['name']),
                   str(date),
                   str(pro['description']), 1]
        table_values.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    num_rows = len(table_values) + len(projects)
    num_col = len(new_row)
    if num_rows <= ROW_COUNT and num_col <= COLUMN_COUNT:
        await wrapper_services.as_service_account(
            service.spreadsheets.values.update(
                spreadsheetId=spreadsheet_id,
                range=f'A1:C{len(table_values) + len(projects)}',
                valueInputOption='USER_ENTERED',
                json=update_body
            )
        )
    else:
        raise ValueError(f'Данные не помещаются в таблице ({num_rows} строк, '
                         f'{num_col} столбцов.)')
