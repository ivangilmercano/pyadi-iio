import adi

# CN0565 connect parameters
port = "COM8"
baudrate = 230400
real = 0
imaginary = 1
cn0565 = adi.cn0565(uri=f"serial:{port},{baudrate},8n1") 

#CN0565 operation parameters
amplitude = 100
frequency = 10000

cn0565.gpio1_toggle = True
cn0565.excitation_amplitude = amplitude
cn0565.excitation_frequency = frequency
cn0565.magnitude_mode = False
cn0565.impedance_mode = True

cn0565.electrode_count = 8
cn0565.force_distance = 1
cn0565.sense_distance = 1

cn0565.add(0x71)
cn0565.add(0x70)

cn0565.immediate = True

voltages = cn0565.all_voltages

real = voltages[:, 0]
imaginary = voltages[:, 1]

print("Test board no.1")
print(f"number of electrodes: {cn0565.electrode_count}")
print("--------------- REAL -----------------")
print(real)
print("--------------- IMAGINARY -----------------")
print(imaginary)