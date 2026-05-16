# Calculator

This is a simple calculator application that provides both a command-line interface and a REST API for basic arithmetic operations. It has been extended, using the agent, from the sample command line application provided as part of the [boot.dev course](https://www.boot.dev/courses/build-ai-agent-python).

## Project Structure

```
.
├── calculator/
│   ├── pkg/
│   │   ├── operations.py
│   │   └── util.py
│   ├── __init__.py
│   ├── api.py
│   └── main.py
├── tests/
│   ├── test_api.py
│   └── test_operations.py
├── Dockerfile
├── requirements.txt
└── README.md
```

## Command Line Tool

To use the calculator as a command-line application, run `calculator/main.py` with the desired mathematical expression as an argument.

### Usage:
```bash
python calculator/main.py "<expression>"
```

### Examples:

```bash
python calculator/main.py "3 + 5"
python calculator/main.py "10 - 4 * 2"
python calculator/main.py "(2 + 3) * 4"
python calculator/main.py "5 > 3"
python calculator/main.py "10 / 2 == 5"
```

If no expression is provided, the application will print usage instructions.

### Supported Operations

The calculator supports the following operations:

*   **Arithmetic Operations**: Addition (`+`), Subtraction (`-`), Multiplication (`*`), Division (`/`).
*   **Unary Operators**: Unary plus (`+`) and unary minus (`-`).
*   **Parentheses**: `()` for controlling the order of operations.
*   **Comparison Operations**: Equal to (`==`), Greater than (`>`), Less than (`<`), Greater than or equal to (`>=`), Less than or equal to (`<=`). These can be used to compare the results of two arithmetic expressions.

### Error Handling

The calculator includes basic error handling:

*   **Invalid Expression**: Catches `ValueError` for malformed expressions, invalid characters, or insufficient operands.
*   **Division by Zero**: Prevents division by zero and raises a `ValueError`.
*   **Mismatched Parentheses**: Detects and reports errors for unbalanced parentheses.
*   **Unexpected Errors**: Catches general exceptions for unforeseen issues.

### Special Behavior

Occasionally, approximately 10% of the time, one of the numeric operands in the user's input expression may be randomly changed to a different number between -100 and 100. This behavior is very silly but I implemented it because I am a good and obedient bot.


## REST API

The REST API is built using the **FastAPI** framework.

### Endpoints

The API provides the following `GET` endpoints:

*   **`/`**: Serves the `index.html` file.
*   **`/health`**: Returns the API health status.
    *   **Response Body Example:**
        ```json
        {
            "status": "ok"
        }
        ```

*   **`/add`**: Performs addition of two numbers.
    *   **Query Parameters:** `a` (float), `b` (float)
    *   **Example Request:** `/add?a=5&b=3`
    *   **Response Body Example:**
        ```json
        {
            "result": 8.0
        }
        ```

*   **`/subtract`**: Performs subtraction of two numbers.
    *   **Query Parameters:** `a` (float), `b` (float)
    *   **Example Request:** `/subtract?a=5&b=3`
    *   **Response Body Example:**
        ```json
        {
            "result": 2.0
        }
        ```

*   **`/multiply`**: Performs multiplication of two numbers.
    *   **Query Parameters:** `a` (float), `b` (float)
    *   **Example Request:** `/multiply?a=5&b=3`
    *   **Response Body Example:**
        ```json
        {
            "result": 15.0
        }
        ```

*   **`/divide`**: Performs division of two numbers.
    *   **Query Parameters:** `a` (float), `b` (float)
    *   **Example Request:** `/divide?a=6&b=3`
    *   **Response Body Example:**
        ```json
        {
            "result": 2.0
        }
        ```
    *   **Error Response (Division by Zero):**
        ```json
        {
            "detail": "Division by zero is not allowed."
        }
        ```

*   **`/calculate`**: Evaluates a mathematical expression.
    *   **Query Parameter:** `expression` (string, e.g., "5 + 3 * 2")
    *   **Example Request:** `/calculate?expression=5%20%2B%203%20*%202`
    *   **Response Body Example:**
        ```json
        {
            "result": 11.0
        }
        ```

*   **`/check`**: Evaluates a comparison expression (e.g., "5 = 3 + 2").
    *   **Query Parameter:** `expression` (string, e.g., "5 = 3 + 2")
    *   **Example Request:** `/check?expression=5%20%3D%203%20%2B%202`
    *   **Response Body Example:**
        ```json
        {
            "result": true
        }
        ```
    *   **Error Response (Invalid Expression):**
        ```json
        {
            "detail": "Invalid expression format for check. Expected format: 'expression = result'"
        }
        ```

### Running Locally

To run the application locally using Docker, follow these steps:

1.  **Build the Docker image:**
    ```bash
    docker build -t calculator .
    ```

2.  **Run the Docker container:**
    ```bash
    docker run -d -p 80:80 calculator
    ```

    The API will be accessible at `http://localhost:80`.


---
This `README.md` was generated by the agent.

The original code has been modified by the AI agent.