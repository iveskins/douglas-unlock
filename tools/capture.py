#!/usr/bin/env python3
"""Read-only Douglas ADB/fastboot snapshot; serials hashed, raw data stays local."""
import argparse, datetime, hashlib, json, pathlib, re, shutil, subprocess

def call(args, timeout=12):
    if not shutil.which(args[0]):
        return {'ok': False, 'error': f'{args[0]} not installed'}
    try:
        p = subprocess.run(args, capture_output=True, text=True, timeout=timeout, check=False)
        return {'ok': p.returncode == 0, 'code': p.returncode, 'stdout': p.stdout.strip(), 'stderr': p.stderr.strip()}
    except (OSError, subprocess.TimeoutExpired) as e:
        return {'ok': False, 'error': str(e)}

def redact(s):
    # Hash serials separately; avoid persisting raw identifiers in structured output.
    s = re.sub(r'\bG0[0-9A-Z]{12,}\b', '[REDACTED_SERIAL]', s)
    s = re.sub(r'(?i)(serialno|serialnumber|serial):\s*\S+', r'\1: [REDACTED]', s)
    s = re.sub(r'(?i)(serialno|serialnumber|serial)=\S+', r'\1=[REDACTED]', s)
    return s

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', default='observations/latest', help='private output folder (gitignored)')
    args = ap.parse_args()
    dest = pathlib.Path(args.output); dest.mkdir(parents=True, exist_ok=True)
    data = {'timestamp_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'policy': 'read-only; no reboot/root/flash'}
    devices = call(['adb', 'devices', '-l'])
    data['adb_devices'] = redact(devices.get('stdout', '') + '\n' + devices.get('stderr', ''))
    # Require exactly one authorized device. No attempts to start root or bypass authorization.
    rows = [x.split() for x in devices.get('stdout','').splitlines()[1:] if x.strip()]
    authorized = [x[0] for x in rows if len(x)>1 and x[1]=='device']
    if len(authorized)==1:
        serial=authorized[0]
        data['device_id_sha256_prefix'] = hashlib.sha256(serial.encode()).hexdigest()[:12]
        props=['ro.product.device','ro.product.model','ro.product.name',
               'ro.build.version.incremental','ro.build.version.release',
               'ro.boot.tee_version','ro.boot.lk_version','ro.boot.pl_version',
               'ro.build.version.sdk']
        data['properties'] = {p: redact(call(['adb','-s',serial,'shell','getprop',p]).get('stdout','')) for p in props}
        data['shell_id'] = redact(call(['adb','-s',serial,'shell','id']).get('stdout',''))
        data['silk_version'] = redact(call(['adb','-s',serial,'shell','dumpsys','package','com.amazon.cloud9'],timeout=20).get('stdout',''))
        # Retain only package version fields rather than entire dumpsys output.
        data['silk_version'] = '\n'.join(x.strip() for x in data['silk_version'].splitlines() if 'versionName=' in x or 'versionCode=' in x)[:2000]
    else:
        data['note'] = 'Exactly one authorized ADB device required for property capture.'
    data['lsusb'] = redact(call(['lsusb']).get('stdout',''))
    (dest/'snapshot.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    print('Saved', dest/'snapshot.json')
    print('ADB devices:', len(authorized), 'authorized')
    if 'properties' in data:
        print('Device:',data['properties'].get('ro.product.device'), 'Build:',data['properties'].get('ro.build.version.incremental'))
    print('Review snapshot for identifiers before sharing.')
if __name__=='__main__': main()
