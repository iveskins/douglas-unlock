# Final preflight verification, 2026-10-15

**Device:** Amazon Fire HD 8 (2017), `douglas`  
**Firmware:** `636558720`  
**Evidence:** Operator-supplied Hermes report; original raw device logs not included in this public copy.

## Live GPT after Step 1

| Partition | First LBA | Last LBA | Size |
|---|---:|---:|---:|
| userdata | 4383744 | 60619775 | ~26.82 GiB |
| boot_tmp | 60619776 | 60845055 | 110 MiB |
| recovery_tmp | 60845056 | 61070335 | 110 MiB |

Hermes reports the live GPT matched `gpt.bin.step1.gpt` with SHA-256 `b0af79d2d78582fa4476721a37aa8bfaef5df0365e3f77affdd953960306afc0`.

## Step 2 payload hashes

Reported SHA-256 matches against the operator's untouched local `amonet-douglas.zip`:

| File | SHA-256 |
|---|---|
| boot.hdr | `12d881348acb2e9c2c7b42988125524c648d5948b1bdb677ee6c9d4e9e8d28c5` |
| boot.payload | `e10fdf770a5be2c2adc3cce0d03b8e296eac3b31e18ebdce5b56dc5491f4e7e8` |
| lk.bin | `7637da8754a7494f8907d07c7b25532476959956d1cfea856ab8ea6940176056` |
| tz.img | `dc0bbd4dec52b96c74e57c6439d093963dfce048e67d22d717b6654629e41cac` |
| preloader.bin | `cefc66528a56626e65a553b7f97e0521e7939c195ce72794e7c4e14eab04619d` |
| preloader.hdr0 | `114f4cbdb58c110168df273be2508b6efa36e2ef432f2255ed4f67ba35e97262` |
| preloader.hdr1 | `e86ae322a97975e75cb3ec7dca89ea4ac24639c1ecdcc3f45fe1bd509fc0c0ff` |
| twrp.img | `77889e8de3d48412bd29665d539c7559c0984ae7e46664581874b752484169af` |

The local archive match does not independently establish the archive's provenance. The MTK-SU binary was separately replaced with R20 for successful temporary-root testing.

## Script handling

Hermes reports `step-2.sh` begins with `set -e`. This provides limited shell error handling, not transactional flashing, write verification or rollback.

## Current state

- Step 1 completed and device boots Fire OS, per Hermes.
- ADB and MTK-SU temporary root available.
- Four Amazon OTA packages disabled, per Hermes.
- **Amonet Step 2 has not been run. TWRP and permanent unlock not confirmed.**
