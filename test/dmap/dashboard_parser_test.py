
import os
#from pprint import pprint

import pytest

from conftest import CI_ENV, TEST_DIRPATH
from app.html_helpers import read_and_parse_mhtml
from app.dmap.dashboard_parser import DashboardParser

SKIP_REASON = "Dashboard pages are ignored right now for privacy. Can remove skip once pages are more completely redacted."

MOCK_DMAP_DIRPATH = os.path.join(TEST_DIRPATH, "mock_dmap")
DASHBOARD_1_FILEPATH = os.path.join(MOCK_DMAP_DIRPATH, "dashboard-1-redacted.mhtml")
DASHBOARD_2_FILEPATH = os.path.join(MOCK_DMAP_DIRPATH, "dashboard-2-redacted.mhtml")

@pytest.fixture(scope="module")
def dashboard_1_source():
    return read_and_parse_mhtml(DASHBOARD_1_FILEPATH)

@pytest.fixture(scope="module")
def dashboard_2_source():
    return read_and_parse_mhtml(DASHBOARD_2_FILEPATH)



@pytest.mark.skipif(CI_ENV, reason=SKIP_REASON)
def test_student_info(dashboard_1_source, dashboard_2_source):
    parser = DashboardParser(dashboard_1_source)
    assert parser.student_id == "G11111111"
    assert parser.student_name == "LAST_NAME_1, FIRST_NAME_1 MIDDLE_NAME_1"

    parser = DashboardParser(dashboard_2_source)
    assert parser.student_id == "G22222222"
    assert parser.student_name == "LAST_NAME_2, FIRST_NAME_2 MIDDLE_INITIAL_2"


@pytest.mark.skipif(CI_ENV, reason=SKIP_REASON)
def test_heading_records(dashboard_1_source, dashboard_2_source):
    parser = DashboardParser(dashboard_1_source)
    assert parser.heading_records == [
        {
            'student_id': 'G11111111', 'student_name': 'LAST_NAME_1, FIRST_NAME_1 MIDDLE_NAME_1',
            'title': 'Bachelor of Arts Degree', 'status': 'IN-PROGRESS', 'gpa': '3.63'
        },
        {
            'student_id': 'G11111111', 'student_name': 'LAST_NAME_1, FIRST_NAME_1 MIDDLE_NAME_1',
            'title': 'Writing in the Disciplines Requirement', 'status': 'COMPLETE', 'gpa': '3.79'
        },
        {
            'student_id': 'G11111111', 'student_name': 'LAST_NAME_1, FIRST_NAME_1 MIDDLE_NAME_1',
            'title': 'University General Education Requirements', 'status': 'COMPLETE', 'gpa': '3.39'
        },
        {
            'student_id': 'G11111111', 'student_name': 'LAST_NAME_1, FIRST_NAME_1 MIDDLE_NAME_1',
            'title': 'Columbian College General Education Curriculum', 'status': 'IN-PROGRESS', 'gpa': '4.00'
        },
        {
            'student_id': 'G11111111', 'student_name': 'LAST_NAME_1, FIRST_NAME_1 MIDDLE_NAME_1',
            'title': 'Major in Political Science', 'status': 'IN-PROGRESS', 'gpa': '3.40'
        },
        {
            'student_id': 'G11111111', 'student_name': 'LAST_NAME_1, FIRST_NAME_1 MIDDLE_NAME_1',
            'title': 'Major in Criminal Justice', 'status': 'IN-PROGRESS', 'gpa': '3.74'
        },
        {
            'student_id': 'G11111111', 'student_name': 'LAST_NAME_1, FIRST_NAME_1 MIDDLE_NAME_1',
            'title': 'Departmental/Special Honors', 'status': 'INCOMPLETE', 'gpa': '3.43'
        }
    ]

    parser = DashboardParser(dashboard_2_source)
    assert parser.heading_records == [
        {
            'student_id': 'G22222222', 'student_name': 'LAST_NAME_2, FIRST_NAME_2 MIDDLE_INITIAL_2',
            'title': 'Bachelor of Arts Degree', 'status': 'IN-PROGRESS', 'gpa': '3.95'},
        {
            'student_id': 'G22222222', 'student_name': 'LAST_NAME_2, FIRST_NAME_2 MIDDLE_INITIAL_2',
            'title': 'Writing in the Disciplines Requirement', 'status': 'COMPLETE', 'gpa': '3.91'},
        {
            'student_id': 'G22222222', 'student_name': 'LAST_NAME_2, FIRST_NAME_2 MIDDLE_INITIAL_2',
            'title': 'University General Education Requirements', 'status': 'COMPLETE', 'gpa': '3.91'},
        {
            'student_id': 'G22222222', 'student_name': 'LAST_NAME_2, FIRST_NAME_2 MIDDLE_INITIAL_2',
            'title': 'Columbian College General Education Curriculum', 'status': 'COMPLETE', 'gpa': '4.00'},
        {
            'student_id': 'G22222222', 'student_name': 'LAST_NAME_2, FIRST_NAME_2 MIDDLE_INITIAL_2',
            'title': 'Major in Political Science', 'status': 'COMPLETE', 'gpa': '3.97'},
        {
            'student_id': 'G22222222', 'student_name': 'LAST_NAME_2, FIRST_NAME_2 MIDDLE_INITIAL_2',
            'title': 'Minor in Span/LatAm Langs,Lits,Cultures', 'status': 'IN-PROGRESS', 'gpa': '3.90'},
        {
            'student_id': 'G22222222', 'student_name': 'LAST_NAME_2, FIRST_NAME_2 MIDDLE_INITIAL_2',
            'title': "Minor in Women's, Gender, and Sexuality Studies", 'status': 'COMPLETE', 'gpa': '4.00'},
        {
            'student_id': 'G22222222', 'student_name': 'LAST_NAME_2, FIRST_NAME_2 MIDDLE_INITIAL_2',
            'title': 'Honors Program', 'status': 'IN-PROGRESS', 'gpa': '3.91'},
        {
            'student_id': 'G22222222', 'student_name': 'LAST_NAME_2, FIRST_NAME_2 MIDDLE_INITIAL_2',
            'title': 'Departmental/Special Honors', 'status': 'COMPLETE', 'gpa': '3.95'}
    ]
