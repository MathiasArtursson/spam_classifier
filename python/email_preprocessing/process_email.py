from bs4 import BeautifulSoup
import re
from nltk.stem import PorterStemmer


def remove_header(string_in):
    """Removes header from string"""
    end_of_header_found = False
    for i in range(1, len(string_in)):
        # Search for two newlines in a row, indicating the end of a header
        if string_in[i-1] == "\n" and string_in[i] == "\n":
            end_of_header_found = True
        # If the end of header is found, and a string is found which is not a new line or space
        if end_of_header_found and not (string_in[i] == "\n" or string_in[i] == " "):
            return string_in[i:]
    return string_in


def strip_html(string_in):
    """Strips html from string"""
    soup = BeautifulSoup(string_in, features="html.parser")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    return text


def process(string_in):
    """Processes email string and returns words stemmed separated by a newline"""
    email_contents = string_in.lower()

    email_contents = remove_header(email_contents)

    email_contents = strip_html(email_contents)

    # newline fix
    email_contents = email_contents.replace("=\n", "")

    # Http addresses corrected
    # Replace occurrence of "http" or "https" + "://" + zero or all following (*) non-white-space characters [^\s]
    # to "httpaddr"
    email_contents = re.sub('(http|https)://[^\\s]*', ' httpaddr ', email_contents)

    # Email addresses corrected
    # Replace occurrence of at least one (+) non-white-space character [^\s] + "@" +
    # at least one (+) non-white-space character [^\s], into "emailaddr"
    email_contents = re.sub('[^\\s]+@[^\\s]+', ' emailaddr ', email_contents)

    # Dollar sign correction
    email_contents = re.sub('[$]+', ' dollar ', email_contents)

    # Number correction
    email_contents = re.sub('[0-9]+', ' number ', email_contents)

    # Replace symbols which are not a-z or non-white-space character \s with " "
    email_contents = re.sub('[^a-z\\s]', ' ', email_contents)

    # Create list of stemmed words using Porter Stemmer
    email_words = []
    ps = PorterStemmer()
    for word in re.split('[\\s]', email_contents):
        if len(word):
            email_words.append(ps.stem(word))
    return "\n".join(email_words)




