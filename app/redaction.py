
#import email
#from bs4 import BeautifulSoup
#
#def read_html_file(html_filepath):
#    """Reads and returns the contents of a file at the given filepath."""
#    with open(html_filepath, 'r', encoding='utf-8') as f:
#        return f.read()
#
#def read_and_parse_mhtml(html_filepath):
#    """Extracts HTML content from an MHTML file."""
#    page_source = read_html_file(html_filepath)
#
#    html_content = None
#    if page_source:
#        message = email.message_from_string(page_source)
#        for part in message.walk():
#            if part.get_content_type() == 'text/html':
#                html_content = part.get_payload(decode=True).decode('utf-8')
#                break
#    return html_content
#
#def redact_tbody(html_content):
#    """Redacts all content within <tbody> elements in the HTML."""
#    soup = BeautifulSoup(html_content, "html.parser")
#    tbodies = soup.find_all("tbody")
#    for tbody in tbodies:
#        tbody.clear()  # Removes all child elements
#    return str(soup)
#
#def write_html_file(output_filepath, html_content):
#    """Saves the modified HTML content to a new file."""
#    with open(output_filepath, 'w', encoding='utf-8') as f:
#        f.write(html_content)
#
#
#if __name__ == "__main__":
#
#
#    import os
#    import webbrowser
#
#    #from app.html_helpers import read_html_file, write_html_file
#    from conftest import DASHBOARD_1_FILEPATH, DASHBOARD_2_FILEPATH
#
#    for redacted_filepath in [DASHBOARD_1_FILEPATH, DASHBOARD_2_FILEPATH]:
#        filepath = redacted_filepath.replace("-redacted","")
#        print("READING HTML FILE:")
#        print(filepath)
#        content = read_html_file(filepath)
#
#        print("REDACTING...")
#        redacted = redact_tbody(content)
#
#        print("WRITING TO FILE:")
#        output_filepath = redacted_filepath.replace(".mhtml",".html")
#        output_filepath = output_filepath.replace("redacted", "autoredacted")
#        print(os.path.abspath(output_filepath))
#        write_html_file(output_filepath, redacted)
#
#        webbrowser.open("file://" + os.path.abspath(output_filepath))
#
