#!/usr/bin/env python3
"""Read-only ADB inventory plus USB udev and optional dmesg event capture.
Python 3.9+, Linux; requires adb for Android properties. No device changes.
"""
import argparse
import csv
import datetime as dt
import json
import pathlib
import queue
import re
import shutil
import subprocess
import threading
import time

FIELDS = ['first_seen','last_seen','serial','manufacturer','model','device','product','hardware','android','fire_os','build_incremental','build_fingerprint','security_patch','sdk','software_root','bootloader_unlock','hardware_route','assessment','notes']
PROPS = {
 'manufacturer':'ro.product.manufacturer','model':'ro.product.model','device':'ro.product.device',
 'product':'ro.product.name','hardware':'ro.hardware','android':'ro.build.version.release',
 'fire_os':'ro.build.version.fireos','build_incremental':'ro.build.version.incremental',
 'build_fingerprint':'ro.build.fingerprint','security_patch':'ro.build.version.security_patch',
 'sdk':'ro.build.version.sdk',
}
KNOWN = {
 'mustang': ('0002517050244','Fire 7 (2019), 9th gen','No confirmed software-only permanent unlock; hardware-assisted route documented.'),
 'douglas': ('636558520','Fire HD 8 (2017), 7th gen','Software Amonet route documented, but involves risky preloader modification.'),
 'giza': ('626533320','Fire HD 8 (2016), 6th gen','Software Amonet route reported; verify specific firmware and guide.'),
}
USB_MODES = {'1949:0262':'Amazon Fire OS / ADB-capable USB','1949:0260':'Amazon Fastboot',
             '0e8d:2000':'MediaTek Preloader','0e8d:0003':'MediaTek BootROM (possible)'}

def stamp():
    return dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec='milliseconds')

def adb(*args, timeout=5):
    try:
        p=subprocess.run(['adb',*args],capture_output=True,text=True,timeout=timeout)
        return p.stdout.strip() if p.returncode==0 else ''
    except (OSError,subprocess.TimeoutExpired): return ''

def assess(r):
    codename=(r.get('device') or r.get('product') or '').lower()
    if codename not in KNOWN:
        r.update(software_root='Unknown',bootloader_unlock='Unknown',hardware_route='Unknown',assessment='UNREVIEWED',notes='No local rule for this device')
        return
    ceiling,description,route=KNOWN[codename]
    build=r.get('build_incremental','')
    # Avoid treating prefixed build strings as reliably comparable.
    if build.isdigit() and len(build)==len(ceiling) and int(build)<=int(ceiling):
        root='CANDIDATE: historical MTK-SU supported range (not tested)'
    else: root='UNVERIFIED: firmware outside/unknown MTK-SU supported range'
    unlock='No confirmed software-only permanent unlock' if codename=='mustang' else 'Reported software Amonet method (not guaranteed)'
    hardware='Documented hardware-assisted route' if codename=='mustang' else 'Hardware-assisted route may exist'
    r.update(software_root=root,bootloader_unlock=unlock,hardware_route=hardware,assessment='RESEARCH REQUIRED',notes=f'{description}. {route} MTK-SU last-listed build: {ceiling}.')

def scan_adb():
    out=adb('devices','-l')
    devices=[]
    for line in out.splitlines()[1:]:
        parts=line.split()
        if len(parts)<2 or parts[1]!='device': continue
        serial=parts[0]
        r={'serial':serial}
        for key,prop in PROPS.items(): r[key]=adb('-s',serial,'shell','getprop',prop)
        assess(r)
        devices.append(r)
    return devices

def usb_snapshot():
    """Poll Linux sysfs as a fallback and to capture USB identity at startup."""
    root=pathlib.Path('/sys/bus/usb/devices')
    result={}
    if not root.exists(): return result
    for node in root.iterdir():
        try:
            vendor=(node/'idVendor').read_text().strip().lower()
            product=(node/'idProduct').read_text().strip().lower()
        except (OSError,ValueError): continue
        key=f'{vendor}:{product}'
        if vendor not in ('1949','0e8d'): continue
        try: bus=(node/'busnum').read_text().strip()
        except OSError: bus=''
        try: dev=(node/'devnum').read_text().strip()
        except OSError: dev=''
        result[node.name]={'usb_path':node.name,'usb_id':key,'mode':USB_MODES.get(key,'Unknown USB mode'), 'busnum':bus,'devnum':dev}
    return result

def start_reader(command,kind,events):
    """Run a system monitor; feed its stdout into the main thread."""
    def worker():
        try:
            proc=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,bufsize=1)
        except OSError as e:
            events.put({'source':'error','time':stamp(),'message':f'{kind}: {e}'})
            return
        def drain_stderr():
            for line in proc.stderr:
                if line.strip(): events.put({'source':'error','time':stamp(),'message':f'{kind}: {line.strip()}'})
        threading.Thread(target=drain_stderr,daemon=True).start()
        if kind=='udev':
            block=[]
            for line in proc.stdout:
                if line.strip(): block.append(line.rstrip('\n'))
                elif block:
                    events.put({'source':'udev','time':stamp(),'lines':block})
                    block=[]
            if block: events.put({'source':'udev','time':stamp(),'lines':block})
        else:
            for line in proc.stdout:
                if line.strip(): events.put({'source':'dmesg','time':stamp(),'message':line.rstrip('\n')})
        code=proc.wait()
        events.put({'source':'error','time':stamp(),'message':f'{kind} monitor exited with status {code}'})
    threading.Thread(target=worker,daemon=True).start()

def write_jsonl(path,item):
    with path.open('a',encoding='utf-8') as f: f.write(json.dumps(item,ensure_ascii=False)+'\n')

