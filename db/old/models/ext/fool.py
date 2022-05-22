from ...sql import Base
from sqlalchemy import Column, BigInteger, Integer, ARRAY


class Audition(Base):
    __tablename__ = "audition"
    __table_args__ = {"extend_existing": True, "schema": "ext_fool"}

    id = Column(Integer, primary_key=True)
    user_id: int = Column(BigInteger)
    message_id: int = Column(BigInteger)
    common: int = Column(Integer, default=0)
    scraps: int = Column(Integer, default=0)
    dont_know: int = Column(Integer, default=0)
    ng: list[int] = Column(ARRAY(BigInteger), default=[])
    pushed_member: list[int] = Column(ARRAY(BigInteger), default=[])
