# TWRP boot and return to Fire OS (2026-10-15)

**Device:** Amazon Fire HD 8 (2017), `douglas` / KFDOWI.
**Firmware before unlock:** `636558720` (Fire OS 5 / Android 5.1 lineage).
**Evidence level:** Direct operator statement in conversation; Step 2 raw execution transcript not supplied.

## Reported outcome

- Amonet Step 1 completed earlier; GPT temporary partitions were independently reported present in the live GPT.
- Amonet Step 2 was subsequently attempted, and the tablet **entered TWRP**.
- The operator then rebooted and successfully **returned to Fire OS**.
- No installation of Magisk, LineageOS, or persistent root has been reported.

## Interpretation and limitations

Successful custom recovery boot followed by stock OS boot is strong evidence that the Amonet modified boot chain works. This is not the same as a recorded `fastboot getvar unlock_status` check. We do not yet have the Step 2 terminal log, TWRP version, screenshots, hashes of flashed partitions, or a repeated TWRP-entry test. Avoid describing these as independently verified.

## Magisk compatibility

Modern Magisk requires Android 6.0 or later. Stock Fire OS 5 on this tablet is based on Android 5.1, so current Magisk is not supported on the existing OS. A compatible Android 8.1 or 10 custom ROM may meet the Android version requirement, but model-specific compatibility and installation steps still need verification. TWRP and an unlocked boot chain do not themselves provide persistent Android root.

## Suggested read-only follow-up

```bash
adb devices -l
adb shell getprop ro.build.version.release
adb shell getprop ro.build.display.id
```

Do not rerun Amonet Step 2 solely to obtain logs. Preserve existing logs if available. Do not wipe `system` merely to test recovery.
