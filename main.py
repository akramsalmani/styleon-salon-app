from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from datetime import datetime
import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="StyleOn Unisex Salon Management")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Auto-seed all 18 Salon Services on startup if empty
@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    count = db.query(models.Service).count()
    if count == 0:
        services_data = [
            ("Hair Cut & Styling", "Normal Haircut (Trimming)", 99, "Fixed", 30),
            ("Hair Cut & Styling", "Normal Haircut (Trimming With Dryer)", 199, "Fixed", 45),
            ("Hair Cut & Styling", "Shampoo + Conditioner", 249, "Fixed", 30),
            ("Hair Cut & Styling", "Blow Dryer (With Wash)", 499, "Fixed", 45),
            ("Hair Color", "Streax", 599, "Fixed", 60),
            ("Hair Color", "Loreal (Majirel)", 799, "Fixed", 60),
            ("Hair Color", "Schwarzkopf", 999, "Fixed", 60),
            ("Hair Color", "Global Hair Color - Basic", 1999, "Fixed", 90),
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
            db.add(models.Service(category=cat, name=name, price=price, pricing_type=p_type, duration_mins=duration))
        db.commit()
    db.close()

@app.get("/", response_class=HTMLResponse)
def owner_dashboard():
    return """
    <!DOCTYPE html>
    <html lang="hi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>StyleOn Unisex Salon - Owner Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; background: #f4f7f6; margin: 0; padding: 20px; }
            .container { max-width: 900px; margin: auto; background: white; padding: 25px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
            h1 { color: #d63384; text-align: center; }
            .info { background: #e2f0d9; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
            .btn { display: inline-block; background: #d63384; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin-top: 10px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>StyleOn Unisex Salon</h1>
            <div class="info">
                📍 <strong>Location:</strong> Pradhan Chowk, Sadh Nagar, Palam, Delhi - 110045<br>
                🕒 <strong>Timing:</strong> 08:30 AM - 09:30 PM (All 7 Days)<br>
                📞 <strong>Contact:</strong> 08076890631
            </div>
            <h2>🚀 Software Status: Live & Operational</h2>
            <p>आपका प्राइवेट सैलून मैनेजमेंट और बुकिंग सिस्टम सफलतापूर्वक क्लाउड पर चल रहा है!</p>
            <a class="btn" href="/docs" target="_blank">API & Booking Docs देखें</a>
        </div>
    </body>
    </html>
    """
