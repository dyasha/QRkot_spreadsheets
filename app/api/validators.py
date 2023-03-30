from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charityproject_crud
from app.models.charity_project import CharityProject


async def check_name_duplicate(
    charity_project_name: str,
    session: AsyncSession
) -> None:
    charity_project_id = await charityproject_crud.get_charity_project_by_name(
        charity_project_name,
        session)
    if charity_project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST.value,
            detail='Проект с таким именем уже существует!'
        )


async def check_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    charity_project = await charityproject_crud.get(project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail='Такого проекта не существует.'
        )
    return charity_project


async def check_invested_amount(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    charity_project = await charityproject_crud.get(project_id, session)
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST.value,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
    return charity_project


async def check_fully_invested(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    charity_project = await charityproject_crud.get(project_id, session)
    if charity_project.fully_invested is True:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST.value,
            detail='Закрытый проект нельзя редактировать!'
        )
    return charity_project


async def check_full_amount_less_invested_amount(
    project_id: int,
    full_amount: int,
    session: AsyncSession,
) -> None:
    charity_project = await charityproject_crud.get(project_id, session)
    if full_amount < charity_project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY.value,
            detail='Нельзя установить требуемую сумму меньше уже вложенной.'
        )