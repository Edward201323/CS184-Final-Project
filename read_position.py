"""Read one SO-101 joint-position snapshot in raw encoder ticks."""

import argparse
import json

from lerobot.motors import Motor, MotorNormMode
from lerobot.motors.feetech import FeetechMotorsBus


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("port", help="USB serial port of the SO-101")
    args = parser.parse_args()

    names = ("shoulder_pan", "shoulder_lift", "elbow_flex", "wrist_flex", "wrist_roll", "gripper")
    motors = {
        name: Motor(motor_id, "sts3215", MotorNormMode.DEGREES)
        for motor_id, name in enumerate(names, start=1)
    }
    bus = FeetechMotorsBus(port=args.port, motors=motors)
    bus.connect(handshake=False)
    try:
        positions = bus.sync_read("Present_Position", normalize=False, num_retry=2)
        print(json.dumps(positions, indent=2))
    finally:
        bus.disconnect(disable_torque=False)


if __name__ == "__main__":
    main()
