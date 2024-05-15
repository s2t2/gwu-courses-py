
from pprint import pprint
from functools import cached_property
from datetime import datetime
from typing import List, Dict

from bs4 import BeautifulSoup


class DashboardParser:

    def __init__(self, page_source):
        self.page_source = page_source
        #self.accessed_at = datetime.now()


    @cached_property
    def soup(self):
        return BeautifulSoup(self.page_source, "html.parser")

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
    def heading_records(self) -> List[Dict]:
        """Only get headings that have two spans.
            Based on observation, one is the heading and the other is the status badge.

            Returns
        """
        print("PAGE HEADINGS:")
        records = []
        for heading in self.headings:
            print("...", heading.text)

            spans = heading.find_all("span")
            if len(spans) == 2:
                # THESE ARE THE HEADINGS WE ARE LOOKING FOR

                # TRY TO GET THE GPA FROM NEIGHBORING ELEMENT:
                gpa = None
                try:
                    label_span = heading.parent.find("span", string='Block GPA:')
                    gpa = label_span.parent.text.replace("Block GPA: ","")
                except:
                    try:
                        gpa = heading.parent.text.split("Block GPA: ")[-1].strip()
                    except:
                        pass

                records.append({
                    "student_id": self.student_id,
                    "student_name": self.student_name,
                    "title": spans[0].text.strip(),
                    "status": spans[1].text.strip(),
                    "gpa": gpa,
                    #"accessed_at": self.accessed_at.strftime("%Y-%m-%d %H:%M:%S")
                })

        return records
