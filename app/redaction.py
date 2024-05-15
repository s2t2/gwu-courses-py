


##import re
#
##def redact_tbody(html_content):
##    # This pattern matches <tbody> to </tbody> including any content in between
##    pattern = r'(<tbody>).*?(</tbody>)'
##    # Replace the content between <tbody> tags with <tbody>TBODY_REDACTED</tbody>
##    redacted_html = re.sub(pattern, r'\1TBODY_REDACTED\2', html_content, flags=re.DOTALL)
##    return redacted_html
#
#
#from bs4 import BeautifulSoup
#
#def redact_tbody(html_content):
#    soup = BeautifulSoup(html_content, "html.parser")
#    tbodies = soup.find_all("tbody")
#    print("FOUND", len(tbodies), "TABLE BODIES")
#    for tbody in tbodies:
#        tbody.clear()
#        tbody.append("TBODY_REDACTED")
#    return str(soup)
#
#
#
#if __name__ == "__main__":
#
#
#    import os
#    import webbrowser
#
#    from app.html_helpers import read_html_file, write_html_file
#    from conftest import DASHBOARD_1_FILEPATH, DASHBOARD_2_FILEPATH
#
#
#    for redacted_filepath in [DASHBOARD_1_FILEPATH, DASHBOARD_2_FILEPATH]:
#
#        filepath = redacted_filepath.replace("-redacted","")
#        print("READING HTML FILE:")
#        print(filepath)
#        content = read_html_file(filepath)
#
#        print("REDACTING...")
#        redacted = redact_tbody(content)
#
#        print("WRITING TO FILE:")
#        print(os.path.abspath(redacted_filepath))
#        write_html_file(redacted_filepath, redacted)
#        #write_html_file(redacted_filepath.replace(".mhtml",".html"), redacted)
#
#        webbrowser.open("file://" + os.path.abspath(redacted_filepath))
#        #webbrowser.open("file://" + os.path.abspath(redacted_filepath.replace(".mhtml",".html")))
#
