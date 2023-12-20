import adi
import pytest

hardware = "cn0565"
classname = "adi.cn0565"


#########################################
@pytest.mark.iio_hardware(hardware, True)
@pytest.mark.parametrize("classname", [(classname)])
@pytest.mark.parametrize(
    "attr, start, stop, step, tol",
    [
        #gpio set pins, i think okay na to
        ("drxn", 0, 1, 1, 1),
        ("enable", 0, 1, 1, 1),
        ("buck_output_voltage", 2, 14, 1, 1),
        ("buck_input_undervoltage", 12, 54, 1, 1),
        ("buck_input_current_limit", 0.07, 10, 1, 0.01),
        ("buck_output_current_limit", 0, 35, 1, 1),
    ],
)
def test_cn0565_attr(
    test_attribute_single_value,
    iio_uri,
    classname,
    attr,
    start,
    stop,
    step,
    tol,
):
    test_attribute_single_value(
        iio_uri, classname, attr, start, stop, step, tol
    )

#########################################
@pytest.mark.iio_hardware(hardware, True)
@pytest.mark.parametrize("classname", [(classname)])
@pytest.mark.parametrize(
    "attr, lower, upper, repeat",
    [
        ("report", 0, 1, 1, 1),
        ("fault", 0, 1, 1, 1),
        ("measure_intvcc_volt", 0, 4, 1, 1 ),
        ("measure_share_volt", 0, 4, 1, 1),
        ("buck_input_voltage", 14, 56, 1, 1),
        ("buck_output_current", 0, 35, 1, 1),
        ("buck_input_current", 0.07, 10, 1, 1),
        ("boost_output_voltage", 14, 56, 1, 1), 
        ("boost_input_undervolt", 0, 1, 1, 1),
        ("boost_input_current_lim", 0, 1, 1, 1),
        ("boost_output_current_lim", 0, 1, 1, 1),
        ("measure_boost_output_volt", 0, 1, 1, 1),
        ("measure_boost_input_volt", 0, 1, 1, 1),
        ("measure_boost_output_current", 0, 1, 1, 1),
        ("measure_boost_input_current", 0, 1, 1, 1),
    ]
)
def test_cn0565_attr(
    attribute_single_value_readonly,
    iio_uri,
    classname,
    attr,
    lower,
    upper,
    repeat,
):
    attribute_single_value_readonly(
        iio_uri, classname, attr, lower, upper, repeat
    )