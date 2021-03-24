import pytest
import System
import User

exec(open('RestoreData.py').read())

#pass
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

#pass
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

@pytest.fixture
def TA_user(grading_system):
    TA_name = 'cmhbf5'
    TA_password = 'bestTA'
    grading_system.login(TA_name, TA_password)
    return grading_system.usr

#fail
def test_change_grade(grading_system, professor_user, student_user):
    student_name = student_user.name
    course = "comp_sci"
    assignment = "assignment1"
    new_grade = 50
    professor_user.change_grade(student_name, course, assignment, new_grade)
    grading_system.reload_data()
    assert grading_system.users[student_name]['courses'][course][assignment]['grade'] == new_grade

#pass
def test_create_assignment(grading_system, professor_user):
    assignment_name = "test_assignment"
    due_date = "2/1/21"
    course = 'comp_sci'
    professor_user.create_assignment(assignment_name, due_date, course)
    grading_system.reload_data()
    assert assignment_name in grading_system.courses[course]['assignments']
    assert grading_system.courses[course]['assignments'][assignment_name]['due_date'] == due_date

#pass
def test_drop_student(grading_system, professor_user):
    student_name = 'akend3'
    course = 'databases'
    assert course in grading_system.users[student_name]['courses']
    professor_user.drop_student(student_name, course)
    grading_system.reload_data()
    assert course not in grading_system.users[student_name]['courses']
    exec(open('RestoreData.py').read())

#fail
def test_add_student(professor_user, student_user):
    student_name = student_user.name
    course = 'software_engineering'
    professor_user.add_student(student_name, course)

#fail
def test_submit_assignment(grading_system, student_user):
    course = 'comp_sci'
    assignment_name = 'assignment2'
    submission = 'Here is the the fake assignment, its super cool'
    submisson_date = '2/11/20'
    student_name = student_user.name
    student_user.submit_assignment(course, assignment_name, submission, submisson_date)
    grading_system.reload_data()
    assert assignment_name in grading_system.users[student_name]['courses'][course]
    assert submisson_date in grading_system.users[student_name]['courses'][course][assignment_name]['submission_date']
    assert submission in grading_system.users[student_name]['courses'][course][assignment_name]['submission']
    assert grading_system.users[student_name]['courses'][course][assignment_name]['ontime'] == False

#fail
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

#pass
def test_student_check_grades(grading_system, student_user):
    student_name = student_user.name
    course = 'comp_sci'
    assignments = grading_system.users[student_name]['courses'][course]
    grades = student_user.check_grades(course)
    for a in grades:
       assert a[0] in assignments
       assert grading_system.users[student_name]['courses'][course][a[0]]['grade'] == a[1]

#fail
def test_view_assignments(grading_system, student_user):
    course = 'databases'
    classAssignments = grading_system.courses[course]['assignments']
    studentAssignments = student_user.view_assignments(course)
    for a in studentAssignments:
        nameMatch = a[0] in classAssignments
        dueDateMatch = a[1] in classAssignments[a[0]]['due_date']
        assert nameMatch and dueDateMatch

def test_TA_check_grades(grading_system, TA_user, student_user):
    student_name = 'hdjsr7'
    course = 'software_engineering'
    assignments = grading_system.users[student_name]['courses'][course]
    studentAssignments = grading_system.users[student_name]['courses'][course]
    studentGrades = TA_user.check_grades(student_name, course)
    for a in studentGrades:
        assert a[0] in assignments
        assert a[1] == studentAssignments[a[0]]['grade']

def test_TA_create_assignment(grading_system, TA_user):
    course = 'software_engineering'
    due_date = '5/10/21'
    assignment_name = 'Name the best TA Assignment'
    TA_user.create_assignment(assignment_name, due_date, course)
    assignments = grading_system.courses[course]['assignments']
    assert assignment_name in assignments
    # assert assignments[assignment_name]['due_date'] == due_date

def test_student_view_assignment_update(grading_system, student_user, professor_user):
    # professor makes assignment
    # student can view assignments
    course = 'databases'
    assignment_name = 'assignment with fake name'
    due_date = '3/1/21'
    assert assignment_name not in grading_system.courses[course]['assignments']
    professor_user.create_assignment(assignment_name, due_date, course)
    grading_system.reload_data()
    assignments = student_user.view_assignments(course)
    assert assignment_name in grading_system.courses[course]['assignments']
    

def test_prof_see_update_after_change(professor_user):
    student_name = 'akend3'
    course = 'databases'
    assignment_name = 'assignment2'
    newGrade = 75

    grades = professor_user.check_grades(student_name, course)
    professor_user.change_grade(student_name, course, assignment_name, newGrade)
    newGrades = professor_user.check_grades(student_name, course)
    assert grades != newGrades


def test_student_grade_update(professor_user, student_user):
    student_name = student_user.name
    course = 'databases'
    assignment_name = 'assignment1'
    grades1 = student_user.check_grades(course)
    professor_user.change_grade(student_name, course, assignment_name, 100)
    grades2 = student_user.check_grades(course)
    assert grades1 != grades2

exec(open('RestoreData.py').read())