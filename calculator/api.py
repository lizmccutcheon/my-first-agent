from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pkg.calculator import Calculator

app = FastAPI()
calculator = Calculator()

@app.get("/")
async def root():
    return FileResponse("index.html")

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/add")
async def add(a: float, b: float):
    try:
        result = calculator.evaluate(f"{a} + {b}")
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/subtract")
async def subtract(a: float, b: float):
    try:
        result = calculator.evaluate(f"{a} - {b}")
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/multiply")
async def multiply(a: float, b: float):
    try:
        result = calculator.evaluate(f"{a} * {b}")
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/divide")
async def divide(a: float, b: float):
    if b == 0:
        raise HTTPException(status_code=400, detail="Division by zero is not allowed.")
    try:
        result = calculator.evaluate(f"{a} / {b}")
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/check")
async def check(expression: str):
    try:
        result = calculator.evaluate(expression)
        
        # The evaluate function will return True/False for comparison expressions
        if isinstance(result, bool):
            return {"result": result}
        else:
            # If it's not a comparison, it means the expression was not in the 'A=B' format
            # or it was a simple arithmetic expression without a comparison.
            # In this specific /check endpoint, we expect a comparison.
            raise HTTPException(status_code=400, detail="Invalid expression format for check. Expected format: 'expression = result'")
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=400, detail="An unexpected error occurred during evaluation.")

@app.get("/calculate")
async def calculate(expression: str):
    try:
        result = calculator.evaluate(expression)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
