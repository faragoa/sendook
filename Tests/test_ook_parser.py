from sendook import parse_code
import pytest

# TESTS pytest


def test_parse_code_none_expectempty():
    code = None
    assert(parse_code(code) == [])


def test_parse_code_empty_expectempty():
    code = ""
    assert(parse_code(code) == [])


def test_parse_code_one1():
    assert(parse_code("1") == [[1, 1]])


def test_parse_code_two1():
    assert(parse_code("11") == [[1, 2]])


def test_parse_code_10():
    assert(parse_code("10") == [[1, 1], [0, 1]])


def test_parse_code_comment():
    assert(parse_code("1  1") == [[1, 2]])


def test_parse_code_comment_and_change():
    assert(parse_code("1  0") == [[1, 1], [0, 1]])


def test_parse_code_fullcomment_expectempty():
    assert(parse_code("     ") == [])


def test_parse_code_10001():
    assert(parse_code("10001") == [[1, 1], [0, 3], [1, 1]])


def test_parse_code_removecommentsproperly():
    signal1 = "11100WITHACOMMENTHERE100100100101001001001001001100110010111011101001SOMETHING"
    signal2 = "ASIMPLECOMMENT1110010010010010100100ANDACOMMENTTHERE100100100110011ANDSOMEEXTRACOMMENT0010111011101001"
    code1 = parse_code(signal1)
    code2 = parse_code(signal2)

    assert([1, 3] in code1)
    assert([1, 2] in code1)
    assert(code1 == code2)
