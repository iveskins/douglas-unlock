# Douglas Unlock Lab

A reproducible **device-specific unlock and ROM lifecycle journal** for the **Amazon Fire HD 8 (2017)**, codename `douglas` (KFDOWI). Documents real experiments, commands, files, results, and recovery risks from stock Fire OS through Amonet, TWRP, and future ROM changes. This is **not** an automated unlocker.

**Current outcome (2026-10-15):** Amonet Steps 1 and 2 completed according to operator reports. **TWRP booted successfully**, and the tablet subsequently **booted back into Fire OS**. No persistent root or LineageOS installation has been confirmed. Full Step 2 terminal transcript is not available.

## Start here: chronological walkthrough

Read **[the numbered experiment timeline](docs/timeline.md)** first. Each step records the starting state, action or command, actual outcome, and evidence limitations. Then consult [experiment index](docs/experiments.md), [Amonet analysis](docs/amonet-analysis.md), and [TWRP/Fire OS return](reports/twrp_boot_and_fireos_return_2026-10-15.md).

## Scope

Included: Douglas hardware/firmware identification, ADB/fastboot and USB modes, MTK-SU, Amonet Step 1/2, GPT changes, TWRP, Fire OS, ROM ZIPs, OTA update discovery, backup/restore, ROM migration, recovery and source/archive provenance.

Excluded: terminal setup, tmux, clipboard configuration, WebGPU/browser experiments, unrelated host workflows.

## Reproduce read-only device inspection

```sh
sudo apt install adb fastboot python3 usbutils
python3 tools/capture.py --output observations/$(date -u +%Y%m%dT%H%M%SZ)
```

`tools/fire_tablet_inventory_v2.py` and [USB mode notes](docs/usb-monitoring.md) are retained **only** for device identification and recovery diagnostics. The supplied tools are intended for observation, not firmware writes.

## Documentation

| File | Contents |
|---|---|
| [Timeline](docs/timeline.md) | Numbered steps, commands, device states, results |
| [Experiments](docs/experiments.md) | Indexed tests, successes, failures, unknowns |
| [Device](docs/device.md) | Hardware, firmware and USB IDs |
| [Temporary root](docs/temporary-root.md) | MTK-SU R20 test |
| [Amonet analysis](docs/amonet-analysis.md) | Script behavior and risks |
| [Final preflight](reports/final_preflight_verification_2026-10-15.md) | GPT comparison and payload hashes |
| [Step 2 plan](reports/pre_deployment_report_2026-10-15.md) | Payloads and expected flashing sequence |
| [TWRP and Fire OS](reports/twrp_boot_and_fireos_return_2026-10-15.md) | Actual post-unlock result |
| [ROM lifecycle](docs/rom-lifecycle.md) | OTA ZIP preservation, TWRP backups, switching ROMs |
| [Sources](docs/sources.md) | Upstream references and attribution |

## Evidence and safety

**User-observed** means the operator explicitly reported seeing the result. **Hermes-reported** means the agent provided output or a summary, but a complete raw session transcript is not in this repository. **Source-inspected** means a script or archive was examined. **Pending** means not verified. Do not interpret a generated patch or successful root test as proof of a complete unlock.

The Amonet process writes boot-critical partitions. Failed flashing can require hardware test-point recovery. Do not run Step 1 or Step 2 just to reproduce this journal on an already modified tablet. Keep serials, raw GPT dumps, firmware images and identifying logs out of public commits. Third-party firmware/binaries are referenced, not redistributed.

Original documentation/tools: MIT license. Upstream firmware and tools retain their respective rights.
