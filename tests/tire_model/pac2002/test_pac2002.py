import sys
import os

# Add the root directory of your project to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from src.TireModel.solvermode import SolverMode
from src.Core import TireState
from src.TireModel.PAC2002 import PAC2002
import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

import numpy as np

# Initialize tire model and state
tire = PAC2002()
state = TireState()
state.P = 260000
state.IA = 0
state.SR = 0
state.V = 10

# Define parameters
vertical_loads = [1000, 1500, 2000]
slip_angles = np.arange(-12, 12, 0.1) * np.pi / 180

# Prepare data for plotting
lateral_forces = []
for fz in vertical_loads:
    state.FZ = fz
    lateral_force = []
    for sa in slip_angles:
        state.SA = sa
        current_state = tire.solve(state, SolverMode.PureFy)
        lateral_force.append(current_state.FY)
        print(current_state.FY)
    lateral_forces.append(lateral_force)

# Create a figure and axes
fig, ax = plt.subplots()

# Plot results
for i, fz in enumerate(vertical_loads):
    ax.plot(slip_angles, lateral_forces[i], label=f"FZ = {fz}")

# Add labels, legend, and grid
ax.set_xlabel("Slip Angle (rad)")
ax.set_ylabel("Lateral Force (N)")
ax.set_title("Lateral Force vs Slip Angle for Various Vertical Loads")
ax.legend()
ax.grid()

# Display the plot
plt.show()


# Prepare data for plotting
aligning_moments = []
for fz in vertical_loads:
    state.FZ = fz
    aligning_moment = []
    for sa in slip_angles:
        state.SA = sa
        current_state = tire.solve(state, SolverMode.PureMz)
        aligning_moment.append(current_state.MZ)
        print(current_state.MZ)  # Print Mz for debugging
    aligning_moments.append(aligning_moment)

# Create a figure and axes
fig, ax = plt.subplots()

# Plot results
for i, fz in enumerate(vertical_loads):
    ax.plot(slip_angles, aligning_moments[i], label=f"FZ = {fz}")

# Add labels, legend, and grid
ax.set_xlabel("Slip Angle (rad)")
ax.set_ylabel("Aligning Moment (N·m)")
ax.set_title("Aligning Moment vs Slip Angle for Various Vertical Loads")
ax.legend()
ax.grid()

# Display the plot
plt.show()
