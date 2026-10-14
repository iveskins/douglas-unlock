# ROM and recovery lifecycle

**Present state:** TWRP was reached and Fire OS booted afterward. LineageOS installation is not confirmed. The operator reports having downloaded Douglas builds of LineageOS 15.1 and 17.1.

## 1. Inventory ROM ZIPs

```sh
find ~/fire/downloads -maxdepth 2 -type f -iname '*.zip' -print
adb shell 'find /sdcard/Download /sdcard -type f -iname "*.zip" 2>/dev/null'
```

If running LineageOS Updater, an update may be stored under `/data/lineageos_updates/` and may require appropriate permissions. Installed updates may be deleted automatically. Inspect ZIP metadata and hashes before using a file; do not assume every ZIP is a full install package.

## 2. Preserve a working ROM before switching

In TWRP, make a **Boot + System + Data** backup (plus supported device-specific partitions as appropriate). Copy it to the host and verify checksums. TWRP backups are snapshots, not equivalent to a reusable signed update ZIP. Record the Android version, ROM build, recovery version, partition names and backup timestamp.

## 3. Switching 15.1 ↔ 17.1

Confirm that each ZIP explicitly targets `douglas`; consult its maintainer instructions for recovery requirements and wipes. Do not restore Android 8.1 Data directly over Android 10. Keep a known-good 15.1 backup and original installation package. Do not modify preloader/LK/GPT for an ordinary ROM switch unless a device-specific guide explicitly requires it.

## 4. Root compatibility

MTK-SU R20 on stock Fire OS was **temporary root**, not persistent Android root. Modern Magisk requires Android 6.0+, so stock Fire OS 5 (Android 5.1) is not a suitable target; a compatible custom ROM may be. Check the actual installed Android version and Magisk requirements before proceeding.

## 5. Recovery checkpoints

After flashing a ROM, verify boot, recovery re-entry, touchscreen, Wi-Fi, storage and available backups. Keep private raw logs and publish sanitized findings in the experiment timeline. Avoid automatically rerunning Amonet after it has succeeded.
