# Temporary-root verification (MTK-SU)

**Operator-reported success** on `douglas` firmware `636558720` with ARM64 MTK-SU Release 20. The operator reported that Hermes replaced the local `amonet/bin/mtk-su` with a binary from an upstream MTK-SU R20 release. Its SHA-256 is **not yet recorded**.

Commands reportedly executed (only the last line attempts kernel exploitation):

```bash
adb push amonet/bin/mtk-su /data/local/tmp/
adb shell chmod 755 /data/local/tmp/mtk-su
adb shell /data/local/tmp/mtk-su -c id
```

Reported result:

```text
uid=0(root) gid=0(root) groups=... context=u:r:shell:s0
```

This verifies UID 0 for that process; it does not establish a persistent `su`, an unlocked bootloader, or unrestricted SELinux privileges. Exploits may panic or reboot the kernel. `/data/local/tmp/` is on persistent userdata and pushed files can survive reboot. **No partition writes or factory reset were reported for this standalone test**, but no independently captured raw log is stored here.

Before reproduction, confirm binary architecture, source, hash and authorization. Never execute MTK-SU automatically from `tools/capture.py`.
