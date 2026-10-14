# USB and kernel monitoring (Ubuntu)

Start monitors *before* connecting the tablet:

```bash
sudo udevadm monitor --kernel --property --subsystem-match=usb | tee douglas-usb.raw.log
sudo dmesg --follow --human | grep --line-buffered -v wlp | tee douglas-kernel.raw.log
watch -n 0.2 'lsusb | grep -Ei "0e8d|1949"'
```

Run these in separate terminals. `watch` polling may miss brief modes; `udevadm` captures transitions. `dmesg` may contain unrelated sensitive host information. Keep raw logs locally and commit only redacted extracts. `udevadm` records may contain `DEVPATH`, bus number, device number, USB ID and action; **do not confuse `0e8d:2000` Preloader with `0e8d:0003` BootROM**.

Observed sequence in earlier testing: Fire OS `1949:0262` → Preloader `0e8d:2000` → Amazon Fastboot `1949:0260`.
