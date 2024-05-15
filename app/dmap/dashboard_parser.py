
from pprint import pprint
from functools import cached_property

from bs4 import BeautifulSoup


class DashboardParser:

    def __init__(self, page_source):
        self.page_source = page_source


    @cached_property
    def soup(self):
        return BeautifulSoup(self.page_source, "html.parser")

    @property
    def record(self):
        return {
            "student_id": self.student_id,
            "student_name": self.student_name,
            "departmental_honors_gpa": self.departmental_honors_gpa,
            "departmental_honors_status": self.departmental_honors_status,
        }

    @property
    def student_id(self):
        try:
            gwid_input = self.soup.find('input', {'id': 'studentSearch'})
            if not gwid_input:
                gwid_input = self.soup.find('input', id="student-id")

            return gwid_input["value"]
        except:
            return None

    @property
    def student_name(self):
        try:
            return self.soup.find('input', {'id': 'student-name'})["value"]
        except:
            return None

    @property
    def headings(self):
        return self.soup.find_all("h2")

    @property
    def heading_records(self):
        """Only get headings that have two spans.
            Based on observation, one is the heading and the other is the status badge.
        """
        print("PAGE HEADINGS:")
        records = []
        for heading in self.headings:
            print("...", heading.text)

            spans = heading.find_all("span")
            if len(spans) == 2:
                records.append({
                    "title": spans[0].text.strip(),
                    "status": spans[1].text.strip(),
                    #"gpa": gpa
                })
            #else:
            #    records.append([heading.text])

        return records

    #@property
    #def departmental_honors_block(self):
    #    try:
    #        breakpoint()
    #        return "TODO"
    #    except:
    #        return None

    @property
    def departmental_honors_gpa(self):
        try:
            return "TODO"
        except:
            return None

    @property
    def departmental_honors_status(self):
        try:
            return "TODO"
        except:
            return None
