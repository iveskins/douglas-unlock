# Amonet Step 2 pre-deployment plan, 2026-10-15

**Status: planned, not executed.** Summary transcribed from Hermes' script inspection and local file inventory. Do not treat predictions as observations.

## Operator-reported payload inventory

| Path under `amonet/bin/` | Bytes |
|---|---:|
| boot.hdr | 4,096 |
| boot.payload | 492,132 |
| lk.bin | 485,988 |
| tz.img | 3,307,008 |
| preloader.hdr0 | 2,048 |
| preloader.hdr1 | 2,048 |
| preloader.bin | 138,924 |
| twrp.img | 13,512,704 |

Generated files: `gpt.bin.step2.gpt` (17,408 B), `gpt.bin.step2.bak` (16,896 B), `gpt.bin.offset` (9 B). These are local artifacts, excluded from Git.

## Expected operation order, from Hermes analysis

1. Confirm `_tmp` partitions and temporary root.
2. Write Amonet exploit payload.
3. Write LK and TrustZone firmware.
4. Write preloader to eMMC boot0.
5. Write final primary and secondary GPT structures.
6. Install TWRP and reboot into recovery.

**Timing:** Hermes estimated 10–30 seconds for script operations; not verified. First recovery boot can take longer. No button interaction is expected while flashing. Do not disconnect USB or rerun automatically after failure.

## Post-execution verification

- Record command transcript, exit status and timestamps.
- Record USB identities and kernel messages from an independent tmux pane.
- Confirm TWRP UI and touch functionality before changing other partitions.
- Do not wipe `system` just to verify unlock.
- ROM and Magisk downloads/compatibility need separate checks before flashing.

## Important distinction

`fire_tablet_inventory_v2.py --once --dmesg` is a **diagnostic test**, not Amonet `step-2.sh`.
