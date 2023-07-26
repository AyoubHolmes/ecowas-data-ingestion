from sqlalchemy import Column, Integer, String, Float, Sequence, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Country(Base):
    __tablename__ = "country"

    id = Column(Integer, primary_key=True)
    label = Column(String, nullable=False)


class Kpi(Base):
    __tablename__ = "kpi"

    id = Column(Integer, primary_key=True)
    label = Column(String, nullable=False)
    parentId = Column(
        Integer,
        ForeignKey(
            "kpi.id", onupdate="CASCADE", ondelete="CASCADE", name="fk_kpi_parent"
        ),
        nullable=False,
    )


class KpiValue(Base):
    __tablename__ = "kpi_value"

    id = Column(
        Integer, Sequence("kpi_value_id_seq", start=1, increment=1), primary_key=True
    )
    kpiId = Column(
        Integer,
        ForeignKey(
            "kpi.id", onupdate="CASCADE", ondelete="CASCADE", name="fk_kpi_value_kpi"
        ),
        nullable=False,
    )
    countryId = Column(
        Integer,
        ForeignKey(
            "country.id",
            onupdate="CASCADE",
            ondelete="CASCADE",
            name="fk_kpi_value_country",
        ),
        nullable=False,
    )
    baseline = Column(Float, nullable=False)
    latestValue = Column(Float, nullable=False)
    targetLatestValue = Column(Float, nullable=False)
    target2030 = Column(Float, nullable=False)
    progressMade = Column(Float, nullable=False)
    distanceToTarget = Column(Float, nullable=False)
    directionGoodPerformance = Column(Float, nullable=False)
    ranking = Column(Float, nullable=False)
