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

import pytest

def test_parse_time_regular_time():
    assert parse_time("14:21") == 861

def test_parse_time_midnight():
    assert parse_time("00:00") ==0 and parse_time("23:59") == 1439

def test_parse_time_zero_padded_time():
    assert parse_time("09:05") == 545 and parse_time("9:5") == 545 and parse_time("09:5") == 545 and parse_time("9:05") == 545

def test_parse_time_invalid():
    
    with pytest.raises(ValueError):
        parse_time("24:00")
    
    with pytest.raises(ValueError):
        parse_time("12:60")

    with pytest.raises(ValueError):
        parse_time("12:30:00")

    with pytest.raises(ValueError):
        parse_time("1230")

    with pytest.raises(ValueError):
        parse_time("ab:30")

    with pytest.raises(ValueError):
        parse_time("12;30")

    


def test_parse_measurement_regular_line():
    assert parse_measurement("Köln;14:21;21.7") == ("Köln", 861, 21.7)

def test_parse_measurement_spaces():
    assert parse_measurement("  Köln  ;  14:21  ;  21.7   ")==("Köln", 861, 21.7)

def test_parse_measurement_invalid():
    with pytest.raises(ValueError):
        parse_measurement("Köln;14:21")

    with pytest.raises(ValueError):
        parse_measurement("Köln;14:21;21.7;schön")

    with pytest.raises(ValueError):
        parse_measurement(";14:21;21.7")

    with pytest.raises(ValueError):
        parse_measurement("    ;14:21;21.7")

    with pytest.raises(ValueError):
        parse_measurement("Köln;25:00;21.7")

    with pytest.raises(ValueError):
        parse_measurement("Köln;14:21;abc")

    with pytest.raises(ValueError):
        parse_measurement(123)

    
    

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

def test_filter_by_temperature_lower_boundry():
    measurements = [
        ("Köln", 600, 10.0),
        ("Düsseldorf", 720, 18.5),
        ("Bonn", 900, 25.0),
    ]
    assert filter_by_temperature(measurements,10.0,15.0)==[("Köln", 600, 10.0)]

def test_filter_by_temperature_higher_boundry():
    measurements=  [
        ("Köln", 600, 10.0),
        ("Düsseldorf", 720, 18.5),
        ("Bonn", 900, 25.0),
    ]
    assert filter_by_temperature(measurements,20.0,25.0)==[("Bonn", 900, 25.0)]

def test_filter_by_temperature_equal_boudry():
    measurements=  [
            ("Köln", 600, 10.0),
            ("Düsseldorf", 720, 18.5),
            ("Bonn", 900, 25.0),
        ]
    assert filter_by_temperature(measurements,18.5,18.5)==[("Düsseldorf", 720, 18.5)]

def test_filter_by_temperature_equal_temp():
    measurements=  [
                ("Köln", 600, 25.0),
                ("Düsseldorf", 720, 18.5),
                ("Bonn", 900, 25.0),
            ]
    assert filter_by_temperature(measurements,20.0 , 25.0)==[("Köln", 600, 25.0),("Bonn", 900, 25.0)]

def test_filter_temperature_invalid_boudry():
    measurements=  [
                ("Köln", 600, 10.0),
                ("Düsseldorf", 720, 18.5),
                ("Bonn", 900, 25.0),
            ]
    with pytest.raises(ValueError): 
        filter_by_temperature(measurements,30.0,10.0)
    

def test_filter_temperature_notfound():
    measurements=  [
                ("Köln", 600, 10.0),
                ("Düsseldorf", 720, 13.5),
                ("Bonn", 900, 15.0),
            ]
    assert filter_by_temperature(measurements,20.0,22.5 )==[]


def test_filter_temperature():
    measurements=[]
    assert filter_by_temperature(measurements,10.0,25.0)==[]

def test_average_temperature_regular_values():
    measurements = [
        ("Köln", 600, 10.0),
        ("Köln", 720, 20.0),
    ]

    assert average_temperature(measurements, "Köln") == 15.0

def test_average_temperature_different_cities():
    measurements=  [
                    ("Köln", 600, 10.0),
                    ("Düsseldorf", 720, 13.5),
                    ("Köln", 720, 20.0),
                ]
    assert average_temperature(measurements, "Köln") == 15.0

def test_average_temperature_invalid_city():
    measurements=  [
                        ("Köln", 600, 10.0),
                        ("Düsseldorf", 720, 13.5),
                        ("köln", 720, 20.0),
                    ]
    assert average_temperature(measurements, "Köln") == 10.0
    
def test_average_temperature_notfound_city():
    measurements= [
                        ("Köln", 600, 10.0),
                        ("Düsseldorf", 720, 13.5),
                        ("Köln", 720, 20.0),
                    ]
    with pytest.raises(ValueError):
        average_temperature(measurements, "Bonn")
    

def test_average_temperature_empty_list():
    measurements=[]
    with pytest.raises(ValueError):
        average_temperature(measurements,"Düsseldorf")

def test_average_temperature_full_list():
    measurements= [("Köln", 600, 10.0),
                    ("Köln", 600, 10.0),
                    ("Düsseldorf", 720, 13.5),
                    ("Köln", 720, 20.0),]
    assert average_temperature(measurements,"Köln")==40/3

def test_hottest_measurement_with_unique_maximum():
    measurements = [
        ("Köln", 600, 10.0),
        ("Düsseldorf", 720, 25.0),
        ("Bonn", 900, 20.0),
    ]

    assert hottest_measurement(measurements) == ("Düsseldorf", 720, 25.0)

def test_hottest_measurement_with_same_maximum():
    measurements = [
            ("Köln", 600, 10.0),
            ("Düsseldorf", 850, 25.0),
            ("Bonn", 900, 20.0),
            ("Berlin",750,25.0)
        ]
    assert hottest_measurement(measurements)==("Berlin", 750, 25.0)

<<<<<<< HEAD
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
=======
def test_hottest_measurement_with_same_values():
    measurements = [
                ("Köln", 600, 10.0),
                ("Düsseldorf", 720, 25.0),
                ("Bonn", 900, 20.0),
                ("Berlin",720,25.0)
            ]
    assert hottest_measurement(measurements)==("Düsseldorf", 720, 25.0)

def test_hottest_temperature_empty_list():
    measurements= []
    with pytest.raises(ValueError):
        hottest_measurement(measurements)
    

def test_hottest_temperature_single_list():
    measurements=[("Köln", 600, 10.0)]
    assert hottest_measurement(measurements)==("Köln", 600, 10.0)

def test_hottest_temperature_negative_values():
    measurements=[
        ("Köln", 600, -10.0),
        ("Düsseldorf", 720, -25.0),
        ("Bonn", 900, -20.0),
    ]
    assert hottest_measurement(measurements)==("Köln",600,-10)


def test_hottest_no_modification():
    measurements = [
        ("Köln", 600, 10.0),
        ("Bonn", 700, 25.0),
        ("Berlin", 800, 20.0)
    ]
>>>>>>> Asser07

    original = measurements.copy()

<<<<<<< HEAD
def test_line_time():
    line = parse_measurement("Köln;14:21;21.7")
    assert line[1] is not None
    assert str(line[1]) == "861"
=======
    hottest_measurement(measurements)

    assert measurements == original
>>>>>>> Asser07
