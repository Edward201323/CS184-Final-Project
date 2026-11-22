"""Read SO-101 joint positions in raw encoder ticks."""

import argparse
import json
import time

from lerobot.motors import Motor, MotorNormMode
from lerobot.motors.feetech import FeetechMotorsBus


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("port", help="USB serial port of the SO-101")
    parser.add_argument("--watch", action="store_true", help="read every second until Ctrl+C")
    args = parser.parse_args()

    names = ("shoulder_pan", "shoulder_lift", "elbow_flex", "wrist_flex", "wrist_roll", "gripper")
    motors = {
        name: Motor(motor_id, "sts3215", MotorNormMode.DEGREES)
        for motor_id, name in enumerate(names, start=1)
    }
    bus = FeetechMotorsBus(port=args.port, motors=motors)
    bus.connect(handshake=False)
    try:
        while True:
            started = time.monotonic()
            positions = bus.sync_read("Present_Position", normalize=False, num_retry=2)
            print(json.dumps(positions, indent=None if args.watch else 2), flush=True)
            if not args.watch:
                break
            time.sleep(max(0, started + 1 - time.monotonic()))
    except KeyboardInterrupt:
        pass
    finally:
        bus.disconnect(disable_torque=False)


if __name__ == "__main__":
    main()
