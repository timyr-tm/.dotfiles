#!/usr/bin/env python

import os
import sys
import subprocess
import json

settings: dict[str, str] = {
    "use-hot-keys": "true"
}

def main(*args) -> None:
    print("\0", "\x1f".join([item for data in settings.items() for item in data]), sep="")

    if len(args) > 0:
        retv: int = int(os.getenv("ROFI_RETV"))
        actions: dict[int, list[str]] = {
            1: ["pactl", "set-default-sink", args[0]],
            10: ["pactl", "set-sink-volume", args[0], "-5%"],
            11: ["pactl", "set-sink-volume", args[0], "-1%"],
            12: ["pactl", "set-sink-volume", args[0], "+5%"],
            13: ["pactl", "set-sink-volume", args[0], "+1%"]
        }
        if retv in actions:
            subprocess.run(actions[retv])

    current_sink: str = subprocess.run(
        ["pactl", "get-default-sink"],
        capture_output=True,
        text=True
    ).stdout.replace("\n", "")
    
    sinks: list[dict[str, object]] = sorted(
        json.loads(
            subprocess.run(
                ["pactl", "-f", "json", "list", "sinks"],
                capture_output=True
            ).stdout
        ),
        key=lambda sink: [
            sink["name"] != current_sink,
            sink["properties"]["node.nick"]
        ]
    )
            
    for sink in sinks:
        print(
            f"{sink["name"]}\0"
            f"icon\x1f"
            f"{sink["properties"]["device.icon_name"]}\x1f"
            f"display\x1f"
            f"{sink["properties"]["node.nick"][:32]:<32} │ "
            f"{("▰" * round(int(sink["volume"]["front-left"]["value_percent"][:-1]) / 10))[:15]:▱<15} │ "
            f"{sink["volume"]["front-left"]["value_percent"]:>4}\x1f"
        )
    

if __name__ == "__main__":
    main(*sys.argv[1:])