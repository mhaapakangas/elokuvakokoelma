from application import db
from application.models import Base


class Genre(Base):
    __tablename__ = "genre"

    name = db.Column(db.String(144), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name
