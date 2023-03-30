from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models.user import User
from app.schemas.donation import DonationCreate, DonationDB, DonationMeDB
from app.services.investments import invest_in_project

router = APIRouter()


@router.get(
    '/',
    response_model=List[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donation(
    session: AsyncSession = Depends(get_async_session),
) -> List[DonationDB]:
    "Список всех пожертвований только для суперюзера."
    donations = await donation_crud.get_multi(session)
    return donations


@router.post(
    '/',
    response_model=DonationMeDB,
    response_model_exclude_none=True
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
) -> DonationDB:
    """Сделать пожертвование."""
    donation = await donation_crud.create(donation, session, user)
    donation = await invest_in_project(donation, session)
    await session.refresh(donation)
    return donation


@router.get(
    '/my',
    response_model=List[DonationMeDB],
    dependencies=[Depends(current_user)],
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
) -> List[DonationMeDB]:
    donations = await donation_crud.get_all_donations_for_user(
        session, user.id
    )
    return donations