def parse_udev(ev):
    lines=ev.pop('lines')
    first=lines[0]
    m=re.match(r'KERNEL\[[^]]+\]\s+(\w+)\s+(.+)',first)
    if m: ev['action']=m.group(1); ev['kernel_path']=m.group(2)
    props={}
    for line in lines[1:]:
        if '=' in line:
            key,val=line.split('=',1)
            props[key]=val
    ev['properties']=props
    raw=props.get('PRODUCT','')
    bits=raw.split('/')
    if len(bits)>=2:
        try: usb_id=f'{int(bits[0],16):04x}:{int(bits[1],16):04x}'
        except ValueError: usb_id=''
        if usb_id:
            ev['usb_id']=usb_id
            ev['mode']=USB_MODES.get(usb_id,'Unknown USB mode')
    ev['raw']=lines
    return ev

def save_inventory(path,records):
    tmp=path.with_suffix('.csv.tmp')
    with tmp.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS,extrasaction='ignore')
        w.writeheader(); w.writerows(records.values())
    tmp.replace(path)
    path.with_suffix('.json').write_text(json.dumps(list(records.values()),indent=2,ensure_ascii=False),encoding='utf-8')

def main():
    ap=argparse.ArgumentParser(description='Continuously inventory Fire tablets via ADB and USB logs (read-only).')
    ap.add_argument('--output',default='fire_inventory.csv',help='Inventory CSV output')
    ap.add_argument('--interval',type=float,default=2.0,help='Polling interval in seconds')
    ap.add_argument('--once',action='store_true',help='Capture one snapshot and exit')
    ap.add_argument('--dmesg',action='store_true',help='Also capture kernel log; uses sudo -n dmesg, needs prior sudo -v')
    ap.add_argument('--all-kernel',action='store_true',help='Retain all kernel lines, not only USB-related ones')
    args=ap.parse_args()
    path=pathlib.Path(args.output)
    path.parent.mkdir(parents=True,exist_ok=True)
    usb_log=path.with_name(path.stem+'_usb_events.jsonl')
    kernel_log=path.with_name(path.stem+'_kernel.jsonl')
    records={}
    if path.exists():
        with path.open(newline='',encoding='utf-8') as f:
            for r in csv.DictReader(f):
                if r.get('serial'): records[r['serial']]=r
    events=queue.Queue()
    if not args.once and shutil.which('udevadm'):
        start_reader(['udevadm','monitor','--kernel','--property','--subsystem-match=usb'],'udev',events)
    elif not args.once:
        print('udevadm unavailable: using USB sysfs polling only.',flush=True)
    if args.dmesg:
        if not shutil.which('sudo'):
            print('sudo unavailable; skipping dmesg.',flush=True)
        else:
            start_reader(['sudo','-n','dmesg','--follow','--human'],'dmesg',events)
    if not shutil.which('adb'): print('adb not found: USB events will still be captured, but Android properties unavailable.',flush=True)
    print(f'Watching USB + ADB. Inventory: {path}; USB events: {usb_log}; kernel: {kernel_log if args.dmesg else "disabled"}. Ctrl+C to stop.',flush=True)
    prior_usb={}
    prior_adb=set()
    next_adb=0
    try:
        while True:
            while True:
                try: ev=events.get_nowait()
                except queue.Empty: break
                if ev['source']=='udev':
                    ev=parse_udev(ev)
                    # Keep all USB udev events, including interfaces and devices.
                    write_jsonl(usb_log,ev)
                    if ev.get('usb_id') in USB_MODES:
                        print(f"[{ev['time']}] {ev.get('action','USB')} {ev['usb_id']} {ev.get('mode')} {ev['properties'].get('DEVPATH','')}",flush=True)
                elif ev['source']=='dmesg':
                    line=ev['message']
                    if re.search(r'\bwlp\w*\b',line,re.I): continue
                    if args.all_kernel or re.search(r'usb|cdc_acm|ttyACM|mediatek|fastboot|1949|0e8d|disconnect',line,re.I):
                        write_jsonl(kernel_log,ev)
                else: print('Monitor:',ev['message'],flush=True)
            current=usb_snapshot()
            for port,details in current.items():
                if port not in prior_usb or prior_usb[port]!=details:
                    ev={'source':'sysfs','time':stamp(),'action':'observed','properties':details}
                    write_jsonl(usb_log,ev)
                    print(f"[{ev['time']}] USB {details['usb_id']} {details['mode']} at {port}",flush=True)
            for port,details in prior_usb.items():
                if port not in current:
                    write_jsonl(usb_log,{'source':'sysfs','time':stamp(),'action':'disappeared','properties':details})
            prior_usb=current
            if time.monotonic()>=next_adb:
                scanned=scan_adb() if shutil.which('adb') else []
                active=set()
                for rec in scanned:
                    serial=rec['serial']; active.add(serial)
                    now=stamp(); old=records.get(serial,{})
                    rec['first_seen']=old.get('first_seen') or now
                    rec['last_seen']=now
                    records[serial]=rec
                    if serial not in prior_adb or any(old.get(k)!=rec.get(k) for k in ('build_incremental','device','model')):
                        print(f"[ADB] {rec['model']} ({rec['device']}) build={rec['build_incremental']} root={rec['software_root']}",flush=True)
                if scanned: save_inventory(path,records)
                prior_adb=active
                next_adb=time.monotonic()+max(0.5,args.interval)
            if args.once: break
            time.sleep(0.15)
    except KeyboardInterrupt: pass
    if records: save_inventory(path,records)
    print(f'Finished: {len(records)} ADB device(s) inventoried; USB events at {usb_log}',flush=True)

if __name__=='__main__': main()
