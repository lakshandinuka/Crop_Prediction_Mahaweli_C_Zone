from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, Text
from sqlalchemy.sql import func

from ..db import Base


class Crop(Base):
    __tablename__ = 'crops'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    scientific_name = Column(String(180), nullable=True)
    crop_type = Column(String(80), nullable=True)
    zone = Column(String(120), nullable=True)
    season = Column(String(80), nullable=True)
    description = Column(Text, nullable=True)
    growth_duration_days = Column(Integer, nullable=True)
    is_verified = Column(Boolean, default=False)
    source_note = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class CropGrowthStage(Base):
    __tablename__ = 'crop_growth_stages'

    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(Integer, nullable=False)
    stage_name = Column(String(80), nullable=False)
    stage_order = Column(Integer, nullable=False)
    coefficient = Column(Float, nullable=True)
    description = Column(Text, nullable=True)


class CropCoefficient(Base):
    __tablename__ = 'crop_coefficients'

    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(Integer, nullable=False)
    growth_stage = Column(String(80), nullable=False)
    kc_value = Column(Float, nullable=False)
    source = Column(String(160), nullable=True)
    is_verified = Column(Boolean, default=False)


class CropCalendar(Base):
    __tablename__ = 'crop_calendars'

    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(Integer, nullable=False)
    season = Column(String(80), nullable=False)
    month_start = Column(Integer, nullable=False)
    month_end = Column(Integer, nullable=False)
    zone = Column(String(120), nullable=True)
    note = Column(String(255), nullable=True)


class CropCycle(Base):
    __tablename__ = 'crop_cycles'

    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(Integer, nullable=False)
    season = Column(String(80), nullable=False)
    planting_date = Column(String(30), nullable=False)
    harvest_date = Column(String(30), nullable=True)
    duration_days = Column(Integer, nullable=True)
