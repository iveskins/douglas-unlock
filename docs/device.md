# Device under test

| Property | Value | Evidence |
|---|---|---|
| Product | Amazon Fire HD 8 (2017, seventh generation) | Observed via ADB |
| Codename | `douglas` | Observed via ADB |
| Model | `KFDOWI` | Observed via ADB |
| Board | `KC13_MB_Rev1.0` | Operator photo/report |
| Firmware | `50.6.3.6_user_636558720` | Observed via ADB |
| ADB serial | **REDACTED** | Do not commit |
| Bootloader state | `unlock_status: false`, `secure: yes` | Observed via fastboot |
| PL antirollback version | `0x0006` | Observed via fastboot |
| LK antirollback version | `0x0002` | Observed via fastboot |
| TEE antirollback version | `0x0103` | Observed via fastboot |
| Normal USB | `1949:0262` | Observed |
| Fastboot USB | `1949:0260` | Observed |
| Preloader USB | `0e8d:2000` | Observed |
| BootROM USB | `0e8d:0003` | **Not observed**; expected on many MTK devices |

The Amonet `step-1.sh` compares `ro.boot.tee_version`, `ro.boot.lk_version` and `ro.boot.pl_version` with 259, 2 and 6. Hermes reported equality at all three thresholds. **Fastboot antirollback values and Android properties have not yet been cross-checked in one captured session**; do not silently treat them as interchangeable.
