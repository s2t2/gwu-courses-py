
import pytest

from conftest import CI_ENV, DASHBOARD_1_FILEPATH, DASHBOARD_2_FILEPATH
from app.html_helpers import read_and_parse_mhtml
from app.dmap.dashboard_parser import DashboardParser


SKIP_REASON = "Dashboard pages are ignored right now for privacy. Can remove skip once pages are more completely redacted."


@pytest.fixture(scope="module")
def dashboard_1_source():
    return read_and_parse_mhtml(DASHBOARD_1_FILEPATH)

@pytest.fixture(scope="module")
def dashboard_2_source():
    return read_and_parse_mhtml(DASHBOARD_2_FILEPATH)



@pytest.mark.skipif(CI_ENV, reason=SKIP_REASON)
def test_headings(dashboard_1_source, dashboard_2_source):
    parser = DashboardParser(dashboard_1_source)
    #breakpoint()
    #assert parser.headings == [
    #    'Bachelor of Arts Degree', # IN-PROGRESS
    #    'Writing in the Disciplines Requirement', # COMPLETE
    #    'University General Education Requirements', # COMPLETE
    #    'Columbian College General Education Curriculum', # IN-PROGRESS
    #    'Major in Political Science', # IN-PROGRESS
    #    'Major in Criminal Justice', # IN-PROGRESS
    #    'Departmental/Special Honors', # INCOMPLETE
    #    'Fall Through General Electives',
    #    'In-progress',
    #    'Not Counted'
    #]
    assert parser.heading_records == [
        {'title': 'Bachelor of Arts Degree', 'status': 'IN-PROGRESS'},
        {'title': 'Writing in the Disciplines Requirement', 'status': 'COMPLETE'},
        {'title': 'University General Education Requirements', 'status': 'COMPLETE'},
        {'title': 'Columbian College General Education Curriculum', 'status': 'IN-PROGRESS'},
        {'title': 'Major in Political Science', 'status': 'IN-PROGRESS'},
        {'title': 'Major in Criminal Justice', 'status': 'IN-PROGRESS'},
        {'title': 'Departmental/Special Honors', 'status': 'INCOMPLETE'}
    ]

    parser = DashboardParser(dashboard_2_source)
    #breakpoint()
    #assert parser.headings == [
    #    'Bachelor of Arts Degree', # IN-PROGRESS
    #    'Writing in the Disciplines Requirement', # COMPLETE
    #    'University General Education Requirements', # COMPLETE
    #    'Columbian College General Education Curriculum', # IN-PROGRESS
    #    'Major in Political Science', # IN-PROGRESS
    #    'Major in Criminal Justice', # IN-PROGRESS
    #    'Departmental/Special Honors', # INCOMPLETE
    #    'Fall Through General Electives',
    #    'In-progress',
    #    'Not Counted'
    #]
    assert parser.heading_records == [
        {'title': 'Bachelor of Arts Degree', 'status': 'IN-PROGRESS'},
        {'title': 'Writing in the Disciplines Requirement', 'status': 'COMPLETE'},
        {'title': 'University General Education Requirements', 'status': 'COMPLETE'},
        {'title': 'Columbian College General Education Curriculum', 'status': 'COMPLETE'},
        {'title': 'Major in Political Science', 'status': 'COMPLETE'},
        {'title': 'Minor in Span/LatAm Langs,Lits,Cultures', 'status': 'IN-PROGRESS'},
        {'title': "Minor in Women's, Gender, and Sexuality Studies", 'status': 'COMPLETE'},
        {'title': 'Honors Program', 'status': 'IN-PROGRESS'},
        {'title': 'Departmental/Special Honors', 'status': 'COMPLETE'}
    ]
