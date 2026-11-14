from fastapi import FastAPI, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

SQLALCHEMY_DATABASE_URL = "sqlite:///./styleon_salon.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
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
    created_at = Column(DateTime, default=datetime.utcnow)

    customer = relationship("Customer")
    service = relationship("Service")

Base.metadata.create_all(bind=engine)

app = FastAPI(title="StyleOn Unisex Salon Management")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Auto-seed all services on startup
@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    if db.query(Service).count() == 0:
        services_data = [
            ("Hair Cut & Styling", "Normal Haircut (Trimming)", 99, "Fixed", 30),
            ("Hair Cut & Styling", "Normal Haircut (Trimming With Dryer)", 199, "Fixed", 45),
            ("Hair Cut & Styling", "Shampoo + Conditioner", 249, "Fixed", 30),
            ("Hair Cut & Styling", "Blow Dryer (With Wash)", 499, "Fixed", 45),
            ("Hair Color", "Streax", 599, "Fixed", 60),
            ("Hair Color", "Loreal (Majirel)", 799, "Fixed", 60),
            ("Hair Color", "Schwarzkopf", 999, "Fixed", 60),
            ("Hair Highlights", "Per Streak", 199, "Fixed", 30),
            ("Hair Spa", "Deep Conditioning", 499, "Fixed", 45),
            ("Hair Spa", "Loreal Spa", 799, "Fixed", 45),
            ("Hair Treatments", "Keratin", 1999, "Onwards", 120),
            ("Hair Treatments", "Smoothing", 2999, "Fixed", 120),
            ("Cleanup", "Normal Fruit Cleanup", 399, "Fixed", 45),
            ("Cleanup", "VLCC Anti Tan Cleanup", 599, "Fixed", 45),
            ("Facial", "Normal Fruit Facial", 499, "Fixed", 60),
            ("Facial", "O3+ Bridal Facial", 2499, "Fixed", 75),
            ("Bleach & D-Tan", "Fruit Bleach", 249, "Fixed", 30),
            ("Bleach & D-Tan", "D-Tan Raaga", 399, "Fixed", 30),
            ("Pedicure", "Normal Pedicure", 399, "Fixed", 45),
            ("Manicure", "Normal Manicure", 349, "Fixed", 30),
            ("Face & Threading", "Eyebrows (Threading)", 40, "Fixed", 10),
            ("Face & Threading", "Full Face Threading/Wax", 350, "Fixed", 30),
        ]
        for cat, name, price, p_type, duration in services_data:
            db.add(Service(category=cat, name=name, price=price, pricing_type=p_type, duration_mins=duration))
        db.commit()
    db.close()

