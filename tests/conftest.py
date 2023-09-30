import pytest
import time

from src.base.items import Category


@pytest.fixture
def categories():
    categories = [
        Category('IT', 'www.test.com/it'),
        Category('Management', 'www.test.com/management'),
        Category('3D', 'www.test.com/3d')
    ]
    return categories

def pytest_addoption(parser):
    parser.addoption(
        "--run-slow",
        default="true",
        choices=("true", "false")
    )

@pytest.mark.skipif('config.getoption("--run-slow") == "false"')
def test_slow():
    time.sleep(3)

def test_fast():
    print('fast')
