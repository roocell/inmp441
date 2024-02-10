import smbus2
from typing import List, Tuple
import time

def read_voltage():
    bus = smbus2.SMBus(1)
    low = bus.read_byte_data(0x75, 0xa2)
    high = bus.read_byte_data(0x75, 0xa3)

    # Check negative values
    if high & 0x20 == 0x20:
        v = (((high | 0xC0) << 8) + low) & 0xFFFF
        voltage = 2600.0 - (v * 0.26855)
    else:
        v = ((high & 0x1f) << 8) + low
        voltage = 2600.0 + (v * 0.26855)

    return voltage / 1000.0

def avg_voltage():
    vacc = 0
    for i in range(10):
        vacc += read_voltage()
        time.sleep(0.1)
    return vacc / 10
    


# Define a type alias for BatteryThreshold
BatteryThreshold = Tuple[float, float]

# Define the battery curve constants
BATTERY_CURVE = [
    (4.16, 100.0),
    (4.05, 95.0),
    (4.00, 80.0),
    (3.92, 65.0),
    (3.86, 40.0),
    (3.79, 25.5),
    (3.66, 10.0),
    (3.52, 6.5),
    (3.49, 3.2),
    (3.1, 0.0),
]

def convert_battery_voltage_to_level(voltage: float, battery_curve: List[BatteryThreshold]) -> float:
    for i in range(len(battery_curve)):
        v_low, l_low = battery_curve[i]
        if voltage >= v_low:
            if i == 0:
                return l_low
            else:
                v_high, l_high = battery_curve[i - 1]
                percent = (voltage - v_low) / (v_high - v_low)
                return round(l_low + percent * (l_high - l_low), 0)
    return 0.0

voltage_value = read_voltage()

# the original source takes an average voltage reading before convert

battery_level = convert_battery_voltage_to_level(voltage_value, BATTERY_CURVE)
print(f'voltage_value {voltage_value} Battery level: {battery_level}%')
