from __future__ import annotations
import argparse, json, time
from .models import SensorFrame, MissionRequest, MissionType
from .runtime import StallionRuntime


def main():
    p = argparse.ArgumentParser()
    p.add_argument("query", nargs="?", default=None)
    p.add_argument("--interactive", "-i", action="store_true")
    p.add_argument("--graph", "-g", action="store_true")
    p.add_argument("--demo", action="store_true")
    args = p.parse_args()

    rt = StallionRuntime()

    if args.graph:
        print(json.dumps(rt.atlas.graph(), ensure_ascii=False, indent=2))
        return

    if args.interactive:
        print("STALLION–PNEVMA Ω v1.1")
        print("Команды: /graph /status /quit")
        while True:
            q = input("Ω > ").strip()
            if q == "/quit":
                return
            if q == "/graph":
                print(json.dumps(rt.atlas.graph(), ensure_ascii=False, indent=2))
                continue
            if q == "/status":
                print(json.dumps(rt.status(), ensure_ascii=False, indent=2))
                continue
            print(json.dumps(rt.atlas.analyze(q).__dict__, ensure_ascii=False, indent=2, default=str))
        return

    if args.query and not args.demo:
        print(json.dumps(rt.atlas.analyze(args.query).__dict__, ensure_ascii=False, indent=2, default=str))
        return

    sensor = SensorFrame(
        timestamp=time.time(),
        objects=["person_in_need", "debris"],
        thermal_alerts=[],
        localization_confidence=.94,
        imu_stable=True,
        battery_level=.82,
    )
    mission = MissionRequest(
        MissionType.RESCUE,
        "locate and assist a person in a simulated training area",
        simulated=True,
    )
    print(json.dumps(rt.cycle(sensor, mission, "ведун волхв характерник"), ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
