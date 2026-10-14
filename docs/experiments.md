# Experiment log

Status markers: `OBSERVED`, `OPERATOR-REPORTED`, `PENDING`, `FAILED`.

| ID | Test | Result | Status |
|---|---|---|---|
| E001 | ADB enumeration | `douglas` / `KFDOWI` / firmware `636558720`; shell UID 2000 | OBSERVED (conversation output) |
| E002 | Fastboot `getvar all` | Locked; PL 6, LK 2, TEE 259; secure yes | OBSERVED (conversation output) |
| E003 | USB reboot into bootloader | `1949:0262` → `0e8d:2000` (~2.55s) → `1949:0260`; no BootROM observed | OBSERVED (conversation output) |
| E004 | Previous Amonet BootROM attempt | `WRITE32` protocol check at `0x10007008` failed expecting `00 01` | FAILED (conversation output); exact archive used then unverified |
| E005 | Root without `su` | `su: not found`; normal shell UID 2000 | OPERATOR-REPORTED (Hermes) |
| E006 | MTK-SU R20 `-c id` | `uid=0(root) gid=0(root)`; `context=u:r:shell:s0` | **OPERATOR-REPORTED**, no raw session log in repo |
| E007 | Inspect Amonet v1.2 | Version gates `259/2/6`; normal path patches GPT; `brick` path writes bootloader areas | SOURCE-INSPECTED |
| E008 | Run `step-1.sh` GPT path | **Not attempted in this record** | PENDING |
| E009 | Full bootloader unlock/TWRP | **Not confirmed** | PENDING |
| E010 | Silk WebGL/Wasm/WebGPU tests | **Not captured** | PENDING |

## Next reproducible checks

1. Record `ro.boot.*_version` using `tools/capture.py` and compare with Hermes' report.
2. Preserve SHA-256 of the exact MTK-SU R20 binary tested, and record whether it replaced a bundled copy (Amonet v1.2 ZIP has no `bin/mtk-su`).
3. Independently verify root again if necessary, keeping a full, sanitized terminal transcript.
4. Inspect the patched GPT *offline* and confirm rollback strategy before any write.
5. Keep USB event logs running for any later BootROM experiments.

Do not mark the device unlocked solely because MTK-SU returned UID 0.
