

# for now we will use the saved HTML file instead of a live page we browsed to

#import email
#
#def read_html_file(html_filepath):
#    with open(html_filepath, 'r', encoding='utf-8') as f:
#        return f.read()
#
#def read_and_parse_saved_page(html_filepath):
#    page_source = read_html_file(html_filepath)
#
#    html_content = None
#    if page_source:
#        message = email.message_from_string(page_source)
#
#        for part in message.walk():
#            if part.get_content_type() == 'text/html':
#                html_content = part.get_payload(decode=True)  # Decoding from quoted-printable encoding
#                break
#
#    return html_content
#


#SEARCH_PAGE_1_FILEPATH = os.path.join(____, "________.mhtml")
#def test_search_box_part_1():
