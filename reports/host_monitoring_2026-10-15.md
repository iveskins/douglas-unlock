# Host environment and monitoring validation, 2026-10-15

**Source:** Hermes operator report. **No Amonet Step 2 execution reported.**

## Tested

- `fire_tablet_inventory_v2.py --once --dmesg` run on host, according to Hermes.
- USB snapshot: Amazon `1949:0262`, bus path `1-2`.
- ADB inventory: `douglas`, model `KFDOWI`, connected and responding.
- `udevadm` and `dmesg` monitoring reported operational.
- Amonet v1.2 extracted under `~/fire/amonet/`.
- LineageOS 15.1 (Android 8.1) and 17.1 (Android 10) ZIP files reported downloaded under `~/fire/downloads/`. No archive hashes or ROM install results supplied.
- A persistent local Hermes skill `fire-tablet-amonet-unlocking` reported saved; not bundled in this repo.
- `~/.tmux.conf` updated for mouse scrolling and OSC 52 clipboard integration. Actual config text not provided.

## Reproducible tmux baseline

```sh
tmux set -g mouse on
tmux set -g history-limit 50000
```

To persist these settings, add them to `~/.tmux.conf`. OSC 52 configuration is terminal-dependent and is not reproduced without the actual tested configuration.

## Evidence to capture during a real Step 2 run

- Raw command transcript and shell exit status (store privately, redact before publishing).
- Independent USB/udev and kernel event logs.
- Start/end timestamps, device screen observations, final boot mode.
- Avoid recording device serials in public files.
