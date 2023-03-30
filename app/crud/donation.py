from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.donation import Donation


class CRUDDonation(CRUDBase):
    async def get_all_donations_for_user(
        self,
        session: AsyncSession,
        user_id: int,
    ) -> Optional[List]:
        donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user_id
            )
        )
        donations = donations.scalars().all()
        return donations


donation_crud = CRUDDonation(Donation)