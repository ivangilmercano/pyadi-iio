import adi
import matplotlib.pyplot as plt
import numpy as np
import pyeit.eit.bp as bp
import pyeit.eit.protocol as protocol
import pyeit.mesh as mesh
import time

port = "COM6"
baudrate = 230400
real = 0
imaginary = 1
cn0565 = adi.cn0565(uri=f"serial:{port},{baudrate},8n1") #you can change this part based on the comport you are using (˶ᵔ ᵕ ᵔ˶)

cn0565.gpio1_toggle = True
cn0565.excitation_amplitude = 100
cn0565.excitation_frequency = 10000
cn0565.magnitude_mode = False
cn0565.impedance_mode = True

cn0565.immediate = True

cn0565.add(0x71)
cn0565.add(0x70)

cn0565.electrode_count = 16
cn0565.force_distance = 1
cn0565.sense_distance = 1

#creating the mesh for the plot
mesh = mesh.create(cn0565.electrode_count, h0=0.08)
protocol = protocol.create(cn0565.electrode_count, dist_exc=1, step_meas=1, parser_meas="std")
eit = bp.BP(mesh, protocol)
eit.setup(weight="none")
points = mesh.node
triangle = mesh.element

plt.ion()
fig, ax = plt.subplots(constrained_layout=True, figsize = (6, 4))

initial_data = True
ds = None
im = None
cbar = None

while True:
    voltages = cn0565.all_voltages
    current_data = voltages[:, imaginary]

    if initial_data:
        v0 = current_data
        if np.any(np.isnan(v0)):
            print(f"no. of electrodes: {cn0565.electrode_count}")
            print("Invalid baseline (NaN or zeros). Retrying...")
            print(v0)
            break
        else:
            initial_data = False
            print(f"no. of electrodes: {cn0565.electrode_count}")
            print("Valid baseline acquired.")
            continue

    v1 = current_data
    ## get average of v0 -> print
    ## get average of v1 -> print
    ds = 192.0 * eit.solve(v1, v0, normalize=True)

    if im is None:
        print("plotting...")
        im = ax.tripcolor(points[:, 0], points[:, 1], triangle, ds)
        ax.axis("equal")
        ax.set_title("Live EIT Frame")
        cbar = fig.colorbar(im, ax=ax)
    else:
        print("Updating...")
        ax.clear()
        im = ax.tripcolor(points[:, 0], points[:, 1], triangle, ds)
        ax.axis("equal")
        ax.set_title("Live EIT Frame")
        cbar.update_normal(im)
        
    plt.pause(0.1)
    time.sleep(0.1)