import pytest
import System
import User


def test_login(grading_system):
    username = "akend3"
    password = "123454321"
    grading_system.login(username, password)
    assert grading_system.usr.name == "akend3"

@pytest.fixture
def grading_system():
    gradingSystem = System.System()
    gradingSystem.load_data()
    return gradingSystem

