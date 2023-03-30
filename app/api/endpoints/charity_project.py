from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_full_amount_less_invested_amount,
                                check_fully_invested, check_invested_amount,
                                check_name_duplicate, check_project_exists)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charityproject_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.investments import invest_in_project

router = APIRouter()


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_project(
    session: AsyncSession = Depends(get_async_session),
) -> List[CharityProjectDB]:
    """Получает список всех проектов."""
    charity_projects = await charityproject_crud.get_multi(session)
    return charity_projects


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
    charityproject: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProjectDB:
    """Создание проекта только для суперюзеров."""
    await check_name_duplicate(charityproject.name, session)
    new_charityproject = await charityproject_crud.create(
        charityproject,
        session)
    new_charityproject = await invest_in_project(new_charityproject, session)
    await session.refresh(new_charityproject)
    return new_charityproject


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def remove_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProjectDB:
    """Удаление проекта только для суперюзеров."""
    charity_project = await check_project_exists(
        project_id,
        session
    )
    charity_project = await check_invested_amount(
        project_id,
        session
    )
    charity_project = await charityproject_crud.remove(
        charity_project,
        session
    )
    return charity_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def partially_update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProjectDB:
    """Изменение данных только для суперюзеров."""
    charity_project = await check_project_exists(project_id, session)
    charity_project = await check_fully_invested(project_id, session)
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    if obj_in.full_amount is not None:
        await check_full_amount_less_invested_amount(
            project_id, obj_in.full_amount, session
        )
    charity_project = await charityproject_crud.update(
        charity_project, obj_in, session
    )
    return charity_project