@app.get("/", response_class=HTMLResponse)
def owner_dashboard(db: Session = Depends(get_db)):
    bookings = db.query(Booking).order_by(Booking.id.desc()).all()
    services = db.query(Service).all()
    
    today_str = datetime.now().strftime("%Y-%m-%d")
    today_bookings = [b for b in bookings if b.booking_date == today_str]
    
    bookings_html = ""
    for b in bookings:
        bookings_html += f"""
        <tr>
            <td>{b.id}</td>
            <td>{b.customer.name if b.customer else 'N/A'}</td>
            <td>{b.customer.mobile if b.customer else 'N/A'}</td>
            <td>{b.service.name if b.service else 'N/A'}</td>
            <td>{b.booking_date} {b.booking_time}</td>
            <td>₹{b.total_price}</td>
            <td><span style="color: green; font-weight: bold;">{b.status}</span></td>
        </tr>
        """

    services_options = ""
    for s in services:
        services_options += f"""<option value="{s.id}">{s.name} - ₹{s.price}</option>"""

    return f"""
    <!DOCTYPE html>
    <html lang="hi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>StyleOn Unisex Salon - Owner Dashboard</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f0f2f5; margin: 0; padding: 15px; color: #333; }}
            .container {{ max-width: 1000px; margin: auto; background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
            h1 {{ color: #d63384; text-align: center; margin-bottom: 5px; }}
            .info {{ background: #e8f5e9; padding: 12px; border-radius: 8px; margin-bottom: 20px; font-size: 14px; border-left: 5px solid #4caf50; }}
            .metrics {{ display: flex; gap: 15px; margin-bottom: 25px; flex-wrap: wrap; }}
            .card {{ flex: 1; background: #fff3e0; padding: 15px; border-radius: 8px; text-align: center; box-shadow: 0 2px 5px rgba(0,0,0,0.05); border-left: 4px solid #ff9800; min-width: 200px; }}
            .card h3 {{ margin: 0; font-size: 16px; color: #e65100; }}
            .card p {{ font-size: 22px; font-weight: bold; margin: 5px 0 0; color: #333; }}
            .section {{ margin-bottom: 30px; background: #fafafa; padding: 15px; border-radius: 8px; border: 1px solid #ddd; }}
            h2 {{ color: #2c3e50; font-size: 18px; margin-top: 0; border-bottom: 2px solid #d63384; padding-bottom: 5px; }}
            form {{ display: grid; gap: 10px; }}
            input, select {{ padding: 10px; border: 1px solid #ccc; border-radius: 5px; font-size: 14px; width: 100%; box-sizing: border-box; }}
            button {{ background: #d63384; color: white; border: none; padding: 12px; border-radius: 5px; font-size: 16px; cursor: pointer; font-weight: bold; }}
            button:hover {{ background: #b02a6b; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 14px; background: white; }}
            th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
            th {{ background: #d63384; color: white; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>StyleOn Unisex Salon</h1>
            <p style="text-align: center; color: #666; margin-top:0;">Pradhan Chowk, Sadh Nagar, Palam, Delhi-110045</p>
            
            <div class="info">
                📍 <strong>Location:</strong> Palam, Delhi | 🕒 <strong>Timing:</strong> 08:30 AM - 09:30 PM (All 7 Days) | 📞 <strong>Contact:</strong> 08076890631
            </div>

            <div class="metrics">
                <div class="card">
                    <h3>आज की कुल बुकिंग</h3>
                    <p>{len(today_bookings)}</p>
                </div>
                <div class="card">
                    <h3>कुल कस्टमर रिकॉर्ड</h3>
                    <p>{len(bookings)}</p>
                </div>
            </div>

            <div class="section">
                <h2>➕ नई मैनुअल बुकिंग करें</h2>
                <form action="/book" method="post">
                    <input type="text" name="customer_name" placeholder="ग्राहक का नाम (Customer Name)" required>
                    <input type="text" name="mobile" placeholder="मोबाइल नंबर (Mobile Number)" required>
                    <select name="service_id" required>
                        <option value="">-- सर्विस चुनें (Select Service) --</option>
                        {services_options}
                    </select>
                    <input type="date" name="booking_date" required>
                    <input type="time" name="booking_time" required>
                    <input type="number" name="advance_payment" placeholder="एडवांस पेमेंट (यदि कोई हो)">
                    <button type="submit">बुकिंग कन्फर्म करें (Save Booking)</button>
                </form>
            </div>

            <div class="section">
                <h2>📋 सभी बुकिंग्स की सूची (Bookings History)</h2>
                <div style="overflow-x: auto;">
                    <table>
                        <tr>
                            <th>ID</th>
                            <th>नाम</th>
                            <th>मोबाइल</th>
                            <th>सर्विस</th>
                            <th>दिनांक और समय</th>
                            <th>प्राइस</th>
                            <th>स्टेटस</th>
                        </tr>
                        {bookings_html if bookings_html else '<tr><td colspan="7" style="text-align:center;">अभी कोई बुकिंग नहीं है।</td></tr>'}
                    </table>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

@app.post("/book")
def save_booking(
    customer_name: str = Form(...),
    mobile: str,
    service_id: int = Form(...),
    booking_date: str = Form(...),
    booking_time: str = Form(...),
    advance_payment: float = Form(0.0),
    db: Session = Depends(get_db)
):
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
        
    customer = db.query(Customer).filter(Customer.mobile == mobile).first()
    if not customer:
        customer = Customer(name=customer_name, mobile=mobile, total_visits=1, last_visit=datetime.utcnow())
        db.add(customer)
        db.commit()
        db.refresh(customer)
    else:
        customer.total_visits += 1
        customer.last_visit = datetime.utcnow()
        db.commit()

    remaining = service.price - advance_payment
    p_status = "Paid" if remaining <= 0 else ("Partially Paid" if advance_payment > 0 else "Pending")
    
    new_booking = Booking(
        customer_id=customer.id,
        service_id=service.id,
        booking_date=booking_date,
        booking_time=booking_time,
        total_price=service.price,
        advance_payment=advance_payment,
        remaining_payment=max(0, remaining),
        payment_status=p_status,
        status="Confirmed"
    )
    db.add(new_booking)
    db.commit()
    
    return RedirectResponse(url="/", status_code=303)
