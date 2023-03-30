from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import AbstractModel, Base


class Donation(Base, AbstractModel):
    """Модель пожертвования."""
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)