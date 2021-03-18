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

def test_check_password(grading_system):
    username = "akend3"
    correct_password = "123454321"
    incorrect_password = "wrongPassword123"
    assert grading_system.check_password(username, correct_password) == True
    assert grading_system.check_password(username, incorrect_password) == False
