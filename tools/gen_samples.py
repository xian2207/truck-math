import asyncio, edge_tts, sys, os
out=sys.argv[1]  # usage: python tools/gen_samples.py dev/voice-samples
V={'1_晓伊_卡通小姐姐':'zh-CN-XiaoyiNeural','2_云夏_卡通小男孩':'zh-CN-YunxiaNeural','3_晓北_东北话':'zh-CN-liaoning-XiaobeiNeural','4_云希_阳光大哥哥':'zh-CN-YunxiNeural'}
LINES=['嘀嘀！绿色垃圾车来啦！',
 '减号，就是拿走，变少啦！看，纸片跑到吸尘车肚子里去了。',
 '哎呀，好臭！是谁的臭臭？不对哦，再想想。',
 '太棒了！太阳出来啦，小花也开了！']
PIECES=['十七','减','九','等于','八']
async def one(text,voice,path,rate='+0%',pitch='+0Hz'):
    await edge_tts.Communicate(text,voice,rate=rate,pitch=pitch).save(path)
async def main():
    for name,v in V.items():
        parts=[]
        for i,t in enumerate(LINES):
            p=f'{out}/_{name}_{i}.mp3';await one(t,v,p,rate='-5%');parts.append(p)
        for i,t in enumerate(PIECES):
            p=f'{out}/_{name}_p{i}.mp3';await one(t,v,p,rate='-10%');parts.append(p)
        with open(f'{out}/{name}.mp3','wb') as f:
            for p in parts: f.write(open(p,'rb').read()); os.remove(p)
        print('ok',name)
asyncio.run(main())
