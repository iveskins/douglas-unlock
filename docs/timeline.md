# Experiment timeline: Amazon Fire HD 8 (2017, Douglas)

**Recorded on:** 2026-10-15. **Device:** `douglas` / `KFDOWI`, Fire OS build `636558720` (`LVY48F`). **Evidence:** reconstructed from operator messages and Hermes reports; raw flashing transcript is not included. Order reflects the reported experiment sequence, not precise wall-clock timestamps. Device serial redacted.

| Step | Starting state / action | Result and evidence |
|---|---|---|
| 01 | Identify stock device over ADB: `adb devices -l`, `adb shell getprop` | Douglas/KFDOWI, Fire OS `636558720`, TEE `0x0103`, LK `0x0002`, PL `0x0006` (Hermes-reported). |
| 02 | Inspect stock privileges: `adb shell id`, `adb shell su -c id` | Normal shell UID 2000; `su` not found (Hermes-reported). |
| 03 | Test fastboot and USB transitions: `adb reboot bootloader`, fastboot `getvar` | USB `1949:0262` (ADB) → transient `0e8d:2000` (Preloader) → `1949:0260` (fastboot). Locked status reported; no `0e8d:0003` BootROM observed (Hermes-reported). |
| 04 | Attempt earlier low-level Amonet/BootROM path | `WRITE32` acknowledgement check failed near address `0x10007008`; no successful BootROM exploit established. Exact earlier script provenance uncertain (failed attempt). |
| 05 | Obtain and inspect Amonet Douglas v1.2 archive | Reviewed `step-1.sh`, `step-2.sh`, `functions.inc`, `modules/gpt.py`; version thresholds equal device values, selecting standard GPT route when Step 1 runs without `brick` argument (source-inspected/Hermes-reported). |
| 06 | Test temporary root: push MTK-SU R20 and run `adb shell /data/local/tmp/mtk-su -c id` | `uid=0(root) gid=0(root)` returned on Fire OS `636558720`; SELinux context `u:r:shell:s0` (Hermes output). Does **not** imply persistent root. |
| 07 | Dump original GPT and run offline patch generation | Original 16-partition GPT; Step 1 creates `boot_tmp` and `recovery_tmp`, each 110 MiB, by shortening `userdata` by 220 MiB. Generated Step 2 GPT renames active boot/recovery partitions (Hermes-reported). |
| 08 | Amonet `step-1.sh` GPT path executed | Hermes reports GPT flashed, recovery wipe requested, and device rebooted back to Fire OS. Later live GPT dump matched generated Step 1 image, including both temporary partitions (Hermes-reported). **Destructive action.** |
| 09 | Post-Step-1 validation | Firmware version gates unchanged; OTA-related Amazon packages disabled; temporary root still operational (Hermes-reported). |
| 10 | Step 2 preflight | Hermes reports all eight Amonet payload SHA-256 hashes match untouched local archive, Step 2 GPT files present, and `set -e` in script. See [final preflight](../reports/final_preflight_verification_2026-10-15.md). File matches do not independently authenticate upstream provenance. |
| 11 | Amonet `step-2.sh` executed | Operator subsequently **reached TWRP**. Hermes describes firmware writes to LK, TrustZone, preloader, GPT and recovery; exact execution transcript and per-command statuses **not supplied**. |
| 12 | Boot into TWRP | **TWRP interface displayed** (user-observed). This strongly indicates custom recovery and modified boot chain function. Independent bootloader unlock-status query pending. |
| 13 | Return to Fire OS | **Successful return to Fire OS** after TWRP (user-observed). Exact reboot mechanism not recorded. |
| 14 | Prepare ROM lifecycle | LineageOS 15.1 (Android 8.1) and 17.1 (Android 10) ZIPs reported downloaded. A ~500 MB LineageOS 15.1 update was discussed, but its installed status, file path, and preservation **have not been verified**. No ROM install or Magisk install confirmed. |

## Selected command evidence

```sh
adb devices -l
adb shell getprop ro.boot.tee_version
adb shell getprop ro.boot.lk_version
adb shell getprop ro.boot.pl_version
adb shell id
adb shell /data/local/tmp/mtk-su -c id
```

Reported root response:

```text
uid=0(root) gid=0(root) ... context=u:r:shell:s0
```

Reported live Step 1 GPT partitions:

```text
userdata       4383744  60619775
boot_tmp      60619776  60845055
recovery_tmp  60845056  61070335
```

## Outcome and remaining checks

**Achieved:** Temporary root; GPT-based Step 1; TWRP boot following Step 2; return to stock Fire OS. **Not established:** Persistent root, custom ROM boot, repeated TWRP entry, Magisk installation, a saved OTA ZIP, or full recovery from a corrupted preloader. Do not rerun destructive steps simply to collect logs. For ROM migration, see [ROM lifecycle](rom-lifecycle.md).
