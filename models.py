from sqlalchemy import Integer, String, Date, Column, ForeignKey, UniqueConstraint, PrimaryKeyConstraint
from db import Base

# Flight model
class Flight(Base):
    __tablename__ = 'flight'

    flight_id = Column(Integer, primary_key=True)
    from_location = Column(String, nullable=False)
    to_location = Column(String, nullable=False)
    schedule = Column(String)
    __table_args__ = (UniqueConstraint('from_location', 'schedule', name='flight_schedule'),
                      UniqueConstraint('to_location', name='to'),)
