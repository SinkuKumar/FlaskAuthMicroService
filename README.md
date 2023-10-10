# Flask Authentication API

This is a simple Flask-based authentication API that allows users to register, login, and access protected routes.

## Prerequisites

Make sure you have the following installed:

- Python 3.x
- Flask
- Flask-SQLAlchemy
- Flask-JWT-Extended
- bcrypt
- `unittest` (standard library)

## Setup and Usage

1. Clone the repository.

2. Install the required dependencies:

    ```bash
    pip install requirements.txt
    ```

3. Set up the database URI in the `app.config['SQLALCHEMY_DATABASE_URI']` variable in `app.py`.

4. Set your JWT secret key in `app.config['JWT_SECRET_KEY']`.

5. Run the application:

    ```bash
    python app.py
    ```

6. Run the test cases:

    ```bash
    python tests.py
    ```

## Routes

- **POST /register**: Register a new user.

    Example request body:
    ```json
    {
        "username": "example_user",
        "password": "example_password"
    }
    ```

- **POST /login**: Log in with a registered user.

    Example request body:
    ```json
    {
        "username": "example_user",
        "password": "example_password"
    }
    ```

- **GET /protected**: Access a protected route. Requires a valid JWT token.

## Running the Tests

The tests are written using the `unittest` framework. To run the tests, execute the following command:

```bash
python tests.py
```

The test cases cover the registration, login, and protected route functionality of the API.

## Notes

- This API uses SQLite as the database. For production, consider using a more robust database like PostgreSQL.

## Docker

To host the Flask app as a microservice using Docker, you'll need to follow these steps:


1. **Build the Docker image:**
   Navigate to the directory containing the Dockerfile and the Flask app code and run:

```bash
docker build -t flask-microservice .
```

2. **Run the Docker container:**
   After building the image, run the Docker container:

```bash
docker run -p 5000:5001 flask-microservice
```

This command maps port 5000 from the container to port 5001 on your host machine.

Now, your Flask application is running as a microservice within a Docker container. You can access the API using `http://localhost:5001`. Replace `localhost` with the appropriate host if you're running Docker on a remote machine.
