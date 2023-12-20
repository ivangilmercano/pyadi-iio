import adi
from adi.attribute import attribute
 
class cn0556(adi.cn0554):
 
    """The CN0556 class inherits features from the CN0554 (providing full
    control and monitoring of the input and output voltages and currents)
    and the one_bit_adc_dac (sets the mode of the regulator to either Buck
    or Boost and enables and disables the LT8228). These combined
    functionalities are utilized for a Programmable High Current and
    Voltage Source/Sink Power Supply.
 
    parameters:
        uri: type=string
            URI of the platform
    """
 
    def __init__(self, uri='ip:analog.local'):
        adi.cn0554.__init__(self, uri=uri)
        self.gpio = adi.one_bit_adc_dac(uri=uri)
 
        # Enable ADC Channels for reading Voltage and Current Monitoring, INTVCC, SHARE
        self.rx_enabled_channels = [0, 4, 8, 10, 12, 14]
        self.adc_scale = self.adc.channel[0].scale
 
    @property
    def drxn(self):
        """drxn: type=int
        Operating mode of the board. Options are:
        1 (Buck Mode), 0 (Boost Mode)."""  
        return self.gpio.gpio_drxn
   
    @drxn.setter
    def drxn(self, value):
        if value == 1:
            mode = "\nBUCK MODE"
           
        elif value  == 0:
            mode = "\nBOOST MODE"
        elif value != 1 and value != 0:
            mode = "\nWRONG INPUT"
            raise Exception("Invalid Input. Valid values are '1' for Buck Mode and '0' for Boost Mode")
        print(mode)
 
        self.gpio.gpio_drxn = value
 
    @property
    def enable(self):
        """enable: type=boolean
        Enables the LT8228 device when True. When set to false, device is disabled, DAC outputs set to 0, and sets the DRXN to boost mode."""        
        return self.gpio.gpio_en
   
    @enable.setter
    def enable(self, value):
        if value:
            self.gpio.gpio_en = 1
        else:
            self.dac.voltage0.volt = 0
            self.dac.voltage2.volt = 0
            self.dac.voltage4.volt = 0
            self.dac.voltage6.volt = 0
            self.dac.voltage8.volt = 0
            self.dac.voltage10.volt = 0
            self.dac.voltage12.volt = 0
            self.dac.voltage14.volt = 0
            self.output_enable = 0  
            self.drxn = 0
 
    def measure_intvcc_volt(self):
        """measure_intvcc_volt: type=float
            read voltage at INTVCC pin
        """
        raw = self.adc.channel[10].raw
        return raw * self.adc_scale  / 100
   
    def measure_share_volt(self):
        """measure_share_volt: type=float
            read voltage at SHARE pin
        """
        raw = self.adc.channel[12].raw
        return raw * self.adc_scale  / 100
 
    @property
    def report(self):
        """report: type=bool
            read data stream at REPORT pin
        """
        return self.gpio.gpio_report
 
    @property
    def fault(self):
        """fault: type=bool
            Check if a fault is present. True if a fault occured.
        """
        return self.gpio.gpio_fault
   
    @property
    def buck_output_voltage(self):
        """buck_output_voltage: type=float
            Read buck output voltage at V2 side
        """
        raw = self.adc.channel[4].raw
        v2_adc = raw * self.adc_scale  / 100
        return v2_adc*(51000/10000)
 
    @buck_output_voltage.setter
    def buck_output_voltage(self, value):
        """set_buck_output_volt: set buck output voltage at V2 side. Valid values are 2 to 14.
       
        parameters:
            value: type=float
                Desired buck output voltage set by user
        """
       
        output = (((15.685 - value)) / 1.4666)
        # The formula was derived using the resistor divider network at FB2 (RFB2A, RFB2B, and RFB2_CTL).
        # Please refer to the discussion under the "Setting the Buck Output Voltage" section in the CN0556 Circuit Note.
       
        if value < 2 or value > 14:
            raise Exception("Buck Output Voltage Limit is only from 2 to 14 volts ")
       
        self.dac.voltage2.volt = output * 1000.0
 
    @property
    def buck_input_voltage(self):
        """buck_input_voltage: type=float
            read buck input voltage at V1 side
        """
        raw = self.adc.channel[14].raw
        v1_adc = raw * self.adc_scale  / 100
        return v1_adc*(243000/10000)
 
    @property
    def buck_output_current(self):
        """buck_output_current: type=float
            read buck output current at V2 side
        """
        raw = self.adc.channel[8].raw
        vmon2 = raw * self.adc_scale  / 100
        return (vmon2 * self.R_in2) / (self.R_mon2 * self.R_sns2)
 
    @property
    def buck_input_current(self):
        """buck_input_current: type=float
            read buck input current at V1 side
        """
        raw = self.adc.channel[0].raw
        vmon1 = raw * self.adc_scale  / 100
        return (vmon1 * self.R_in1) / (self.R_mon1 * self.R_sns1)
 
    @property
    def buck_input_undervoltage(self):
        """buck_input_undervoltage: type=float
        Buck input undervoltage V1 side. Valid values are 12 to 54.
        """
        return 60.415 - (self.dac.voltage4.volt * 5.1281 / 1000.0)
 
    @buck_input_undervoltage.setter
    def buck_input_undervoltage(self, value):
       
        output = (((60.415 - value)) / 5.1281)
        # The formula was derived using the resistor divider network at UV1 (RUV1A, RUV1B, and RUV1_CTL).
        # Please refer to the discussion under the "Setting the V1 Buck Input Undervoltage" section in the CN0556 Circuit Note.
 
        if value < 12 or value > 54:
            raise Exception("Buck Input Undervoltage Limit is only from 12 to 54 volts ")
       
        self.dac.voltage4.volt = output * 1000.0
 
    @property
    def buck_input_current_limit(self):
        """buck_input_current_limit: type=float
            Buck input current limit V1 side. Valid values are 0.07 to 10.
        """
        return 11.345 - (self.dac.voltage8.volt * 1.1274 / 1000.0)
 
    @buck_input_current_limit.setter
    def buck_input_current_limit(self, value):
        output = (((11.345 - value)) / 1.1274)
        # The formula was derived using the resistor divider network at ISET1P (R1P and RCTL1P).
        # Please refer to the discussion under the "Setting the Buck Input and Output Current Limit" section in the CN0556 Circuit Note.
 
        if value < 0.07 or value > 10:
            raise Exception("Buck Input Current Limit is only from 0.07 to 10 A ")
       
        self.dac.voltage8.volt = output * 1000.0
 
    @property
    def buck_output_current_limit(self):
        """buck_output_current_limit: type=float
            Buck output current limit V2 side. Valid values are 0.16 to 35.
        """
        return 39.623 - (self.dac.voltage8.volt * 4.0108 / 1000.0)
 
    @buck_output_current_limit.setter
    def buck_output_current_limit(self, value):
        output = (((39.623 - value)) / 4.0108)
        # The formula was derived using the resistor divider network at ISET2P (R2P and RCTL2P).
        # Please refer to the discussion under the "Setting the Buck Input and Output Current Limit" section in the CN0556 Circuit Note.
 
        if value < 0 or value > 35:
            raise Exception("Buck Output Current Limit is only from 0 to 35 A ")
       
        self.dac.voltage12.volt = output * 1000.0
 
    """The functions below are for the control and monitoring of
    the input and output voltages and currents in Boost Mode.
    """
 
    def set_boost_output_volt(self, value):
        """set_boost_output_volt: set boost output voltage at V1 side. Valid values are 14 to 56.
       
        parameters:
            value: type=float
                Desired boost output voltage set by user
        """
       
        output = (((61.995 - value)) / 4.859)
        # The formula was derived using the resistor divider network at FB1 (RFB1A, RFB1B, and RFB1_CTL).
        # Please refer to the discussion under the "Setting the Boost Output Voltage" section in the CN0556 Circuit Note.
 
        if value < 14 or value > 56:
            raise Exception("Boost Output Voltage Limit is only from 14 to 56 volts ")
       
        self.dac.voltage0.volt = output * 1000.0
 
   
    def set_boost_input_undervolt(self, value):
        """set_boost_input_undervolt: set boost input undervoltage V2 side. Valid values are 8 to 14.
       
        parameters:
            value: type=float
                Desired boost input under voltage set by user
        """
       
        output = (((13.386 - value)) / 1.2195)
        # The formula was derived using the resistor divider network at UV2 (RUV2A, RUV2B, and RUV2_CTL).
        # Please refer to the discussion under the "Setting the V2 Boost Input Undervoltage" section in the CN0556 Circuit Note.
 
        if value < 8 or value > 12:
            raise Exception("Boost Input Undervoltage Limit is only from 8 to 12 volts ")
       
        self.dac.voltage6.volt = output * 1000.0
 
 
    def set_boost_input_current_lim(self, value):
        """set_boost_input_current_lim: set boost input current limit V2 side. Valid values are 0 to 35.
       
        parameters:
            value: type=float
                Desired boost input current limit set by user
        """
       
        output = (((39.623 - value)) / 4.0108)
        # The formula was derived using the resistor divider network at ISET2N (R2N and RCTL2N).
        # Please refer to the discussion under the "Setting the Boost Input and Output Current Limit" section in the CN0556 Circuit Note.
 
        if value < 0 or value > 35:
            raise Exception("Boost Input Current Limit is only from 0 to 35 A ")
       
        self.dac.voltage14.volt = output * 1000.0
   
    def set_boost_output_current_lim(self, value):
        """set_boost_output_current_lim: set boost output current limit V1 side. Valid values are 0.07 to 10.
       
        parameters:
            value: type=float
                Desired boost output current limit set by user
        """
       
        output = (((11.345 - value)) / 1.1274)
        # The formula was derived using the resistor divider network at ISET1N (R1N and RCTL21).
        # Please refer to the discussion under the "Setting the Boost Input and Output Current Limit" section in the CN0556 Circuit Note.
 
        if value < 0.07 or value > 10:
            raise Exception("Boost Output Current Limit is only from 0.07 to 10 A ")
       
        self.dac.voltage10.volt = output * 1000.0
 
    def measure_boost_output_volt(self):
        """measure_boost_output_volt: type=float
            read boost output voltage at V1 side
        """
        raw = self.adc.channel[14].raw
        v1_adc = raw * self.adc_scale  / 100
        boost_out_volt = v1_adc*(243000/10000)
 
        return boost_out_volt
   
    def measure_boost_input_volt(self):
        """measure_boost_input_volt: type=float
            read boost input voltage at V2 side
        """
        raw = self.adc.channel[4].raw
        v2_adc = raw * self.adc_scale  / 100
        boost_in_volt = v2_adc*(51000/10000)
 
        return boost_in_volt
   
    def measure_boost_output_current(self):
        """measure_boost_output_current: type=float
            read boost output current at V1 side
        """
        raw = self.adc.channel[0].raw
        vmon1 = raw * self.adc_scale  / 100
        boost_out_current = (vmon1 * self.R_in1) / (self.R_mon1 * self.R_sns1)
       
        return boost_out_current
   
    def measure_boost_input_current(self):
        """measure_boost_input_current: type=float
            read boost input current at V2 side
        """
        raw = self.adc.channel[8].raw
        vmon2 = raw * self.adc_scale  / 100
        boost_in_current = (vmon2 * self.R_in2) / (self.R_mon2 * self.R_sns2)
       
        return boost_in_current




