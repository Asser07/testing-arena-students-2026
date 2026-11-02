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

def test_parse_time_midnight():
    assert parse_time("00:00") ==0 and parse_time("23:59") == 1439

def test_parse_time_zero_padded_time():
    assert parse_time("09:05") == 545 and parse_time("9:5") == 545 and parse_time("09:5") == 545 and parse_time("9:05") == 545

def test_parse_time_invalid():
    try:
        parse_time("24:00")
    except ValueError:
        pass
    try: 
        parse_time("12:60")
    except ValueError:
        pass


def test_parse_measurement_regular_line():
    assert parse_measurement("Köln;14:21;21.7") == ("Köln", 861, 21.7)

def test_parse_measurement_spaces():
    assert parse_measurement("  Köln  ;  14:21  ;  21.7   ")==("Köln", 861, 21.7)

def test_parse_measurement_invalid():
    try: 
        parse_measurement("Köln;14:21")
    except ValueError:
        pass
    try : 
        parse_measurement("Köln;14:21;21.7;schön")
    except ValueError:
        pass
    try: 
        parse_measurement(";14:21;21.7")
    except ValueError:
        pass
    try: 
        parse_measurement("Köln;25:00;21.7")
    except ValueError:
        pass
    try : 
        parse_measurement("Köln;14:21;abc")
    except ValueError:
        pass

def test_parse_measurement_negative_temp():
    assert parse_measurement("Köln;14:21;-5.0") == ("Köln", 861, -5.0)


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


