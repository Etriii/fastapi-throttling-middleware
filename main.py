from fastapi import FastAPI, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from redis import Redis
app = FastAPI()

# Connect to Redis running in WSL using the URI connection format
redis_uri = "redis://127.0.0.1:6379/0"  # Redis URI (localhost:6379 and database 0)

# Create the Limiter using Redis
limiter = Limiter(key_func=get_remote_address, storage_uri=redis_uri)

# Uncomment this if you dont want to use redis and comment the code above
# limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Mock function to get logged-in user ID (use a real auth system in production)
"""
If X-User-ID is NOT Provided:
    The function will fall back to using the IP address by calling get_remote_address(request)
"""


def get_user_id_key(request: Request):
    result = request.headers.get("X-User-ID", get_remote_address(request))
    print(result)
    return result


# --- ENDPOINTS ---


# 1️⃣ Per-user limit for OTP
@app.get("/send-otp")
@limiter.limit("2/minute", key_func=get_user_id_key)  # 2 requests per minute per user
async def send_otp(request: Request):
    """2 requests per minute per user"""
    return {"message": "OTP sent!"}


# 2️⃣ Per-IP limit for search
@app.get("/search")
@limiter.limit(
    "5/minute", key_func=get_remote_address
)  # 5 requests per minute per IP
async def search(request: Request):
    """5 requests per minute per IP"""
    return {"message": "Search done!"}


# 3️⃣ Global limit for all requests (by user or IP)
@app.get("/any-endpoint")
@limiter.limit("10/hour")  # 10 requests per hour for any user or IP
async def any_endpoint(request: Request):
    """Global limit for all requests (by user or IP)"""
    return {"message": "This has a global limit too"}


# You can even stack decorators to make:
"""
    @limiter.limit("5/minute", key_func=get_user_id_key)  # per user
    @limiter.limit("20/minute", key_func=get_remote_address)  # per IP

this can limit the requests and make sure that even if you change a user
    you still cannot request another one if you reach the limit. 
    
    Unless if you changed your ip :>
"""

# Example: /search → per IP (5/min) + per User (2/minute)
@app.get("/search2")
@limiter.limit("2/minute", key_func=get_user_id_key)# 2/minute limit per user
@limiter.limit("5/minute", key_func=get_remote_address)# 5/minute limit per ip
async def search(request: Request, q: str = ""):
    """2/minute limit per user and 5/minute limit per ip"""
    return {"message": f"Search results for '{q}'"}
