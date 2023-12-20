import pytest
 
hardware = "cn0556"
classname = "adi.cn0556"
 
 
#########################################
@pytest.mark.iio_hardware(hardware, True)
@pytest.mark.parametrize("classname", [(classname)])
@pytest.mark.parametrize(
    "attr, start, stop, step, tol, param_set",
    [
        ("sample_rate", 10, 19200, 10, 10, 4, 19200),
        ("rx_enabled_channels", 0, 4, 8, 10, 12, 14),
        ("in_scale", 11, 40, 1, 1, 3, 11),
    ],
)
def test_cn0556_attr(
    test_attribute_single_value,
    iio_uri,
    classname,
    attr,
    start,
    stop,
    step,
    tol,
    param_set,
):
    test_attribute_single_value(
        iio_uri, classname, attr, start, stop, step, tol, param_set
    )
 
 
#########################################
@pytest.mark.iio_hardware(hardware, True)
@pytest.mark.parametrize("classname", [(classname)])
@pytest.mark.parametrize(
    "attr, max_pow, tol", [("rx_buffer_size", 12, 10),],
)
def test_cn0556_attr_pow2(
    test_attribute_single_value_pow2, iio_uri, classname, attr, max_pow, tol
):
    test_attribute_single_value_pow2(iio_uri, classname, attr, max_pow, tol)
 
 
#########################################
@pytest.mark.iio_hardware(hardware, True)
@pytest.mark.parametrize("classname", [(classname)])
@pytest.mark.parametrize(
    "attr, value, tol",
    [
        ("rx_output_type", "SI", 1),
        ("rx_output_type", "raw", 1),
       
        ("voltage019_in_range", "+/-13.75", 1),
        ("voltage019_in_range", "+27.5", 1),
        ("voltage019_in_range", "+2.5", 1),
 
        ("voltage119_in_range", "+/-13.75", 1),
        ("voltage119_in_range", "+27.5", 1),
        ("voltage119_in_range", "+2.5", 1),
 
        ("voltage219_in_range", "+/-13.75", 1),
        ("voltage219_in_range", "+27.5", 1),
        ("voltage219_in_range", "+2.5", 1),
 
        ("voltage319_in_range", "+/-13.75", 1),
        ("voltage319_in_range", "+27.5", 1),
        ("voltage319_in_range", "+2.5", 1),
 
        ("voltage419_in_range", "+/-13.75", 1),
        ("voltage419_in_range", "+27.5", 1),
        ("voltage419_in_range", "+2.5", 1),
 
        ("voltage519_in_range", "+/-13.75", 1),
        ("voltage519_in_range", "+27.5", 1),
        ("voltage519_in_range", "+2.5", 1),
 
        ("voltage619_in_range", "+/-13.75", 1),
        ("voltage619_in_range", "+27.5", 1),
        ("voltage619_in_range", "+2.5", 1),
 
        ("voltage719_in_range", "+/-13.75", 1),
        ("voltage719_in_range", "+27.5", 1),
        ("voltage719_in_range", "+2.5", 1),
 
        ("voltage819_in_range", "+/-13.75", 1),
        ("voltage819_in_range", "+27.5", 1),
        ("voltage819_in_range", "+2.5", 1),
 
        ("voltage919_in_range", "+/-13.75", 1),
        ("voltage919_in_range", "+27.5", 1),
        ("voltage919_in_range", "+2.5", 1),
 
        ("voltage1019_in_range", "+/-13.75", 1),
        ("voltage1019_in_range", "+27.5", 1),
        ("voltage1019_in_range", "+2.5", 1),
 
        ("voltage1119_in_range", "+/-13.75", 1),
        ("voltage1119_in_range", "+27.5", 1),
        ("voltage1119_in_range", "+2.5", 1),
 
        ("voltage1219_in_range", "+/-13.75", 1),
        ("voltage1219_in_range", "+27.5", 1),
        ("voltage1219_in_range", "+2.5", 1),
 
        ("voltage1319_in_range", "+/-13.75", 1),
        ("voltage1319_in_range", "+27.5", 1),
        ("voltage1319_in_range", "+2.5", 1),
 
        ("voltage1419_in_range", "+/-13.75", 1),
        ("voltage1419_in_range", "+27.5", 1),
        ("voltage1419_in_range", "+2.5", 1),
 
        ("voltage1519_in_range", "+/-13.75", 1),
        ("voltage1519_in_range", "+27.5", 1),
        ("voltage1519_in_range", "+2.5", 1),
               
    ],
)
def test_cn0556_attr_string(
    test_attribute_single_value_str, iio_uri, classname, attr, value, tol
):
    test_attribute_single_value_str(iio_uri, classname, attr, value, tol)
 