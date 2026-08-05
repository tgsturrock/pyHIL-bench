# pyHIL-bench
A Real-Time Hardware-in-the-Loop Simulation &amp; Fault-Injection Testing Framework
## 📌 Executive Summary
pyHIL-bench is a lightweight, Python-native Hardware-in-the-Loop (HIL) and Software-in-the-Loop (SIL) testing framework designed to validate autonomous control systems (UAVs, automotive ECUs, or robotics) under simulated physical conditions.

By running a physics dynamic model in software and streaming real-time synthetic sensor telemetry over UDP/Serial to a System Under Test (SUT), pyHIL-bench enables automated verification, stress testing, and real-time fault injection without requiring physical field tests.

## 🏗️ System Architecture
```
+-------------------------------------------------------------------+
|                        pyHIL Test Host                            |
|                                                                   |
|   +-----------------------+           +-----------------------+   |
|   |   Physics Engine      |           | Fault Injector Engine |   |
|   |  (Kinematics, Flight) |           |  (Bit flips, Latency) |   |
|   +-----------+-----------+           +-----------+-----------+   |
|               |                                   |               |
|               +-----------------+-----------------+               |
|                                 |                                 |
|                      +----------v----------+                      |
|                      | Telemetry Generator |                      |
|                      +----------+----------+                      |
+---------------------------------|---------------------------------+
                                  | UDP / Serial (M4 / MavLink / JSON)
                                  v
+-------------------------------------------------------------------+
|                     System Under Test (SUT)                       |
|        (Embedded MCU, MicroPython / C++ Flight Controller)        |
+-------------------------------------------------------------------+
                                  |
                                  | Control Actuation Signals
                                  v
+-------------------------------------------------------------------+
|                     Pytest Verification Engine                    |
|             (Pass/Fail Logs, Traceability Reports)                |
+-------------------------------------------------------------------+
```
## ✨ Key Features
* Physics & Environment Simulation: Simulates vehicle dynamics (acceleration, angular rate, altitude decay, sensor noise) in a real-time 50Hz update loop.

* Automated Fault Injection: Inject edge-case failure modes during live execution, including:

    * GPS signal dropouts / satellite loss.

    * Sensor drift (accelerometer / gyro bias).

    * Packet corruption and artificial network latency.

* Closed-Loop Feedback: Accepts actuation commands from the target controller (e.g., motor throttle or steering angle) to update physical states dynamically.

* Pytest-Integrated Automated Verification: Automated assertions checking for critical safety bounds (e.g., "System must engage Emergency Failsafe within 200ms of GPS loss").

* CLI & Visual Telemetry Dashboard: Integrated terminal UI (built with Rich) or Web UI (Streamlit) to monitor vehicle states and injection triggers live.
