import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_flight_path(log_filename="flight_log.json"):

    # Load data
    with open(log_filename, "r") as f:
        data = json.load(f)

    x = [entry["x"] for entry in data]
    y = [entry["y"] for entry in data]
    z = [entry["z"] for entry in data]

    # Create 3D figure
    fig =plt.figure(figsize=(10,7))
    ax = fig.add_subplot(111, projection = '3d')

    # Plit 3D trajectory line
    ax.plot(x, y, z, label="Flight Trajectory", color="blue", linewidth=2)

    # Start(green) and End(red) markers
    ax.scatter(x[0], y[0], z[0], color="green", s =50, label="Start")
    ax.scatter(x[-1], y[-1], z[-1], color="red", s =50, label="End")

    # Labels and ground reference plane
    ax.set_xlabel(" X Position (m)")
    ax.set_ylabel(" Y Position (m)")
    ax.set_zlabel(" Z Position (m)")
    ax.set_title("pyHIL-bench Flight Trajectory")
    ax.legend()

    # Forcce Z acis to start at ground level (0)
    ax.set_zlim(bottom=0)

    plt.show()

if __name__ == "__main__":
    plot_flight_path()    

