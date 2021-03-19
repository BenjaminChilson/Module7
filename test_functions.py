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

@pytest.fixture
def student_user(grading_system):
    username = "akend3"
    password = "123454321"
    grading_system.login(username, password)
    return grading_system.usr

@pytest.fixture
def professor_user(grading_system):
    username = "goggins"
    password = "augurrox"
    grading_system.login(username, password)
    return grading_system.usr


def test_change_grade(grading_system, professor_user, student_user):
    student_name = student_user.name
    course = "comp_sci"
    assignment = "assignment1"
    new_grade = 50
    
    professor_user.change_grade(student_name, course, assignment, new_grade)
    grading_system.reload_data()
    assert grading_system.users[student_name]['courses'][course][assignment]['grade'] == new_grade

def test_create_assignment(grading_system, professor_user):
    assignment_name = "test_assignment"
    due_date = "2/1/21"
    course = 'comp_sci'
    professor_user.create_assignment(assignment_name, due_date, course)
    grading_system.reload_data()
    assert assignment_name in grading_system.courses[course]['assignments']
    assert grading_system.courses[course]['assignments'][assignment_name]['due_date'] == due_date