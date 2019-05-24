import pytest
from app import app
import json
import datetime


@pytest.fixture
def client():
    app.testing = True
    client = app.test_client()
    yield client


def test_student_resubmissions(client):
    # assert False
    pass


def test_distribution(client):
    """ Tests histogram data

    Test labels are as expected
    Test datasets' labels are module names
    Test datasets' data contains 10 elements
    Test datasets' data contains only integers
    """
    url = "/graph/histogram"
    resp = client.get(url)
    print(resp.json)
    assert resp.json['labels'] == [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    for ds in resp.json['datasets']:
        assert ds['label'] in ['pre2-programming', 'pre1-maths']
        assert len(ds['data']) == 10
        assert all(isinstance(x, int) for x in ds['data'])


def test_grades(client):
    """ Test grades graph data

    Tests all student ideas are present
    Tests module names are one of the expected labels
    Tests grade is a number between 0 and 100
    """
    url = "/graph/grades"
    resp = client.get(url)
    assert resp.json['labels'] == [
        14, 15, 19, 21, 26, 30,
        34, 35, 38, 39, 42, 43,
        44, 46, 48, 50, 51, 55,
        59
    ]
    for ds in resp.json['datasets']:
        assert ds['label'] in ['pre1-maths', 'pre2-programming']
        for grade in ds['data']:
            assert type(grade) in [float, int]
            assert grade <= 100
            assert grade >= 0


def test_groups(client):
    """ Tests the groups

    Tests both expected group names are present
    """
    url = "/groups"
    resp = client.get(url)
    assert resp.json == ['cohort1', 'cohort2']


def test_students(client):
    """ Tests students list

    Tests list of all students
    Tests by group:
        ensure only students in group are returned when specified
    """
    url = "/students"
    resp = client.get(url)
    print(resp.json)
    assert set([14, 26, 15, 19, 34]).issubset(resp.json)
    assert not set([14, 26, 15, 19, 34, 99]).issubset(resp.json)

    url = "/students?group=cohort1"
    resp = client.get(url)
    print(resp.json)
    assert set([14, 15, 19]).issubset(resp.json)
    assert not set([14, 15, 19, 34]).issubset(resp.json)
    # assert False


def test_top_scores(client):
    """ Tests top scores data

    Tests number of results (one for each student/module)
    Tests at least one expected entry is in result set
    """
    url = "/data/top_scores"
    resp = client.get(url)
    assert len(resp.json) == 29
    assert {
        "group": "cohort1",
        "module": "pre1-maths",
        "score": 22.697930724246515,
        "student": 15
    } in resp.json
    print(len(resp.json))
    # assert False


def test_resumbissions(client):
    """ Tests the resubmission scatter plot data

    Tests that each group has the correct number of labels
    Tests that a sample of labels are present of absent as required
    tests 'y' value is always a float >= 0

    """
    url = "/graph/resubmissions"
    resp = client.get(url)
    assert len(resp.json) == 29
    labels = [s['label'] for s in resp.json]
    assert {
        'Student_38_pre1-maths',
        'Student_44_pre2-programming',
        'Student_55_pre1-maths',
        'Student_48_pre2-programming',
        'Student_46_pre1-maths'
    }.issubset(set(labels))

    url = "/graph/resubmissions?group=cohort1"
    resp = client.get(url)
    assert len(resp.json) == 6
    labels = [s['label'] for s in resp.json]
    assert not {
        'Student_38_pre1-maths',
        'Student_44_pre2-programming',
        'Student_55_pre1-maths',
        'Student_48_pre2-programming',
        'Student_46_pre1-maths'
    }.issubset(set(labels))
    assert {
        'Student_14_pre2-programming',
        'Student_15_pre1-maths',
        'Student_15_pre2-programming',
        'Student_19_pre1-maths'
    }.issubset(set(labels))

    url = "/graph/resubmissions?group=cohort2"
    resp = client.get(url)
    assert len(resp.json) == 23
    labels = [s['label'] for s in resp.json]
    assert not {
        'Student_14_pre2-programming',
         'Student_15_pre1-maths',
         'Student_15_pre2-programming',
         'Student_19_pre1-maths'
    }.issubset(set(labels))

    assert {
        'Student_30_pre2-programming',
        'Student_34_pre1-maths',
        'Student_34_pre2-programming',
        'Student_35_pre1-maths'
    }.issubset(set(labels))

    url = "/graph/resubmissions?group[]=cohort1,cohort2"
    resp = client.get(url)
    assert len(resp.json) == 29
    for e in resp.json:
        for d in e['data']:
            x = d['x']
            y = d['y']
            assert type(y) == float
            assert y >= 0
    # assert False
