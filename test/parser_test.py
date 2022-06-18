
import os

from pandas import DataFrame

from app.parser import PageParser

from conftest import MOCK_EXPORTS_DIRPATH


def test_page_parser():

    html_filepath = os.path.join(MOCK_EXPORTS_DIRPATH, "EMSE", "page_1.html")
    parser = PageParser(html_filepath=html_filepath)

    courses = parser.courses
    assert isinstance(courses, DataFrame)
    assert len(courses) == 20

    assert courses.iloc[0].to_dict() == {
        'availability': 'OPEN',
        'crn': '71511',
        #'short_code': 'EMSE 1001',
        'subject': 'EMSE',
        'number': '1001',
        'section': '10',
        'title': 'Introduction to Systems Engineering',
        'credits': '1.00',
        'instructor': '',
        'location': 'TOMP 406',
        'time_range': 'F09:35AM - 10:25AM',
        'date_range': '08/29/22 - 12/12/22',
        'comments': 'Comments: Also register for laboratory section: EMSE 1001.30. This course meets: 10/14/2022 - 12/9/2022. Registration restricted to SEAS freshmen only. Find Books'
    }
