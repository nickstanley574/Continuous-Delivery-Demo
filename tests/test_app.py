import pytest
from app import create_app, db
from app.models import ToDo


@pytest.fixture(scope="module")
def test_client():
    # Set up the Flask test client
    app = create_app("local")  # or 'development' based on your config
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()  # Create tables
        yield testing_client  # Testing happens here
        with app.app_context():
            db.drop_all()  # Cleanup


@pytest.fixture(scope="module")
def init_database(test_client):
    # Initialize the database with one todo inside application context
    todo = ToDo(title="Test ToDo", description="This is a test ToDo item")
    with test_client.application.app_context():
        db.session.add(todo)
        db.session.commit()

    yield db  # Return the database for testing

    # Cleanup the database after tests
    db.session.remove()
    db.drop_all()


def test_index_page(test_client, init_database):
    """Test that the index page loads correctly and displays existing todos."""
    response = test_client.get("/")
    assert response.status_code == 200
    assert b"Test ToDo" in response.data  # Check that the initial ToDo is displayed


def test_add_todo(test_client):
    """Test that a new todo can be added successfully."""
    response = test_client.post(
        "/add",
        data=dict(title="New ToDo", description="Another test todo"),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"New ToDo" in response.data  # Check that the new ToDo is displayed


def test_toggle_todo(test_client, init_database):
    """Test that a todo's done status can be toggled."""
    # Toggle the first todo (ID = 1) using the test client without manual app context
    response = test_client.post("/toggle/1", follow_redirects=True)
    assert response.status_code == 200

    # Access the todo directly via the database after the request is handled
    with test_client.application.app_context():
        todo = db.session.get(ToDo, 1)
        assert todo.done is True  # Check that the todo was toggled to 'done'

    # Toggle it back to 'not done'
    response = test_client.post("/toggle/1", follow_redirects=True)
    assert response.status_code == 200

    with test_client.application.app_context():
        todo = db.session.get(ToDo, 1)
        assert todo.done is False  # Check that the todo was toggled back to 'not done'


def test_delete_todo(test_client):
    """Test that a todo can be deleted."""
    response = test_client.post("/delete/1", follow_redirects=True)
    assert response.status_code == 200
    assert b"Test ToDo" not in response.data  # Ensure the deleted todo is not displayed
