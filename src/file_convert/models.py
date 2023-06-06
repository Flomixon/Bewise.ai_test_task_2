import uuid

from sqlalchemy import ForeignKey, Integer, String, Column
from sqlalchemy.dialects.postgresql import UUID

from users.models import Base, User


class Song(Base):
    __tablename__ = "song"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    user_created = Column(Integer, ForeignKey(User.id))
