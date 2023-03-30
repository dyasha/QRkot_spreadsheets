from sqlalchemy import Column, String, Text

from app.core.db import AbstractModel, Base


class CharityProject(Base, AbstractModel):
    """Модель проекта."""
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)