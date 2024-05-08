

# for now we will use the saved HTML file instead of a live page we browsed to

import os
import email

from conftest import TEST_DIRPATH #MOCK_DMAP_DIRPATH
from app.dmap import parse_student_dashboard_page

MOCK_DMAP_DIRPATH = os.path.join(TEST_DIRPATH, "mock_dmap")

DASHBOARD_1_FILEPATH = os.path.join(MOCK_DMAP_DIRPATH, "dashboard-1-redacted.mhtml")
DASHBOARD_2_FILEPATH = os.path.join(MOCK_DMAP_DIRPATH, "dashboard-2-redacted.mhtml")

#
# HELPER FUNCTIONS
# ... normally we would be reading the HTML page source stright from the web driver (driver.page_source)
# ... however we are not easily able to login using an admin account
# ... so instead of testing against a live web driver,
# ... we have saved some page contents locally (refacting pii as necessary)
# ... we can use these mock pages for testing the page parsing functionality
#


def read_html_file(html_filepath):
    """Reads and returns the contents of a file at the given filepath."""
    with open(html_filepath, 'r', encoding='utf-8') as f:
        return f.read()

def read_and_parse_saved_page(html_filepath):
    """The page content we saved seems to have some headers before the document starts,
        so this strategy gets us to the page contents.
    """
    page_source = read_html_file(html_filepath)

    html_content = None
    if page_source:
        message = email.message_from_string(page_source)

        for part in message.walk():
            if part.get_content_type() == 'text/html':
                html_content = part.get_payload(decode=True)
                break

    return html_content



#
# PAGE PARSER TESTS
#

def test_page_parsing():

    page_source = read_and_parse_saved_page(DASHBOARD_1_FILEPATH)
    record = parse_student_dashboard_page(page_source)
    assert record == {
        'gwid': 'G11111111',
        'name': 'LAST_NAME_1_REDACTED, FIRST_NAME_1_REDACTED MIDDLE_NAME_1_REDACTED',
        'major_gpa': '3.63',
        'honors_status': 'INCOMPLETE'
    }

    page_source = read_and_parse_saved_page(DASHBOARD_2_FILEPATH)
    record = parse_student_dashboard_page(page_source)
    assert record == {
        'gwid': 'G22222222',
        'name': 'LAST_NAME_2_REDACTED, FIRST_NAME_2_REDACTED MIDDLE_INITIAL_2_REDACTED',
        'major_gpa': '3.95',
        'honors_status': 'COMPLETE'
    }
