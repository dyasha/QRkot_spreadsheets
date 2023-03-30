from datetime import datetime
from typing import List, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.models.donation import Donation


async def get_open_objects(
        model: Union[CharityProject, Donation],
        session: AsyncSession
) -> List[Union[CharityProject, Donation]]:
    open_objects = await session.execute(
        select(model).where(
            model.fully_invested.is_(False)
        )
    )
    open_objects = open_objects.scalars().all()
    return open_objects


async def close_object(
    obj: Union[CharityProject, Donation],
) -> None:
    obj.fully_invested = True
    obj.close_date = datetime.now()


async def invest_in_project(
        model: Union[CharityProject, Donation],
        session: AsyncSession
) -> Union[CharityProject, Donation]:
    model_type_map = {
        CharityProject: Donation,
        Donation: CharityProject
    }
    objects = await get_open_objects(model_type_map[type(model)], session)
    full_amount = model.full_amount
    if objects:
        for obj in objects:
            remaining_amount = obj.full_amount - obj.invested_amount
            if remaining_amount <= 0:
                continue
            investment_amount = min(remaining_amount,
                                    full_amount)
            obj.invested_amount += investment_amount
            full_amount -= investment_amount
            if obj.invested_amount == obj.full_amount:
                await close_object(obj)
            if not full_amount:
                await close_object(model)
                break
            if full_amount <= 0:
                break
            session.add(obj)
    await session.commit()
    return model
