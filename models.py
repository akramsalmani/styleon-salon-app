from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    pricing_type = Column(String, default="Fixed")
    duration_mins = Column(Integer, default=30)
    is_active = Column(Integer, default=1)

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    mobile = Column(String, unique=True, index=True)
    total_visits = Column(Integer, default=0)
    last_visit = Column(DateTime, nullable=True)

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    service_id = Column(Integer, ForeignKey("services.id"))
    booking_date = Column(String)
    booking_time = Column(String)
    status = Column(String, default="Confirmed")
    total_price = Column(Float)
    advance_payment = Column(Float, default=0.0)
    remaining_payment = Column(Float, default=0.0)
    payment_method = Column(String, default="Cash")
    payment_status = Column(String, default="Pending")
    special_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    customer = relationship("Customer")
    service = relationship("Service")
