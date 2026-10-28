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
    line="Köln;14:21;21.7"
    assert isinstance(line, str)

def test_line_measurement():
    line=" Düsseldforf;14:21;21.7            "
    l=line.strip().split(";")
    assert len(l)==3
    assert isinstance(l[0], str)
    assert isinstance(l[1], float)
    assert isinstance(l[2], float)

def test_line_city():
    line="  ;14:21;21.7            "
    l=line.strip().split(";")
    assert l[0]!=""


def test_line_time():
    line="sfax;25:655;6520"
    l=line.strip().split(";")
    assert l[1]!= None
    assert l[1].count(":")==1
    assert l[1].split(":")[0] in range(0,23)
    assert l[1].split(":")[1] in range(0,59)


