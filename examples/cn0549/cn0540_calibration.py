import time
from adi import cn0540
import matplotlib.pyplot as plt
import numpy as np

adc = cn0540.cn0540(uri='ip:169.254.7.18')

adc.sw_cc = 1
adc.fda_disable_status = 1
adc.fda_mode = 'full-power'
adc.monitor_powerup = 0

adc_chan = adc._rxadc
adc_scale = float(adc._get_iio_attr("voltage0", "scale", False, adc_chan))

dac_chan = adc._ltc2606
dac_scale = float(adc._get_iio_attr("voltage0", "scale", True, dac_chan))

data=[]
captures=200

for i in range(captures):
    raw_adc = adc._get_iio_attr("voltage0", "raw", False, adc_chan)
    adc_voltage = raw_adc * adc_scale

    raw_dac = adc._get_iio_attr("voltage0", "raw", True, dac_chan)
    dac_voltage = raw_dac * dac_scale

    #sensorv_oltage = adc.sensor_voltage

    if adc.input_voltage > 0:
        new_dac_setting = raw_dac - (2 ** (16 - (i + 1)))
    else:
        new_dac_setting = raw_dac + (2 ** (16 - (i + 1)))

    e = int(dac_voltage * dac_scale)

    if int(new_dac_setting) > 2 ** 16 - 1:
        print(
            "Warning: DAC voltage at upper limit, "
            + f"calibration may not converge (Error: {e-(2**16-1)} codes).\n"
            + "Make sure sensor is connected." + 'in if'
        )
        new_dac_setting = 2 ** 16 - 1
    elif int(new_dac_setting) < 0:
        print(
            "Warning: DAC voltage at lower limit, "
            + f"calibration may not converge (Error: {e} codes).\n"
            + "Make sure sensor is connected.")
        new_dac_setting = 0
    

    print(f"dac_voltage= {dac_voltage}")

    adc._set_iio_attr_float("voltage0", "raw", True, int(new_dac_setting), dac_chan)
    print('input voltage', adc.input_voltage)
    data.append(adc.input_voltage)
    plt.clf()
    plt.xlabel('captures')
    plt.ylabel('sensor voltage')
    plt.plot(data)
    plt.show(block=False)
    plt.pause(0.1)

print('max: ',max(data))
print('min: ',min(data))
