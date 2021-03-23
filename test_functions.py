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


def test_change_grade(professor_user, student_user):
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

def test_drop_student(grading_system, professor_user):
    student_name = 'akend3'
    course = 'databases'
    assert course in grading_system.users[student_name]['courses']
    professor_user.drop_student(student_name, course)
    grading_system.reload_data()
    assert course not in grading_system.users[student_name]['courses']


# def test_drop_student(grading_system, professor_user):
#     student_name = 'yted91'
#     course = 'software_engineering'
#     inCourse = course in grading_system.users[student_name]['courses']
#     professor_user.drop_student(student_name, course)
#     grading_system.reload_data()
#     outOfCourse = course not in grading_system.users[student_name]['courses']
#     assert inCourse and outOfCourse

def test_submit_assignment(grading_system, student_user):
    course = 'comp_sci'
    assignment_name = 'assignment1'
    submission = 'Here is the the fake assignment, its super cool'
    submisson_date = '1/31/20'
    student_name = student_user.name
    student_user.submit_assignment(course, assignment_name, submission, submisson_date)
    grading_system.reload_data()
    assert assignment_name in grading_system.users[student_name]['courses'][course]
    assert submisson_date in grading_system.users[student_name]['courses'][course][assignment_name]['submission_date']
    assert submission in grading_system.users[student_name]['courses'][course][assignment_name]['submission']

def test_check_ontime(grading_system, student_user):
    course = 'comp_sci'
    assignment_name = 'assignment1'
    submission = 'Here is the the fake assignment, its super cool'
    submisson_date = '1/31/20'
    student_name = student_user.name
    student_user.submit_assignment(course, assignment_name, submission, submisson_date)
    grading_system.reload_data()
    assert grading_system.users[student_name]['courses'][course][assignment_name]['submission_date'] == submisson_date
    assert grading_system.users[student_name]['courses'][course][assignment_name]['ontime'] == True
    submisson_date = '2/2/20'
    student_user.submit_assignment(course, assignment_name, submission, submisson_date)
    grading_system.reload_data()
    assert grading_system.users[student_name]['courses'][course][assignment_name]['submission_date'] == submisson_date
    assert grading_system.users[student_name]['courses'][course][assignment_name]['ontime'] == False

def test_check_grades(grading_system, student_user):
    student_name = student_user.name
    course = 'comp_sci'
    assignments = grading_system.users[student_name]['courses'][course]
    grades = student_user.check_grades(course)
    for a in grades:
       assert a[0] in assignments
       assert grading_system.users[student_name]['courses'][course][a[0]]['grade'] == a[1]

def test_view_assignments(grading_system, student_user):
    course = 'comp_sci'
    classAssignments = grading_system.courses[course]['assignments']
    studentAssignments = student_user.view_assignments(course)
    for a in studentAssignments:
        assert a[0] in classAssignments
        assert a[1] in classAssignments[a[0]]['due_date'] 
    