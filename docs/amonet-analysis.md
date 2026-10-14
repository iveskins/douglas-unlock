# Amonet Douglas v1.2 source inspection

Archive: `amonet-douglas-v1.2.zip`, SHA-256 `6647dd0b5b9d2c04a2f167f6ccc7a2cfbcaa6f1f93f8251c7a39455db77119b2`.

The inspected archive contains `step-1.sh`, `step-2.sh`, `bootrom-step.sh`, `bootrom-step-minimal.sh`, `fastboot-step.sh`, `functions.inc`, Python modules and binary images. **It does not contain `brick-9820.sh`**. That script appears in a different community distribution and must not be assumed equivalent.

## `step-1.sh` flow, without `brick` argument

1. Wait for ADB and check `ro.product.name == douglas`.
2. Invoke `get_root` from `functions.inc`.
3. Read Android properties `ro.boot.tee_version`, `ro.boot.lk_version`, `ro.boot.pl_version`.
4. If **any** value is strictly greater than 259/2/6, ask to brick preloader and continue via BootROM. Passing literal argument `brick` forces that branch.
5. Otherwise prompt for factory reset; dump first 34 sectors of `/dev/block/mmcblk0` to a local `gpt-<serial>/gpt.bin`.
6. Patch local GPT with `modules/gpt.py patch` and write the patched first 34 sectors back to eMMC.
7. Write wipe instructions to `/cache/recovery/command`; reboot to recovery.

**Danger:** This is not a dry-run. It modifies the partition table and schedules data erasure. The local backup directory name embeds the device serial; do not commit it.

## `get_root` behavior

It checks `adb shell su -c id`, and if that fails, pushes `bin/mtk-su`, `bin/minisu.img`, `bin/busybox` to `/data/local/tmp/`. It repeatedly runs MTK-SU to mount `minisu.img` on `/system/xbin/` and checks `su -c id`. The loop may repeat indefinitely if root fails. MTK-SU R20 standalone success does **not** prove that this mount or the GPT write succeeds.

## Previous failure

A separate previous attempt failed in the Python `WRITE32` exchange during watchdog handling; the USB monitor observed Preloader but not BootROM. This does not establish that flashing had begun, nor does it prove the precise cause of the failure.

## Script identity caveat

The community GitHub guide uses `brick-9820.sh` + `bootrom-step-minimal.sh`; the uploaded original v1.2 package uses a different entry point. Do not combine procedures from different archives without a line-by-line comparison.
