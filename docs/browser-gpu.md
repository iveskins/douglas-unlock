# Target use: browser graphics on Douglas

Goal: run WebAssembly-heavy pages and hardware-accelerated browser graphics; investigate WebGPU but do not assume support.

Observed Silk package version: `71.2.4.3578.98.10`, `versionCode=712000410`, `targetSdk=24`. **Silk version 71 is not evidence of Chromium 71.**

| Capability | Current evidence | Next test |
|---|---|---|
| Wasm | Not directly measured | Run feature probe |
| Wasm SIMD / threads | Unknown | Run feature probe |
| WebGL 1 | Likely, unverified | https://get.webgl.org/ |
| WebGL 2 | Unknown | https://webglreport.com/?v=2 |
| WebGPU | Unknown, likely constrained by Mali-T720 driver/backend | https://webgpureport.org/ |
| Hardware vs software rendering | Unknown | Browser GPU diagnostics if exposed |

LineageOS 15.1 and 17.1 builds are available for Douglas; neither guarantees working WebGPU. GPU tests should be repeated on stock Fire OS and any alternative ROM.
