from application import app


def f():
    return 3


def test_function():
    assert f() == 3


def test_home_page():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """

    # Create a test client using the Flask application configured for testing
    with app.test_client() as test_client:
        response = test_client.get('/home')
        assert response.status_code == 200
        assert b"Simple Python Web App" in response.data
        assert b"Flask web microframework" in response.data
        assert b"Version" in response.data


def test_welcome_page():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/welcome/bob' page is requested (GET)
    THEN check that the response is valid
    """

    with app.test_client() as test_client:
        response = test_client.get('/welcome/bob')
        assert response.status_code == 200
        assert b"Hello Bob." in response.data
        assert b"Welcome Everyone!" in response.data
        assert b"Version" in response.data


def test_welcome_page_with_team():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/welcome/team' page is requested (GET)
    THEN check that the response is valid
    """

    with app.test_client() as test_client:
        response = test_client.get('/welcome/team')
        assert response.status_code == 200
        assert b"Hello Team." in response.data
        assert b"Welcome Everyone!" in response.data
        assert b"Version" in response.data


def test_jokes_page():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/joke' page is requested (GET)
    THEN check that the response is valid
    """

    with app.test_client() as test_client:
        response = test_client.get('/joke')
        assert response.status_code == 200
        assert b"Tell me a joke" in response.data
        assert b"Tell me another" in response.data
        assert b"Version" in response.data


def test_joke_count():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/joke' page is requested (GET)
    THEN check that the correct number of jokes is displayed
    """

    with app.test_client() as test_client:
        response = test_client.get('/joke')
        assert response.status_code == 200
        assert b"Number of jokes" in response.data
        assert b"21" in response.data

def test_register_page():
    """
    testing /register page functionality
    """
    with app.test_client() as test_client:
        response = test_client.get("/register")
        assert response.status_code == 201

        # make post request to register a user
        response = test_client.post("/register", data={"username": "John", "password": "123" })
        assert response.status_code == 302

def test_login():
    """
    testing /login page
    """
    with app.test_client() as test_client:
        response = test_client.get("/login")
        assert response.status_code == 200

        response = test_client.post("/login", data={"username": "John", "password": "123"})
        assert response.status_code == 302

        response = test_client.post("/login", data={"username": "John", "password": "1234"})
        assert response.status_code == 401