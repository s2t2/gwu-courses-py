
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
        records = []

        breakpoint()
        #tables = self.soup.find_all("article", "placard")
