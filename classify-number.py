from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import httpx

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Utility functions
def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n: int) -> bool:
    divisors_sum = sum(i for i in range(1, n) if n % i == 0)
    return divisors_sum == n

def is_armstrong(n: int) -> bool:
    digits = [int(d) for d in str(n)]
    return sum(d ** len(digits) for d in digits) == n

@app.get("/api/classify-number")
async def classify_number(number: int = Query(..., description="The number to classify")):
    if number < 0:
        raise HTTPException(status_code=400, detail="Number must be non-negative")

    # Determine properties of the number
    prime = is_prime(number)
    perfect = is_perfect(number)
    armstrong = is_armstrong(number)
    properties = [
        "prime" if prime else None,
        "perfect" if perfect else None,
        "armstrong" if armstrong else None,
        "even" if number % 2 == 0 else "odd",
    ]
    properties = [prop for prop in properties if prop is not None]
    digit_sum = sum(int(d) for d in str(number))

    # Fetch fun fact from Numbers API
    async with httpx.AsyncClient() as client:
        fun_fact_response = await client.get(f"http://numbersapi.com/{number}/math")
        fun_fact = (
            fun_fact_response.text if fun_fact_response.status_code == 200 else "No fun fact available."
        )

    return {
        "number": number,
        "is_prime": prime,
        "is_perfect": perfect,
        "properties": properties,
        "digit_sum": digit_sum,
        "fun_fact": fun_fact,
    }

# Custom error handler for validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={
            "number": request.query_params.get("number", "invalid_input"),
            "error": True,
        }
    )

# Error handling for 400 Bad Request
@app.exception_handler(HTTPException)
async def bad_request_handler(request, exc):
    if exc.status_code == 400:
        return JSONResponse(
            status_code=400,
            content={
                "number": request.query_params.get("number", "invalid_input"),
                "error": True,
            }
        )
    raise exc
