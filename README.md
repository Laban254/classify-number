# FastAPI Number Classifier

A FastAPI-based web service that classifies numbers based on their properties and fetches fun facts. The service can identify if a number is prime, perfect, or armstrong, and also provides the sum of its digits and a fun fact.

## Features

-   Classify numbers as **prime**, **perfect**, **armstrong**, **even**, or **odd**.
-   Calculate **digit sum**.
-   Fetch a **fun fact** from the Numbers API.
-   Error handling for invalid or malformed inputs.

## Requirements

-   Python 3.7 or higher
-   FastAPI
-   Uvicorn (ASGI server)
-   httpx (for making asynchronous HTTP requests)

## Installation

1.  Clone the repository:
    
    
    ```git clone https://github.com/yourusername/number-classifier.git
    cd number-classifier` 
    ```
2.  Create and activate a virtual environment:
    

    ```
    python3 -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate` 
   
3.  Install the dependencies:
    

    
    `pip install -r requirements.txt` 
    
4.  Run the FastAPI app with Uvicorn:
    

    
    `uvicorn main:app --reload` 
    
    This will start the server at `http://127.0.0.1:8000`.
    

## Endpoints

### 1. `/api/classify-number`

Classifies a number and returns its properties.

#### Method: `GET`

#### Query Parameters:

-   `number` (required): The number to classify (must be an integer).

#### Example Request:


`GET /api/classify-number?number=28` 

#### Example Response:



```json{
    "number": 28,
    "is_prime": false,
    "is_perfect": true,
    "properties": ["perfect", "even"],
    "digit_sum": 10,
    "fun_fact": "28 is a perfect number."
}` 
```
### Error Handling

-   **Invalid input** (e.g., non-integer, negative number):
    -   Returns a `400 Bad Request` error with the format:
        

        
        ```json{
          "number": "invalid_input",
          "error": true      

## License

This project is licensed under the MIT License.