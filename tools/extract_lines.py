import re,sys,json
s=open(sys.argv[1],encoding='utf-8').read()
js='\n'.join(re.findall(r'<script>(.*?)</script>',s,re.S))
js=re.sub(r'/\*CLIPS\*/.*?/\*CLIPS_END\*/','{}',js,flags=re.S)  # skip embedded manifest
# tokenize JS string literals; template literals split at ${...}
pieces=[];i=0;n=len(js)
def tmpl(i):
    out=[];buf=''
    while i<n:
        c=js[i]
        if c=='\\':buf+=js[i:i+2];i+=2;continue
        if c=='`':out.append(buf);return out,i+1
        if c=='$' and js[i+1]=='{':
            out.append(buf);buf='';d=1;i+=2
            while d:
                if js[i]=='`':sub,i=tmpl(i+1);out+=sub;continue
                if js[i] in "'\"":
                    q=js[i];j=i+1
                    while js[j]!=q: j+=2 if js[j]=='\\' else 1
                    out.append(js[i+1:j]);i=j+1;continue
                if js[i]=='{':d+=1
                elif js[i]=='}':d-=1
                i+=1
            continue
        buf+=c;i+=1
    return out,i
while i<n:
    c=js[i]
    if js.startswith('//',i) and (i==0 or js[i-1] in ' \n;{}'):
        i=js.find('\n',i);i=n if i<0 else i;continue
    if c in "'\"":
        j=i+1
        while j<n and js[j]!=c and js[j]!='\n': j+=2 if js[j]=='\\' else 1
        pieces.append(js[i+1:j]);i=j+1;continue
    if c=='`':
        sub,i=tmpl(i+1);pieces+=sub;continue
    i+=1
CJK=re.compile(r'[一-鿿]')
P='，。！？：；、'
chunks=set()
for p in pieces:
    if '<' in p or not CJK.search(p):continue
    for ch in re.findall(r'[^%s]+[%s]*'%(P,P),p):
        ch=ch.strip()
        core=re.sub('[%s\\s]'%P,'',ch)
        if CJK.search(core):chunks.add(ch)
print(json.dumps(sorted(chunks),ensure_ascii=False,indent=0))
