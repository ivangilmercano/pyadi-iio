from adi import cn0540

adc = cn0540.cn0540(uri='ip:169.254.7.18')

adc.sw_cc = 1
adc.fda_disable_status = 0
adc.fda_mode = 'full-power'
adc.monitor_powerup = 1

adc.shift_voltage = 4057

print(f'fault flag = {adc.sw_ff_status}')
print(f'adc.input_voltage = {adc.input_voltage}')
print(f'adc.shift_voltage = {adc.shift_voltage}')
print(f'adc.sensor_voltage = {adc.sensor_voltage}')
print(adc.rx())