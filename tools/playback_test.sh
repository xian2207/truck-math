#!/bin/bash
# Headless Chrome smoke test: split a sentence -> fetch clips -> decode -> schedule playback.
# Usage: tools/playback_test.sh   (run from repo root; needs Google Chrome on macOS and python3)
set -e
CH="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
python3 - <<'PY'
s=open('index.html',encoding='utf-8').read()
inj='''setTimeout(async()=>{const r=document.createElement('pre');r.id='RESULT';document.body.appendChild(r);
 try{const plan=planClips('十七减九，等于几？');await Promise.all(plan.map(p=>loadClip(p.k)));const t0=performance.now();
  await playClips(plan,clipTok);r.textContent='OK clips='+plan.length+' ms='+Math.round(performance.now()-t0);
 }catch(e){r.textContent='ERR '+e}},100);
'''
i=s.rfind('})();');open('_playback_test.html','w',encoding='utf-8').write(s[:i]+inj+s[i:])
PY
python3 -m http.server 8765 >/dev/null 2>&1 & SRV=$!; trap 'kill $SRV; rm -f _playback_test.html' EXIT; sleep 1
"$CH" --headless=new --autoplay-policy=no-user-gesture-required --virtual-time-budget=60000 --dump-dom \
  "http://localhost:8765/_playback_test.html" 2>/dev/null | grep -o 'id="RESULT">[^<]*' | sed 's/id="RESULT">//'
