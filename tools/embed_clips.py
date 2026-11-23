"""Embed the clip manifest (clips.json) into index.html between /*CLIPS*/ and /*CLIPS_END*/."""
import json, re, sys
html, manifest = sys.argv[1], sys.argv[2]
s = open(html, encoding='utf-8').read()
m = json.load(open(manifest, encoding='utf-8'))
new = '/*CLIPS*/' + json.dumps(m, ensure_ascii=False, separators=(',', ':')) + '/*CLIPS_END*/'
s, n = re.subn(r'/\*CLIPS\*/.*?/\*CLIPS_END\*/', lambda _: new, s, flags=re.S)
assert n == 1, 'marker not found'
open(html, 'w', encoding='utf-8').write(s)
print('embedded', len(m), 'clips')
