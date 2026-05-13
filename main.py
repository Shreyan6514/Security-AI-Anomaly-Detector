from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import time
import csv
import os

app = FastAPI(title="Shreyan's Secure Cloud E-Commerce API")

# --- DATABASE ---
# In-memory product list. All activity is logged to 'traffic_logs.csv'
products = [
    {"id": 1, "name": "Gaming Laptop", "price": 1200},
    {"id": 2, "name": "Wireless Mouse", "price": 40},
    {"id": 3, "name": "Monitor 4K", "price": 350}
]
users_db = {"student": "password60309"}

# --------------- SECURITY (Auth Setup) ------------------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Simulates verification of a JWT token for the project demo
    if token != "secret-jwt-token-val":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return "student"

# --- MONITORING MIDDLEWARE (Data Collection for AI) ---
@app.middleware("http")
async def log_traffic_to_csv(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    # Feature Extraction for the Neural Network: [StatusCode, PathLength, Duration]
    log_data = [
        response.status_code, 
        len(request.url.path), 
        round(duration, 4)
    ]
    
    # Ensure the CSV file exists and append the new entry
    file_exists = os.path.isfile("traffic_logs.csv")
    with open("traffic_logs.csv", "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["status", "path_len", "duration"]) 
        writer.writerow(log_data)
        
    return response

# ------- ENDPOINTS ---

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    if not user or form_data.password != user:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    return {"access_token": "secret-jwt-token-val", "token_type": "bearer"}

@app.get("/products")
def get_catalogue():
    return {"products": products}

@app.post("/order")
def create_order(item_id: int, user: str = Depends(get_current_user)):
    product = next((p for p in products if p["id"] == item_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
        
    return {
        "message": "Order Successful", 
        "user": user, 
        "product": product["name"],
        "timestamp": time.strftime("%H:%M:%S")
    }

@app.get("/admin/config")
def secret_data(user: str = Depends(get_current_user)):
    # A sensitive path an attacker might probe to trigger anomalies
    return {"system_status": "All systems operational", "version": "5.0.1"}