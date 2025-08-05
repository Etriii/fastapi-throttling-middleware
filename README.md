# FastAPI Rate Limiting with Redis

This project demonstrates how to implement rate-limiting in a FastAPI application using Redis as the backend to track request counts for each user or IP address.

## Features:
- **Rate-Limiting**: Limits requests to 5 per minute per user or IP.
- **Redis Backend**: Stores request counts for each user/IP.
- **Global & Endpoint Specific Rate-Limiting**: Custom limits for different endpoints and global limits for all requests.
  
## Requirements:
1. **Redis**: Redis server must be installed and running.
2. **Python 3.8+**: Python version for running the application.

## Installation Instructions:

### 1. Install Redis

#### On Ubuntu (Linux):
```bash
sudo apt-get update
sudo apt-get install redis-server
```
### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Running Redis
Make sure Redis is running. You can start Redis with the following command:

On Linux/macOS:
```bash
sudo service redis-server start
```

On Windows (Using WSL):
If you're using WSL, you can run Redis by executing:
```bash
redis-server
```

check if redis is working by running: 
```bash
redis-cli ping
```
It should return PONG.

### 4. Run the FastAPI Application
Start the FastAPI application with Uvicorn:
```bash
python -m uvicorn app:main --reload
```
This will start the FastAPI app on http://127.0.0.1:8000. You can visit this URL in your browser or use a tool like Postman or curl to test the endpoints.

to see documentation: http://127.0.0.1:8000/docs


### 5. Endpoints:

/send-otp: Sends an OTP (rate-limited to 5 requests per minute per user or IP).
/search: A search endpoint (rate-limited to 20 requests per minute per user or IP).
/any-endpoint: A global endpoint with a rate limit of 100 requests per hour.

You can test these endpoints by sending GET requests to them.

### 6. Test endpoints in Postman

You can import the Postman collection for testing the FastAPI throttling middleware using the following link:

[Download Postman Collection](https://github.com/Etriii/fastapi-throttling-middleware/blob/main/collection_postman.json)

### How to Import

1. Download the `.json` file from the link above.
2. Open Postman and click **Import** in the top-left corner.
3. Select the downloaded `.json` file to import the collection.

###
NOTE that:

1. Default In-Memory Store (Fallback Mechanism) in slowapi:
The slowapi library (used for rate-limiting in your FastAPI app) can work without Redis by falling back to an in-memory store.

By default, slowapi uses an in-memory dictionary to track rate limits. This means, if you haven't set up Redis, it will still track request counts for each user or IP address in memory (while the application is running).

However, there are limitations to this:

Persistence: In-memory storage is volatile, meaning that once your FastAPI server restarts, all rate limit data will be lost.

Scaling: The in-memory store is only useful for a single instance of your FastAPI app. If you scale your app across multiple servers or containers, the in-memory data will not be shared, leading to potential rate-limiting inconsistencies.