
import pytest

from conftest import CI_ENV, DASHBOARD_1_FILEPATH, DASHBOARD_2_FILEPATH
from app.html_helpers import read_and_parse_mhtml
from app.dmap.honors_scraper import parse_student_dashboard_page


@pytest.mark.skipif(CI_ENV, reason="Dashboard pages are ignored right now for privacy. Can remove skip once pages are more completely redacted.")
def test_page_parsing():

    page_source = read_and_parse_mhtml(DASHBOARD_1_FILEPATH)
    record = parse_student_dashboard_page(page_source)
    assert record == {
        'gwid': 'G11111111',
        'name': 'LAST_NAME_1_REDACTED, FIRST_NAME_1_REDACTED MIDDLE_NAME_1_REDACTED',
        'departmental_honors_gpa': '3.43',
        'departmental_honors_status': 'INCOMPLETE'
    }

    page_source = read_and_parse_mhtml(DASHBOARD_2_FILEPATH)
    record = parse_student_dashboard_page(page_source)
    assert record == {
        'gwid': 'G22222222',
        'name': 'LAST_NAME_2_REDACTED, FIRST_NAME_2_REDACTED MIDDLE_INITIAL_2_REDACTED',
        'departmental_honors_gpa': '3.95',
        'departmental_honors_status': 'COMPLETE'
    }
