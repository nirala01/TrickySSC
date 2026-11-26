#!/bin/bash
# usage: bash common/package.sh pNN   -> /mnt/user-data/outputs/<prefix>.zip (one folder; CSVs, then .txt, then docx)
set -e
P=$1; cd "$(dirname "$0")/.."
PFX=$(python3 -c "import importlib.util as u;s=u.spec_from_file_location('d','$P/data.py');d=u.module_from_spec(s);s.loader.exec_module(d);print(d.META['prefix'])")
T=$(mktemp -d); mkdir "$T/$PFX"
for f in questions-EN.csv questions-HI.csv solutions-EN.csv solutions-HI.csv questions-EN.txt figures.docx; do
  [ -f "$P/out/$PFX-$f" ] && cp "$P/out/$PFX-$f" "$T/$PFX/"
done
( cd "$T" && rm -f "$PFX.zip" && zip -q "$PFX.zip" "$PFX/" && for f in questions-EN.csv questions-HI.csv solutions-EN.csv solutions-HI.csv questions-EN.txt figures.docx; do [ -f "$PFX/$PFX-$f" ] && zip -q "$PFX.zip" "$PFX/$PFX-$f"; done; true )
mkdir -p /mnt/user-data/outputs
for i in 1 2 3 4 5; do cp "$T/$PFX.zip" /mnt/user-data/outputs/ && break || sleep $i; done
unzip -l "/mnt/user-data/outputs/$PFX.zip" | awk 'NR>3 && $4!=""{print $4}' | head -10
