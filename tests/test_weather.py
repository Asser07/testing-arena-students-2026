"""Starter tests for the weather module.

These tests deliberately cover only ordinary examples. They show how pytest works,
but they are not a sufficient test suite for the specification in SPECIFICATION.md.
"""

from weather import (
    average_temperature,
    filter_by_temperature,
    hottest_measurement,
    parse_measurement,
    parse_time,
)


def test_parse_time_regular_time():
    assert parse_time("14:21") == 861


def test_parse_measurement_regular_line():
    assert parse_measurement("Köln;14:21;21.7") == ("Köln", 861, 21.7)


def test_filter_by_temperature_regular_values():
    measurements = [
        ("Köln", 600, 10.0),
        ("Düsseldorf", 720, 18.5),
        ("Bonn", 900, 25.0),
    ]

    assert filter_by_temperature(measurements, 15.0, 20.0) == [
        ("Düsseldorf", 720, 18.5)
    ]


def test_average_temperature_regular_values():
    measurements = [
        ("Köln", 600, 10.0),
        ("Köln", 720, 20.0),
    ]

    assert average_temperature(measurements, "Köln") == 15.0


def test_hottest_measurement_with_unique_maximum():
    measurements = [
        ("Köln", 600, 10.0),
        ("Düsseldorf", 720, 25.0),
        ("Bonn", 900, 20.0),
    ]

    assert hottest_measurement(measurements) == ("Düsseldorf", 720, 25.0)


def test_line_type():
    line = parse_measurement("Köln;14:21;21.7")
    assert isinstance(line, (tuple, list))


def test_line_measurement():
    line = parse_measurement("Köln;14:21;21.7")
    assert len(line) == 3
    assert isinstance(line[0], str)
    assert isinstance(line[2], float)
    assert line[2] == 21.7


def test_line_city():
    line = parse_measurement("Köln;14:21;21.7")
    assert line[0] == "Köln"


def test_line_time():
    line = parse_measurement("Köln;14:21;21.7")
    assert line[1] is not None
    assert str(line[1]) == "861"