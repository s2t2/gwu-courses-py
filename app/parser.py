
from functools import cached_property

from bs4 import BeautifulSoup
from pandas import DataFrame



class PageParser:
    """Parses a previously downloaded HTML page"""
    def __init__(self, html_filepath):
        self.html_filepath = html_filepath

        with open(self.html_filepath, 'r') as html_file:
            contents = html_file.read()
            self.soup = BeautifulSoup(contents, features="html.parser")

    @cached_property
    def courses(self):
        """
        Looking for:

            <table class="courseListing basicTable courseListingSetWidths" style="background-color:#006699;">

        """
        records = []

        tables = self.soup.find_all("table", "courseListing")

        for table in tables:
            course_row = table.find("tr", "crseRow1")
            comments_row = table.find("tr", "crseRow2")

            cells = course_row.find_all("td")
            #vals = [clean_text(cell.text) for cell in cells]
            #> ['OPEN', '71511', 'EMSE1001', '10', 'Introduction to Systems Engineering', '1.00', '', 'TOMP 406', 'F09:35AM - 10:25AM', '08/29/22 - 12/12/22', 'Linked']

            #subj, number = [span.text.strip() for span in cells[2].find_all("span")]
            short_code = " ".join( [span.text.strip() for span in cells[2].find_all("span")])
            comments = comments_row.text.strip().replace("\n","").replace("\t","").replace("\xa0\xa0"," ")

            record = {
                "availability": cells[0].text,
                "crn": cells[1].text,
                "short_code": short_code,
                "section": cells[3].text,
                "title": cells[4].text,
                "credits": cells[5].text.strip(), # this can be like "0.00 OR   3.00"
                "instructor": cells[6].text,
                "location": cells[7].text,
                "time_range": cells[8].text, # FYI: the first char is the day M/T/W/R/F, etc
                "date_range": cells[9].text,
                "comments": comments
            }
            records.append(record)

        df = DataFrame(records)
        #print(df.head())
        return df
