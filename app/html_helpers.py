
import email

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
    #with open(html_filepath, 'rb') as f:
    with open(html_filepath, 'r', encoding='utf-8') as f:
        return f.read()


def read_and_parse_mhtml(html_filepath):
    """The page content we saved seems to have some headers before the document starts,
        so this strategy gets us to the page contents.

        Returns just the page contents in HTML format.
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


#def write_html_file(html_filepath, html_content):
#    with open(html_filepath, "w") as f:
#        f.write(html_content)
