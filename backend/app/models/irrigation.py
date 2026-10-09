from sqlalchemy import Column, DateTime, Float, Integer, String, Text
from sqlalchemy.sql import func

from ..db import Base


class IrrigationPlan(Base):
    __tablename__ = 'irrigation_plans'

    id = Column(Integer, primary_key=True, index=True)
    crop_name = Column(String(100), nullable=False)
    area_m2 = Column(Float, nullable=False)
    daily_etc_mm = Column(Float, nullable=True)
    net_irrigation_mm = Column(Float, nullable=True)
    gross_irrigation_mm = Column(Float, nullable=True)
    irrigation_efficiency = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class IrrigationEvent(Base):
    __tablename__ = 'irrigation_events'

    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, nullable=False)
    event_date = Column(String(30), nullable=False)
    depth_mm = Column(Float, nullable=False)
    volume_litres = Column(Float, nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class SavedScenario(Base):
    __tablename__ = 'saved_scenarios'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    payload = Column(Text, nullable=False)
    created_by = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AgriculturalReport(Base):
    __tablename__ = 'agricultural_reports'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(180), nullable=False)
    content = Column(Text, nullable=False)
    created_by = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AuditLog(Base):
    __tablename__ = 'audit_logs'

    id = Column(Integer, primary_key=True, index=True)
    actor_id = Column(Integer, nullable=True)
    event_type = Column(String(120), nullable=False)
    details = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
