import time
from adi import cn0540
import matplotlib.pyplot as plt
import numpy as np

# board configuration
adc = cn0540.cn0540(uri='ip:169.254.7.18')

adc.sw_cc = 1
adc.fda_disable_status = 1
adc.fda_mode = 'full-power'
adc.monitor_powerup = 0

if 