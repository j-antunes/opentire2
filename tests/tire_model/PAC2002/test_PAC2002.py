import sys
import os

# Add the root directory of your project to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from src.tire_models.PAC2002.PAC2002 import PAC2002


from src.core.tirestate import TireState
from src.tire_models.solvermode import SolverMode
import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

import numpy as np

# Initialize tire model and state
tire = PAC2002()
tire.createmodel()
state = TireState()
state["P"] = 260000
state["IA"] = 0
state["SR"] = 0
state["V"] = 10

# Define parameters
vertical_loads = [1000, 1500, 2000]
slip_angles = np.arange(-12, 12, 0.1) * np.pi / 180

# Prepare data for plotting
lateral_forces = []
for fz in vertical_loads:
    state["FZ"] = fz
    lateral_force = []
    for sa in slip_angles:
        state["SA"] = sa
        current_state = tire.solve(state, SolverMode.PureFy)
        lateral_force.append(current_state["FY"])
        print(current_state["FY"])
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
    state["FZ"] = fz
    aligning_moment = []
    for sa in slip_angles:
        state["SA"] = sa
        current_state = tire.solve(state, SolverMode.PureMz)
        aligning_moment.append(current_state["MZ"])
        print(current_state["MZ"])  # Print Mz for debugging
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


# Define slip ratios
slip_ratios = np.arange(-0.2, 0.2, 0.01)

# Prepare data for plotting
longitudinal_forces = []
for fz in vertical_loads:
    state["FZ"] = fz
    longitudinal_force = []
    for sr in slip_ratios:
        state["SR"] = sr
        current_state = tire.solve(state, SolverMode.PureFx)
        longitudinal_force.append(current_state["FX"])
        print(current_state["FX"])  # Print Fx for debugging
    longitudinal_forces.append(longitudinal_force)

# Create a figure and axes
fig, ax = plt.subplots()

# Plot results
for i, fz in enumerate(vertical_loads):
    ax.plot(slip_ratios, longitudinal_forces[i], label=f"FZ = {fz}")

# Add labels, legend, and grid
ax.set_xlabel("Slip Ratio")
ax.set_ylabel("Longitudinal Force (N)")
ax.set_title("Longitudinal Force vs Slip Ratio for Various Vertical Loads")
ax.legend()
ax.grid()

# Display the plot
plt.show()


# Prepare data for plotting FX-FY-SA
fx_fy_data = []
for fz in vertical_loads:
    state["FZ"] = fz
    fx_fy_per_load = []
    for sa in slip_angles:
        state["SA"] = sa
        state["SR"] = 0  # Assuming no longitudinal slip for this plot
        # Solve for both FX and FY using the 'All' solver mode
        current_state = tire.solve(state, SolverMode.All)
        fx_fy_per_load.append((current_state["FX"], current_state["FY"]))
    fx_fy_data.append(fx_fy_per_load)

# Create a figure and axes for FX-FY-SA plot
fig, ax = plt.subplots()

# Plot results
for i, fz in enumerate(vertical_loads):
    fx = [point[0] for point in fx_fy_data[i]]
    fy = [point[1] for point in fx_fy_data[i]]
    ax.plot(fx, fy, label=f"FZ = {fz} N")

# Add labels, legend, and grid
ax.set_xlabel("Longitudinal Force, FX (N)")
ax.set_ylabel("Lateral Force, FY (N)")
ax.set_title("FX vs FY for Various Slip Angles and Vertical Loads")
ax.legend()
ax.grid()

# Display the plot
plt.show()

# Prepare data for plotting FX-SA
longitudinal_forces = []
for fz in vertical_loads:
    state["FZ"] = fz
    fx_per_load = []
    for sa in slip_angles:
        state["SA"] = sa
        state["SR"] = 0  # Assuming no longitudinal slip for this plot
        # Solve for FX
        current_state = tire.solve(state, SolverMode.PureFx)
        fx_per_load.append(current_state["FX"])
    longitudinal_forces.append(fx_per_load)

# Create a figure and axes for FX-SA plot
fig, ax = plt.subplots()

# Plot results
for i, fz in enumerate(vertical_loads):
    ax.plot(
        slip_angles * 180 / np.pi,  # Convert slip angles to degrees for readability
        longitudinal_forces[i],
        label=f"FZ = {fz} N",
    )

# Add labels, legend, and grid
ax.set_xlabel("Slip Angle (°)")
ax.set_ylabel("Longitudinal Force, FX (N)")
ax.set_title("FX vs SA for Various Vertical Loads")
ax.legend()
ax.grid()

# Display the plot
plt.show()


# Define slip ratios
slip_ratios = np.arange(-0.2, 0.2, 0.01)

# Define slip angles in degrees
slip_angles_deg = [0, 2, 4, 6]
slip_angles_rad = [
    angle * np.pi / 180 for angle in slip_angles_deg
]  # Convert to radians

# Prepare data for plotting FX-SR
fx_data = {sa: [] for sa in slip_angles_deg}  # Store FX data for each slip angle
for sa, sa_rad in zip(slip_angles_deg, slip_angles_rad):
    state["SA"] = sa_rad  # Set slip angle
    fx_per_sa = []
    for sr in slip_ratios:
        state["SR"] = sr  # Set slip ratio
        # Solve for FX using PureFx mode
        current_state = tire.solve(state, SolverMode.Fx)
        fx_per_sa.append(current_state["FX"])
    fx_data[sa] = fx_per_sa

# Create a figure and axes for FX-SR plot
fig, ax = plt.subplots()

# Plot results
for sa in slip_angles_deg:
    ax.plot(slip_ratios, fx_data[sa], label=f"SA = {sa}°")

# Add labels, legend, and grid
ax.set_xlabel("Slip Ratio (SR)")
ax.set_ylabel("Longitudinal Force, FX (N)")
ax.set_title("FX vs SR for Various Slip Angles")
ax.legend()
ax.grid()

# Display the plot
plt.show()


# Define slip angles in degrees
slip_angles = np.arange(-12, 12, 0.1)  # Slip angle in degrees
slip_angles_rad = slip_angles * np.pi / 180  # Convert to radians

# Define slip ratios
slip_ratios = [0, 0.03, 0.05]

# Prepare data for plotting FY-SA
fy_data = {sr: [] for sr in slip_ratios}  # Store FY data for each slip ratio
for sr in slip_ratios:
    state["SR"] = sr  # Set slip ratio
    fy_per_sr = []
    for sa in slip_angles_rad:
        state["SA"] = sa  # Set slip angle
        # Solve for FY using PureFy mode
        current_state = tire.solve(state, SolverMode.Fy)
        fy_per_sr.append(current_state["FY"])
    fy_data[sr] = fy_per_sr

# Create a figure and axes for FY-SA plot
fig, ax = plt.subplots()

# Plot results
for sr in slip_ratios:
    ax.plot(
        slip_angles,  # Use slip angles in degrees for plotting
        fy_data[sr],
        label=f"SR = {sr}",
    )

# Add labels, legend, and grid
ax.set_xlabel("Slip Angle (°)")
ax.set_ylabel("Lateral Force, FY (N)")
ax.set_title("FY vs SA for Various Slip Ratios")
ax.legend()
ax.grid()

# Display the plot
plt.show()
