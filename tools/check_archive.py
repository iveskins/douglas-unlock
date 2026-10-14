#!/usr/bin/env python3
"""Verify original Amonet ZIP without extracting or executing it."""
import hashlib,sys,pathlib,zipfile
EXPECTED='6647dd0b5b9d2c04a2f167f6ccc7a2cfbcaa6f1f93f8251c7a39455db77119b2'
if len(sys.argv)!=2: raise SystemExit('Usage: python3 tools/check_archive.py /path/to/amonet-douglas-v1.2.zip')
p=pathlib.Path(sys.argv[1]);digest=hashlib.sha256(p.read_bytes()).hexdigest()
print('SHA256:', digest, 'Matches inspected archive:', digest == EXPECTED)
with zipfile.ZipFile(p) as z:
 names=z.namelist()
 print('Scripts:',*[n for n in names if n.endswith('.sh')],sep=' | ')
 print('Contains brick-9820.sh:',any(n.endswith('/brick-9820.sh') for n in names))
