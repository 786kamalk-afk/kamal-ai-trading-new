import yaml
import time
import os
from signal_bus import SignalBus

CONFIG_FILE = "signals.yaml"

def load_config():
    """YAML se config aur signals load kare"""
    with open(CONFIG_FILE, "r") as f:
        data = yaml.safe_load(f)
    signals = data.get("signals", [])
    loop = data.get("loop", False)
    return loop, signals

def main():
    bus = SignalBus()
    last_mtime = 0
    loaded_signals = []
    sent_signals = set()
    loop_mode = False

    print(f"[FEEDER] Watching {CONFIG_FILE} for changes...")

    while True:
        try:
            # check file modification time
            mtime = os.path.getmtime(CONFIG_FILE)
            if mtime != last_mtime:
                last_mtime = mtime
                loop_mode, loaded_signals = load_config()
                sent_signals.clear()
                print(f"[FEEDER] Reloaded {len(loaded_signals)} signals | Loop={loop_mode}")

            # process signals
            for i, signal in enumerate(loaded_signals):
                sig_key = f"{signal['symbol']}_{signal['direction']}_{i}"

                if loop_mode:
                    # hamesha bhejta rahega
                    bus.emit(signal)
                    print(f"[FEEDER][LOOP] Sent -> {signal}")
                else:
                    # sirf ek baar bhejega
                    if sig_key not in sent_signals:
                        bus.emit(signal)
                        sent_signals.add(sig_key)
                        print(f"[FEEDER][ONCE] Sent -> {signal}")

            time.sleep(2)

        except Exception as e:
            print(f"[FEEDER][ERROR] {e}")
            time.sleep(2)

if __name__ == "__main__":
    main()
