# Douglas unlock lab: reproducible research notes

**Status (2026-10-15): Temporary UID 0 confirmed; Amonet Step 1 GPT change completed and post-reset Fire OS boot reported; final Step 2 preflight passed; Amonet Step 2 NOT executed and bootloader unlock NOT confirmed.**

Research journal and read-only diagnostics for the Amazon Fire HD 8 (2017, `douglas`, model `KFDOWI`). This is **not** an automated unlocker. Scripts in `tools/` gather diagnostic information and do not write to Android partitions. High-risk commands are recorded as *unexecuted* until independently confirmed.

## Quick start

```bash
sudo apt install adb fastboot python3 usbutils
python3 tools/capture.py --output observations/$(date -u +%Y%m%dT%H%M%SZ)
# connect and authorize the tablet, then run again to record its state
```

`capture.py` is a one-shot read-only snapshot, not a background daemon. `tools/fire_tablet_inventory_v2.py` is an additional operator-tested inventory and USB/kernel-monitoring utility. To watch USB transitions separately, see [`docs/usb-monitoring.md`](docs/usb-monitoring.md). **Do not publish unredacted raw logs**: serials, hostnames, MAC addresses and paths may identify devices or people. Captured files are gitignored.

## Evidence levels

- **Observed**: output directly recorded from the user's computer and reproduced in this repo (sanitized).
- **Operator-reported**: Hermes/terminal output shared by the operator; original raw logs not provided.
- **Source-inspected**: claims derived from the exact `amonet-douglas-v1.2.zip` uploaded for analysis.
- **Community-reported**: third-party reports, not independent verification.
- **Pending**: not tested.

## Navigation

| Document | Purpose |
|---|---|
| [October 15 progress and deployment gate](docs/2026-10-15-status.md) | Step 1 outcome, Step 2 readiness, outstanding risks |
| [Final preflight report](reports/final_preflight_verification_2026-10-15.md) | GPT ranges, checksums, evidence levels |
| [Step 2 execution plan](reports/pre_deployment_report_2026-10-15.md) | Payload inventory and operator checklist |
| [Host tooling validation](reports/host_monitoring_2026-10-15.md) | Inventory v2, tmux and monitoring status |
| [Device profile](docs/device.md) | Hardware, Fire OS, USB identities, version gates |
| [Experiment log](docs/experiments.md) | Chronological test results, confidence and next checks |
| [Amonet analysis](docs/amonet-analysis.md) | Actual v1.2 script behavior, risk boundaries |
| [USB monitoring](docs/usb-monitoring.md) | Reproducible udev/dmesg capture |
| [Temporary root](docs/temporary-root.md) | MTK-SU R20 commands and reported outcome |
| [Web graphics goal](docs/browser-gpu.md) | Wasm/WebGL/WebGPU test matrix |
| [Sources](docs/sources.md) | Original downloads and upstream credits |
| [Provenance](artifacts/README.md) | Archive hash and redistribution policy |

## Safety and scope

This repo documents potentially destructive research. `step-1.sh` writes the GPT and requests a factory reset; `step-1.sh brick` writes boot partitions and firmware. Battery disconnection may reset a stuck tablet but does not guarantee unbricking. Do not run these operations on a device containing important data. Keep a backup, verified device identity and a recovery plan. No vendor binaries are committed by default.

## Reproduce and contribute

Clone this repo, run read-only capture, save a sanitized experiment entry using [`templates/experiment.md`](templates/experiment.md), then commit. Do not publish device serials, identifiers, user data, GPT dumps, keys or proprietary firmware without review.

License: documentation and our original tools under MIT (`LICENSE`); third-party Amonet, MTK-SU, firmware and TWRP retain their own licenses and ownership.
