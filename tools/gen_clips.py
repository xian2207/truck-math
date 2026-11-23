import asyncio, edge_tts, json, re, hashlib, os, sys, subprocess
chunks_file, outdir, manifest_out = sys.argv[1:4]
os.makedirs(outdir, exist_ok=True)
NARR, BUDDY = 'zh-CN-YunxiaNeural', 'zh-CN-YunxiNeural'
BUDDY_LINES = ['哈哈，太好了！太阳出来了，小花也开了！','好臭好臭！地上有一坨臭臭！快帮我算对，把它收走！',
 '我是环卫工乐乐叔叔！你答对了，我就开心；答错了，苍蝇就来找我啦！','哎呀，好臭！是谁的臭臭？','哎呀，差点踩到臭臭！','苍蝇围着臭臭飞来啦！']
P='，。！？：；、'
core=lambda t: re.sub(r'[%s\s“”]'%P,'',t)
buddy_cores={core(ch) for l in BUDDY_LINES for ch in re.findall(r'[^%s]+[%s]*'%(P,P),l)}
D='零一二三四五六七八九十'
def cn(n):
    if n<=10: return D[n]
    if n<20: return '十'+D[n-10]
    return D[n//10]+'十'+(D[n%10] if n%10 else '')
chunks=[x for x in json.load(open(chunks_file)) if not re.search(r'[A-Za-z0-9×]',x)]
items={}
for n in range(31): items[cn(n)]=cn(n)
items['两']='两'
for k,t in {'10以内':'十以内','20以内':'二十以内','30以内':'三十以内'}.items(): items[k]=t
for ch in chunks:
    k=core(ch)
    if k not in items or ch[-1] in '。！？': items[k]=ch.strip()
manifest={}; todo=[]
for k,text in items.items():
    v=BUDDY if k in buddy_cores else NARR
    h=hashlib.md5((v+'|'+text).encode()).hexdigest()[:10]
    manifest[k]=h
    if not os.path.exists(f'{outdir}/{h}.mp3'): todo.append((text,v,h))
print('clips',len(manifest),'to generate',len(todo))
sem=asyncio.Semaphore(6)
async def gen(text,v,h):
    async with sem:
        raw=f'{outdir}/{h}.raw.mp3'
        for attempt in range(4):
            try:
                await edge_tts.Communicate(text,v,rate='-8%' if v==NARR else '-5%').save(raw); break
            except Exception as e:
                if attempt==3: print('FAIL',text,e); return
                await asyncio.sleep(2)
        af='silenceremove=start_periods=1:start_threshold=-50dB,areverse,silenceremove=start_periods=1:start_threshold=-50dB,areverse'
        p=await asyncio.create_subprocess_exec('ffmpeg','-v','error','-y','-i',raw,'-af',af,'-ac','1','-ar','24000','-b:a','48k',f'{outdir}/{h}.mp3')
        await p.wait(); os.remove(raw)
async def main(): await asyncio.gather(*(gen(*t) for t in todo))
asyncio.run(main())
missing=[k for k,h in manifest.items() if not os.path.exists(f'{outdir}/{h}.mp3')]
print('missing',missing)
json.dump(manifest,open(manifest_out,'w'),ensure_ascii=False,separators=(',',':'))
