from fastapi import FastAPI, Query, HTTPException
import requests
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

# Initialize FastAPI app
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for simplicity
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception Handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """Handle validation errors for invalid inputs."""
    return JSONResponse(
        status_code=422,
        content={
            "number": request.query_params.get("number", "alphabet"),
            "error": True,
        }
    )

@app.exception_handler(HTTPException)
async def bad_request_handler(request, exc):
    """Handle HTTP exceptions for specific errors."""
    if exc.status_code == 400:
        return JSONResponse(
            status_code=400,
            content=exc.detail,  # Send the custom detail passed in the exception
        )
    raise exc

# Utility functions
def is_prime(n: int) -> bool:
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n: int) -> bool:
    """Check if a number is perfect."""
    if n < 2:
        return False
    sum_divisors = sum(i for i in range(1, n) if n % i == 0)
    return sum_divisors == n

def is_armstrong(n: int) -> bool:
    """Check if a number is an Armstrong number."""
    digits = [int(d) for d in str(n)]
    num_digits = len(digits)
    return sum(d ** num_digits for d in digits) == n

def get_fun_fact(n: int) -> str:
    """Get a fun fact about a number using the Numbers API."""
    url = f"http://numbersapi.com/{n}/math"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return "No fun fact available."

# API Endpoint
@app.get("/api/classify-number")
async def classify_number(number: int = Query(..., description="The number to classify")):
    """Classify a number and return its mathematical properties."""
    if number < 0:
        raise HTTPException(
            status_code=400,
            detail={
                "number": number,
                "error": True,
            }
        )

    if number is None:
        raise HTTPException(
            status_code=400,
            detail={
                "number": number,
                "error": True,
            }
        )
    properties = []
    if is_armstrong(number):
        properties.append("armstrong")
    if number % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")

    digit_sum = sum(int(d) for d in str(number))
    fun_fact = get_fun_fact(number)


    return {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": digit_sum,
        "fun_fact": fun_fact,
    }


