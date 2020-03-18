import pytest
import library

def test_main():
    html = library.get_html(84959999999)
    assert html, 'PAGE NOT FOUND'
    parsed_html = library.parse_html(html)
    test_html = open("/home/grinningsoul/Work/Python/test/html_test.html", "r").read()
    parsed_test_html = library.parse_html(test_html)
    information = library.get_information(parsed_html)
    test_information = library.get_information(parsed_test_html)
    assert information == test_information, 'FAILED'