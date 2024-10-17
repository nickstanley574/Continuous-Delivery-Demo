import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import multiprocessing

from selenium.webdriver.chrome.options import Options

from app import create_app, db


@pytest.fixture(scope="module")
def test_client():
    """Set up the Flask test client and run the app."""

    app = create_app("local")  # or 'development' based on your config
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False  # Disable CSRF for testing

    # Run the app on a different port in a separate thread
    port = 5000
    server = multiprocessing.Process(
        target=app.run, kwargs={"port": port, "use_reloader": False}
    )
    server.start()

    time.sleep(1)  # If app time to start

    yield f"http://localhost:{port}"  # Return the URL of the test server

    # Stop the server after tests
    server.terminate()

    with app.app_context():
        db.drop_all()


@pytest.fixture(scope="module")
def browser():
    """Set up the Selenium WebDriver."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=chrome_options,
    )
    yield driver
    driver.quit()


def test_index_page(browser, test_client):
    """Test that the index page loads correctly."""
    # Adjust the URL as needed
    browser.get("http://127.0.0.1:5000/")
    # Wait for the page to load
    time.sleep(1)

    assert "ToDo App" in browser.title  # Check the title
    assert (
        len(browser.find_elements(By.CLASS_NAME, "todo-item")) == 0
    )  # Check if any todos are displayed


def test_add_todo(browser, test_client):
    """Test adding a new todo."""
    browser.get("http://127.0.0.1:5000/")  # Go to the index page
    time.sleep(2)

    # Find the form elements and fill them
    title_input = browser.find_element(By.NAME, "title")
    description_input = browser.find_element(By.NAME, "description")
    submit_button = browser.find_element(By.XPATH, '//button[text()="Add"]')

    title_input.send_keys("Selenium Test ToDo")
    description_input.send_keys("This todo was added by Selenium test.")
    submit_button.click()

    time.sleep(2)  # Wait for the page to reload

    # Verify that the new todo is in the list
    assert "Selenium Test ToDo" in browser.page_source


def test_delete_todo(browser, test_client):
    """Test deleting a todo."""
    browser.get("http://127.0.0.1:5000/")  # Go to the index page
    time.sleep(2)

    delete_button = browser.find_element(By.XPATH, '//button[text()="Delete"]')
    delete_button.click()

    time.sleep(2)  # Wait for the page to reload

    # Verify that the todo is deleted
    assert "Selenium Test ToDo" not in browser.page_source
