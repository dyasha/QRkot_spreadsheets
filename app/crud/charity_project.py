from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):
    async def get_charity_project_by_name(
        self,
        charity_project_name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        db_charity_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == charity_project_name
            )
        )
        db_charity_project_id = db_charity_project_id.scalars().first()
        return db_charity_project_id

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession,
    ):
        projects = await session.execute(
            select([CharityProject.name,
                    CharityProject.close_date.label('close'),
                    CharityProject.create_date.label('open'),
                   CharityProject.description]).where(
                CharityProject.fully_invested.is_(True)
            )
        )
        projects = projects.all()
        return projects


charityproject_crud = CRUDCharityProject(CharityProject)