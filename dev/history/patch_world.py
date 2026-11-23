import sys, pathlib
p = pathlib.Path(sys.argv[1])
s = p.read_text(encoding='utf-8')

def between(s, start, end, new, keep_end=True):
    i = s.index(start); j = s.index(end, i)
    assert s.count(start) == 1, start
    return s[:i] + new + (s[j:] if keep_end else s[j+len(end):])

def rep(s, old, new, count=1):
    assert s.count(old) == count, (old, s.count(old))
    return s.replace(old, new)

HOME_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/></svg>'
SPK_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 9h4l5-4v14l-5-4H4z" fill="currentColor"/><path d="M16 9a4 4 0 0 1 0 6"/><path d="M18.5 6.5a7.5 7.5 0 0 1 0 11"/></svg>'
BULB_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18h6M10 21h4"/><path d="M12 3a6 6 0 0 0-3.5 10.9c.6.5 1 1.2 1 2.1h5c0-.9.4-1.6 1-2.1A6 6 0 0 0 12 3z" fill="#fff"/></svg>'
SUN_SVG = '<svg viewBox="0 0 100 100" aria-hidden="true"><g class="srays" stroke="#FAB005" stroke-width="6" stroke-linecap="round"><path d="M50 4v12M50 84v12M4 50h12M84 50h12M17 17l9 9M74 74l9 9M17 83l9-9M74 26l9-9"/></g><circle cx="50" cy="50" r="27" fill="#FFD43B" stroke="#FAB005" stroke-width="3"/><circle cx="41" cy="46" r="3.5" fill="#1B2A41"/><circle cx="59" cy="46" r="3.5" fill="#1B2A41"/><path d="M40 57q10 9 20 0" fill="none" stroke="#1B2A41" stroke-width="3.5" stroke-linecap="round"/><circle cx="34" cy="55" r="4.5" fill="#FF8787" opacity=".6"/><circle cx="66" cy="55" r="4.5" fill="#FF8787" opacity=".6"/></svg>'
GULL_SVG = '<svg viewBox="0 0 40 24" aria-hidden="true"><path d="M2 10q9-9 18 2q9-11 18-2" fill="none" stroke="#fff" stroke-width="4.5" stroke-linecap="round"/><path d="M2 10q9-9 18 2q9-11 18-2" fill="none" stroke="#495057" stroke-width="1.4" stroke-linecap="round"/><circle cx="20" cy="13" r="3.2" fill="#fff" stroke="#495057" stroke-width="1"/><path d="M22.5 13l4 1-4 1z" fill="#FAB005"/></svg>'
TRAM_SVG = '<svg viewBox="0 0 160 64" aria-hidden="true"><path d="M72 1l10 11M92 1l-10 11" stroke="#495057" stroke-width="2.5"/><rect x="8" y="12" width="144" height="40" rx="8" fill="#2B8A3E" stroke="#1B5E2B" stroke-width="2.5"/><rect x="8" y="36" width="144" height="7" fill="#FFF3BF"/><g fill="#D0EBFF"><rect x="16" y="18" width="16" height="13" rx="2"/><rect x="38" y="18" width="16" height="13" rx="2"/><rect x="60" y="18" width="16" height="13" rx="2"/><rect x="104" y="18" width="16" height="13" rx="2"/><rect x="126" y="18" width="16" height="13" rx="2"/></g><rect x="82" y="18" width="16" height="32" fill="#D0EBFF" stroke="#1B5E2B" stroke-width="1.5"/><text x="124" y="42" font-size="7" font-family="Fredoka,Arial,sans-serif" font-weight="700" fill="#1B5E2B">201</text><circle cx="36" cy="55" r="6.5" fill="#343A40"/><circle cx="124" cy="55" r="6.5" fill="#343A40"/></svg>'
STATION_SVG = '<svg class="station2" viewBox="0 0 40 40" aria-hidden="true"><path d="M4 18 20 6l16 12v18H4z" fill="#FFD43B" stroke="#E6A700" stroke-width="2.5"/><rect x="14" y="22" width="12" height="14" fill="#5C6B7A"/><path d="M20 6V0" stroke="#fff" stroke-width="2"/><path d="M20 0h9l-3 3 3 3h-9" fill="#E03131"/></svg>'

NEW_HTML = f'''  <!-- PLAY -->
  <section class="screen" id="play" hidden>
    <div class="world" id="world" style="--dirty:1">
      <div class="sky"></div>
      <div class="rainbow"></div>
      <div class="cloud c1"></div><div class="cloud c2"></div><div class="cloud c3"></div>
      <button class="sun" id="sun" aria-label="太阳公公">{SUN_SVG}</button>
      <svg class="city" id="city" viewBox="0 0 1200 260" preserveAspectRatio="xMidYMax slice" aria-hidden="true"></svg>
      <button class="tram" id="tram" aria-label="有轨电车">{TRAM_SVG}</button>
      <button class="gull g1" aria-label="海鸥">{GULL_SVG}</button><button class="gull g2" aria-label="海鸥">{GULL_SVG}</button><button class="gull g3" aria-label="海鸥">{GULL_SVG}</button>
      <div class="smog"></div>
    </div>
    <div class="hud">
      <button class="ib hudhome" id="hudHome" aria-label="回到首页">{HOME_SVG}</button>
      <div class="tl" id="pLight" data-on="yellow"><span class="lamp lr"></span><span class="lamp ly"></span><span class="lamp lg"></span></div>
      <button class="smell" id="smell" aria-label="街道的味道"></button>
      <div class="streak" id="streak" hidden></div>
      <div class="hudsp"></div>
      <button class="tool" id="pSay">{SPK_SVG}<span class="lbl">再听一遍</span></button>
      <button class="tool main" id="pHelp">{BULB_SVG}<span class="lbl">帮帮我</span></button>
    </div>
    <div class="buddywrap">
      <div class="bubble" id="bubble" data-mood="idle">?</div>
      <button class="buddy" id="buddy" data-mood="idle" aria-label="乐乐叔叔"></button>
    </div>
    <div class="pmain">
      <div class="stage" id="pStage"></div>
      <div class="caption" id="pCap"></div>
      <div class="ansrow"><div class="eqbox" id="pEq"></div><div class="opts" id="pOpts"></div></div>
    </div>
    <div class="road2" id="road">
      <div class="walk" id="walk"></div>
      <div class="lane" id="lane">{STATION_SVG}<div class="rtruck" id="rtruck"></div></div>
    </div>
  </section>

'''

NEW_CSS = r'''/* ===== play: one-screen street world (landscape first) ===== */
body.playing{padding-bottom:0}
body.playing .wrap{max-width:none}
#play{--bw:clamp(7rem,16vw,12rem);--roadH:5.8rem;--ts:.7;position:relative;display:grid;grid-template-columns:var(--bw) minmax(0,1fr);grid-template-rows:auto minmax(0,1fr) auto;grid-template-areas:"hud hud" "buddy main" "road road";gap:.45rem .8rem;padding:.5rem .8rem 0;box-sizing:border-box;height:calc(100vh - 4.6rem - env(safe-area-inset-top,0px) - env(safe-area-inset-bottom,0px));height:calc(100dvh - 4.6rem - env(safe-area-inset-top,0px) - env(safe-area-inset-bottom,0px));min-height:19rem;border-radius:1.4rem;overflow:hidden;border:.15rem solid var(--edge)}
.world{position:absolute;inset:0;z-index:0;overflow:hidden}
.world > *{position:absolute}
.world button{border:0;background:none;padding:0}
.sky{inset:0;background:linear-gradient(#5AB4F2,#B9E1FF 55%,#E3F4FF)}
.rainbow{left:18%;top:3%;width:64%;aspect-ratio:2/1;background:radial-gradient(50% 100% at 50% 100%,transparent 58%,#7048E8 58% 63%,#1C7ED6 63% 68%,#2F9E44 68% 73%,#FCC419 73% 78%,#F76707 78% 83%,#E03131 83% 88%,transparent 88%);opacity:0;transition:opacity 1.8s}
.world.rainbow .rainbow{opacity:.85}
.sun{left:calc(var(--bw) / 2 + .8rem - 2.4rem);top:3.4rem;width:4.8rem;z-index:1;transform:translateY(calc(var(--dirty) * 10rem));opacity:calc(1.15 - var(--dirty) * 1.5);transition:transform 1.4s ease,opacity 1.2s}
.sun svg,.tram svg,.gull svg{display:block;width:100%}
.sun .srays{transform-origin:50px 50px;animation:spin 12s linear infinite}
.cloud{left:0;width:7rem;height:2.2rem;background:#fff;border-radius:2rem;opacity:.92;animation:drift 50s linear infinite}
.cloud::before,.cloud::after{content:"";position:absolute;border-radius:50%;background:#fff}
.cloud::before{width:3.2rem;height:3.2rem;left:1.1rem;top:-1.5rem}
.cloud::after{width:2.4rem;height:2.4rem;left:3.4rem;top:-1rem}
.cloud.c1{top:14%;animation-delay:-8s}.cloud.c2{top:30%;animation-duration:64s;animation-delay:-30s}.cloud.c3{top:8%;animation-duration:70s;animation-delay:-52s;scale:.7}
@keyframes drift{from{transform:translateX(-9rem)}to{transform:translateX(110vw)}}
.city{left:0;bottom:calc(var(--roadH) - .2rem);width:100%;height:46%}
.tram{left:-12rem;bottom:calc(var(--roadH) - .25rem);width:8rem;z-index:1}
.world.lively .tram{animation:tram 18s linear infinite}
@keyframes tram{0%{left:-12rem}55%,100%{left:105%}}
.gull{width:2.4rem;opacity:0;transition:opacity 1s;z-index:1;pointer-events:none}
.world.lively .gull{opacity:1;pointer-events:auto;animation:bob 2.4s ease-in-out infinite}
.world.lively .gull.away{animation:flyaway 2s ease-in-out}
.gull.g1{top:.4rem;left:36%}.gull.g2{top:1.1rem;left:52%;animation-delay:-.8s}.gull.g3{top:.5rem;left:66%;animation-delay:-1.5s}
@keyframes bob{50%{transform:translateY(-.4rem)}}
@keyframes flyaway{50%{transform:translate(-5rem,-2rem) scale(.6)}}
.smog{inset:0;z-index:2;pointer-events:none;background:linear-gradient(rgba(105,95,60,.82),rgba(150,140,100,.55));opacity:calc(var(--dirty) * .9);transition:opacity 1.2s}
.hud,.buddywrap,.pmain,.road2{position:relative;z-index:1}
.hud,.buddywrap,.pmain{pointer-events:none}
.hud > *,.buddywrap > *,.pmain > *{pointer-events:auto}
.hud{grid-area:hud;display:flex;align-items:center;gap:.6rem;min-width:0}
.hud .hudhome{display:none}
.hud .hudsp{flex:1;pointer-events:none}
.hud .streak{position:static;box-shadow:none;font-size:1.15rem;padding:.25rem .8rem}
.hud .tool{padding:.4rem .9rem;background:rgba(255,255,255,.92)}
.hud .tool.main{background:var(--sun)}
.buddywrap{grid-area:buddy;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;min-height:0;container-type:size}
.bubble{position:relative;margin-bottom:.55rem;min-width:2.8rem;padding:.05rem .7rem;background:#fff;border:.15rem solid var(--edge);border-radius:1rem;font-family:var(--font-n);font-weight:700;font-size:1.9rem;line-height:1.2;text-align:center;color:var(--eqc)}
.bubble::after{content:"";position:absolute;left:50%;bottom:-.55rem;margin-left:-.4rem;border:.4rem solid transparent;border-top-color:#fff;border-bottom:0}
.bubble[data-mood=sad]{color:var(--harm)}
.bubble svg{display:block;width:1.9rem;height:1.9rem;margin:.15rem auto;fill:#FAB005}
#play .buddy,#play .buddy[data-mood]{flex:none;width:100%;width:min(100cqw,calc((100cqh - 3.6rem) * .7));padding:0;border:0;border-radius:0;background:none;overflow:visible}
.pmain{grid-area:main;display:grid;grid-template-rows:minmax(0,1fr) auto auto;gap:.35rem;min-height:0;min-width:0}
#play .stage{min-height:0;overflow:hidden;background:rgba(255,255,255,.74);-webkit-backdrop-filter:blur(3px);backdrop-filter:blur(3px);padding:.6rem}
#play .scene{width:max-content;flex-wrap:nowrap;flex:none}
#play .caption{justify-self:center;font-size:1.2rem;min-height:1.4em;padding:0 .7rem;border-radius:.8rem;background:rgba(255,255,255,.7)}
.ansrow{display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:.4rem 1.6rem}
#play .eq{font-size:3rem}
#play .opts{padding-top:.75rem;gap:.9rem 1rem;flex-wrap:nowrap}
#play .opt{width:5.4rem;height:5.6rem;font-size:3.2rem}
.road2{grid-area:road;height:var(--roadH);margin:0 -.8rem}
.walk{position:absolute;left:0;right:0;top:0;height:1.1rem;background:#DEE2E6;border-bottom:.3rem solid #ADB5BD}
.lane{position:absolute;left:0;right:0;top:1.4rem;bottom:0;background:var(--road);overflow:hidden}
.lane::after{content:"";position:absolute;left:0;right:0;top:55%;height:.2rem;background:repeating-linear-gradient(90deg,var(--line) 0 1.4rem,transparent 1.4rem 2.6rem)}
.lane .pile{width:calc(var(--roadH) * .5);margin-left:calc(var(--roadH) * -.25);bottom:.2rem;z-index:2;cursor:pointer}
.rtruck{position:absolute;left:.3rem;bottom:.15rem;z-index:3;transform:scale(var(--ts));transform-origin:0 100%;transition:left 1s cubic-bezier(.4,1.25,.6,1);--bag:1.3rem}
.station2{position:absolute;right:.5rem;bottom:.3rem;width:calc(var(--roadH) * .6);z-index:1}
.fl{position:absolute;bottom:.1rem;width:1.3rem;margin-left:-.65rem;transform-origin:50% 100%;animation:grow .6s cubic-bezier(.3,1.6,.6,1) both;z-index:1}
.fl svg{display:block;width:100%}
.sprinkler{position:absolute;bottom:.15rem;left:-12rem;width:calc(var(--roadH) * 1.55);z-index:4;animation:sprink 5.5s linear forwards}
.sprinkler svg{display:block;width:100%;overflow:visible}
.sprinkler .note{animation:note 1s ease-in-out infinite;transform-box:fill-box}
.sprinkler .n2{animation-delay:.5s}
@keyframes sprink{to{left:105%}}
@keyframes note{50%{transform:translateY(-6px)}}
.drop{position:absolute;width:.45rem;height:.45rem;border-radius:50%;background:#4DABF7;z-index:3}
@media (max-height:540px) and (orientation:landscape){
  :root{font-size:calc(14px * var(--zoom))}
  body.playing .top{display:none}
  #play{--bw:clamp(5rem,12vw,7.5rem);--roadH:4rem;--ts:.5;height:calc(100vh - env(safe-area-inset-top,0px) - env(safe-area-inset-bottom,0px) - .7rem);height:calc(100dvh - env(safe-area-inset-top,0px) - env(safe-area-inset-bottom,0px) - .7rem);margin-top:.35rem;padding:.35rem .6rem 0;gap:.3rem .6rem;border-radius:1rem}
  .road2{margin:0 -.6rem}
  .hud .hudhome{display:grid}
  .hud .ib{width:2.4rem;height:2.4rem}
  .hud .tool{padding:.25rem .55rem}
  .hud .tool .lbl{display:none}
  .hud .lamp{width:1rem;height:1rem}
  .smell{width:2.3rem;height:2.3rem}
  .sun{top:2.6rem;width:3.4rem}
  .tram{width:5.5rem}
  .bubble{font-size:1.3rem;min-width:2rem}
  .bubble svg{width:1.3rem;height:1.3rem}
  #play .caption{display:none}
  #play .eq{font-size:2.1rem}
  #play .opts{padding-top:.6rem;gap:.7rem}
  #play .opt{width:4.2rem;height:3.5rem;font-size:2.3rem;padding-top:.2rem}
  #play .opt::before{top:-.55rem;height:.62rem}
  .walk{height:.8rem}
  .lane{top:1.05rem}
}
@media (orientation:portrait) and (max-width:700px){
  #play{--bw:5rem}
  #play .opt{width:4.4rem;height:4.6rem;font-size:2.6rem}
  #play .eq{font-size:2.3rem}
}

'''

NEW_ROAD_JS = r'''function light(c){$('#pLight').dataset.on=c}
function moodOf(i){const n=game.qs.length,r=(n-i)/n;return r===0?3:r<=.25?2:r<=.6?1:0}
function updateSmell(){$('#smell').innerHTML=faceSVG(moodOf(game.i))}
const remPx=()=>parseFloat(getComputedStyle(document.documentElement).fontSize)||16;
const FLC=['#F06595','#FF922B','#845EF7','#FA5252','#22B8CF','#FCC419'];
function streetFlower(c){return `<svg viewBox="0 0 20 30" aria-hidden="true"><path d="M10 30V14" stroke="#2F9E44" stroke-width="2.4"/><path d="M10 23q5-5 8-1q-4 4-8 1z" fill="#40C057"/><g fill="${c}"><circle cx="10" cy="5" r="4"/><circle cx="15" cy="9" r="4"/><circle cx="5" cy="9" r="4"/><circle cx="7" cy="14" r="4"/><circle cx="13" cy="14" r="4"/></g><circle cx="10" cy="10" r="3" fill="#FCC419"/></svg>`}
let roadTruck=null;
function pileX(i,W){const n=game.qs.length;return W*(0.2+0.68*(n>1?i/(n-1):0))}
function positionTruck(){
  const lane=$('#lane'),rt=$('#rtruck');if(!lane||!game)return;
  const W=lane.clientWidth,tw=rt.getBoundingClientRect().width,R=remPx();
  let x;
  if(game.finished)x=W-R*4.6-tw;
  else if(game.i===0)x=R*.3;
  else x=pileX(game.i-1,W)+R*.4-tw;
  rt.style.left=Math.max(-tw*.25,x)+'px';
}
function updateTrack(){positionTruck()}
function layoutRoad(){
  const lane=$('#lane');if(!lane||!game)return;const W=lane.clientWidth;
  lane.querySelectorAll('.pile').forEach((p,i)=>p.style.left=pileX(i,W)+'px');
  $('#walk').querySelectorAll('.fl[data-i]').forEach(f=>f.style.left=pileX(+f.dataset.i,W)+'px');
  positionTruck();
}
function updateWorld(){const n=game.qs.length,d=Math.max(0,(n-game.i)/n),w=$('#world');w.style.setProperty('--dirty',d.toFixed(3));w.classList.toggle('lively',d<=.5)}
function buildStreet(){
  const lane=$('#lane'),walk=$('#walk'),n=game.qs.length;
  lane.querySelectorAll('.pile,.sprinkler,.drop').forEach(e=>e.remove());walk.innerHTML='';
  const rt=$('#rtruck');rt.innerHTML='';roadTruck=truckEl(0,5);roadTruck.load.style.minHeight='calc(2 * (var(--bag) * 1.1 + .22rem) - .22rem)';rt.appendChild(roadTruck.el);
  for(let i=0;i<n;i++){const p=h('div','pile',i%3===1?POOP_PILE:PILE);p.onclick=()=>{tone(150,.3,'sawtooth',.07,60);pulse(p)};lane.appendChild(p)}
  $('#world').classList.remove('rainbow');updateWorld();
  rt.style.transition='none';layoutRoad();void rt.offsetWidth;rt.style.transition='';
  updateSmell();
}
$('#smell').onclick=()=>{const m=moodOf(game.i);say(['好臭啊！快把垃圾收走吧！','还有一点点臭，加油！','快干净啦！','香香的，真干净！'][m])};
function startLevel(i){game={idx:i,lv:LEVELS[i],qs:genLevel(LEVELS[i].id),i:0,mistakes:0,streak:0,starsBefore:totalStars(),finished:false};show('play');capEl=$('#pCap');setMood('idle');buildStreet();nextQ(true)}
'''

NEW_CLEANUP = r'''    // street cleanup: truck drives to the next pile, scoops it, a flower grows, the sky clears
    const before=moodOf(game.i);game.i++;game.streak++;S.piles++;LS.set('piles',S.piles);
    positionTruck();showStreak();
    const ci=game.i-1,pile=$('#lane').querySelectorAll('.pile')[ci];
    setTimeout(()=>{
      if($('#play').hidden)return;
      if(pile&&roadTruck){const box=roadTruck.el.querySelector('.tbox'),rt=roadTruck;flyClone(pile,box.getBoundingClientRect(),{end:.3,mid:1.2,dur:600}).then(()=>{const b=bagEl(ci%3===1?'#8B5A2B':'#495057');b.classList.add('pop');rt.load.appendChild(b)});pile.style.visibility='hidden';sfx.plop()}
      const f=h('div','fl',streetFlower(FLC[ci%FLC.length]));f.dataset.i=ci;f.style.left=pileX(ci,$('#lane').clientWidth)+'px';$('#walk').appendChild(f);
      updateSmell();updateWorld();pulse($('#smell'));
    },950);
    const after=moodOf(game.i);
    let extra='';
    if([3,5,8].includes(game.streak)){confetti();sfx.fanfare();extra+=`连对${cn(game.streak)}题！`}
    if(after!==before)extra+=after===3?'街道干干净净，天也蓝了！':after===2?'太阳出来啦！':'臭味变少啦！';
'''

HELPERS = r'''/* ---------- world helpers ---------- */
const SPRINKLER='<svg viewBox="0 0 150 70" aria-hidden="true"><text class="note n1" x="30" y="10" font-size="15" fill="#7048E8">♪</text><text class="note n2" x="62" y="8" font-size="13" fill="#E03131">♫</text><rect x="10" y="16" width="88" height="36" rx="18" fill="#A5D8FF" stroke="#1971C2" stroke-width="3"/><path d="M24 26h60" stroke="#fff" stroke-width="4" stroke-linecap="round" opacity=".7"/><path d="M98 22h22q6 0 9 5l9 14v15H98z" fill="#fff" stroke="#2F9E44" stroke-width="3"/><path d="M104 27h14l7 11h-21z" fill="#D0EBFF"/><rect x="6" y="50" width="136" height="6" fill="#2F9E44"/><rect x="1" y="44" width="11" height="6" rx="2" fill="#495057"/><circle cx="34" cy="60" r="8" fill="#262B33" stroke="#555D6B" stroke-width="3"/><circle cx="118" cy="60" r="8" fill="#262B33" stroke="#555D6B" stroke-width="3"/></svg>';
function fitStage(st){
  if(!st||st.id!=='pStage')return;const s=st.firstElementChild;if(!s)return;
  s.style.transform='';const cs=getComputedStyle(st);
  const aw=st.clientWidth-parseFloat(cs.paddingLeft)-parseFloat(cs.paddingRight),ah=st.clientHeight-parseFloat(cs.paddingTop)-parseFloat(cs.paddingBottom);
  if(aw<=0||ah<=0||!s.offsetWidth||!s.offsetHeight)return;
  const k=Math.min(1,aw/s.offsetWidth,ah/s.offsetHeight);
  if(k<.999){s.style.transformOrigin='50% 100%';s.style.transform=`scale(${k.toFixed(3)})`}
}
function buildCity(){
  const W=1200,H=260,base=238;let s='';
  s+=`<rect x="0" y="150" width="${W}" height="${H-150}" fill="#74C0FC"/><path d="M0 170h${W}M0 196h${W}" stroke="#A5D8FF" stroke-width="3" stroke-dasharray="30 22"/>`;
  s+=`<g fill="#9AA9B8"><rect x="556" y="66" width="9" height="86"/><rect x="836" y="66" width="9" height="86"/><rect x="430" y="146" width="540" height="7"/></g><path d="M430 150L560 70Q700 140 840 70L970 150" fill="none" stroke="#9AA9B8" stroke-width="3"/>`;
  const cols=['#FFD8A8','#FFE3E3','#D0EBFF','#E5DBFF','#D3F9D8','#FFF3BF','#C5F6FA'];
  let x=-10,i=0;
  while(x<W){
    if(x>470&&x<930){x=930;continue}
    const w=60+((i*37)%50),hh=70+((i*53)%110),c=cols[i%cols.length],y=base-hh;
    s+=`<rect x="${x}" y="${y}" width="${w}" height="${hh}" fill="${c}" stroke="#9AA9B8" stroke-width="2"/>`;
    if(i%3===0)s+=`<path d="M${x-3} ${y}L${x+w/2} ${y-18}L${x+w+3} ${y}Z" fill="#E8590C" opacity=".75"/>`;
    for(let wy=y+12;wy<base-14;wy+=22)for(let wx=x+10;wx<x+w-14;wx+=18)s+=`<rect x="${wx}" y="${wy}" width="9" height="11" rx="1.5" fill="#fff" opacity=".85"/>`;
    if(i%2===1)s+=`<rect x="${x+w+6}" y="${base-22}" width="5" height="22" fill="#8B5A2B"/><circle cx="${x+w+8.5}" cy="${base-30}" r="13" fill="#51CF66"/>`;
    x+=w+(i%2===1?24:6);i++;
  }
  s+=`<rect x="0" y="${base}" width="${W}" height="${H-base}" fill="#ADB5BD"/><path d="M0 ${base+9}h${W}M0 ${base+16}h${W}" stroke="#868E96" stroke-width="2"/>`;
  $('#city').innerHTML=s;
}
function playTwinkle(){const N={C:523,D:587,E:659,F:698,G:784,A:880};let t=0;'C C G G A A G- F F E E D D C-'.split(' ').forEach(x=>{const long=x.endsWith('-');setTimeout(()=>tone(N[x[0]],long?.55:.28,'triangle',.1),t);t+=long?640:340})}
function spray(sp,lane){
  const r=sp.getBoundingClientRect(),lr=lane.getBoundingClientRect(),d=h('div','drop');
  d.style.left=(r.left-lr.left+r.width*.03)+'px';d.style.bottom=(lr.bottom-r.bottom+r.height*.3)+'px';lane.appendChild(d);
  d.animate([{transform:'translate(0,0)',opacity:1},{transform:`translate(${-25-Math.random()*60}px,${(Math.random()*30-18).toFixed(0)}px)`,opacity:0}],{duration:700,easing:'ease-out'}).finished.then(()=>d.remove(),()=>d.remove());
}
async function grandFinale(){
  busy=true;game.finished=true;const id=runId;
  setMood('happy');positionTruck();
  $('#world').classList.add('rainbow');
  const lane=$('#lane'),walk=$('#walk'),sp=h('div','sprinkler',SPRINKLER);lane.appendChild(sp);
  playTwinkle();
  const iv=setInterval(()=>{if(!sp.isConnected||$('#play').hidden){clearInterval(iv);return}spray(sp,lane)},80);
  const W=lane.clientWidth;
  for(let k=0;k<12;k++)setTimeout(()=>{if($('#play').hidden)return;const f=h('div','fl',streetFlower(FLC[k%FLC.length]));f.style.left=(W*(0.04+k*0.08))+'px';walk.appendChild(f)},300+k*350);
  await say('洒水车来啦！把街道洗得干干净净，还出了彩虹！');
  await wait(3200);clearInterval(iv);
  if(id!==runId||$('#play').hidden)return;
  finish();
}

/* ---------- scenes ---------- */'''

# 1. CSS: replace old narrow buddy media block, insert new world CSS before /* done */
s = between(s, "@media (max-width:600px){\n  .buddy{width:5.4rem}", "/* done */", NEW_CSS)
# 2. HTML play section
s = between(s, "  <!-- PLAY -->", "  <!-- DONE -->", NEW_HTML)
# 3. road/street JS
s = between(s, "function light(c){", "function renderQ(q){", NEW_ROAD_JS)
# 4. cleanup inside onAnswer
s = between(s, "    // street cleanup", "    const praise=", NEW_CLEANUP)
# 5. finale
s = rep(s, "if(game.i>=game.qs.length)finish();else nextQ()", "if(game.i>=game.qs.length)grandFinale();else nextQ()")
# 6. mood bubble
s = rep(s, "function setMood(m){clearTimeout(moodTimer);const b=$('#buddy');if(b)b.dataset.mood=m}",
        "function setMood(m){clearTimeout(moodTimer);const b=$('#buddy');if(b)b.dataset.mood=m;const bb=$('#bubble');if(bb){bb.dataset.mood=m;bb.innerHTML=m==='happy'?STAR:m==='sad'?'!':'?'}}")
# 7. playing class
s = rep(s, "$('#streak').hidden=true}", "$('#streak').hidden=true;document.body.classList.toggle('playing',id==='play')}")
# 8. stage sizing
s = rep(s, "truck=truckEl(a,colsFor(Math.max(a+b,1)));",
        "truck=truckEl(a,colsFor(Math.max(a+b,1)));truck.load.style.minHeight=`calc(${Math.ceil(Math.max(a+b,1)/5)} * (var(--bag) * 1.1 + .22rem) - .22rem)`;")
s = rep(s, "s.append(bu.el,tu.el);stage.append(s);", "s.append(bu.el,tu.el);stage.append(s);fitStage(stage);")
s = rep(s, "s.append(gu.el,su.el);stage.append(s);", "s.append(gu.el,su.el);stage.append(s);fitStage(stage);")
s = rep(s, "s.append(bu.el);stage.append(s);", "s.append(bu.el);stage.append(s);fitStage(stage);")
s = rep(s, "renderQ(cur);updateTrack();", "renderQ(cur);fitStage($('#pStage'));updateTrack();")
# 9. helpers
s = rep(s, "/* ---------- scenes ---------- */", HELPERS)
# 10. intro line
s = rep(s, "街上好臭啊！我们开着垃圾车，答对一题，就收走一堆垃圾！", "街上好臭啊，天都变灰了！我们开着垃圾车，答对一题，就收走一堆垃圾，天就会变蓝！")
# 11. init: buddy, city, easter eggs, resize
s = rep(s, "$('#buddy').innerHTML=BUDDY;$('#doneBuddy').innerHTML=BUDDY;",
r"""$('#buddy').innerHTML=BUDDY.replace('<svg ','<svg preserveAspectRatio="xMidYMax meet" ');$('#doneBuddy').innerHTML=BUDDY;
buildCity();
$('#sun').onclick=()=>{tone(660,.15);setTimeout(()=>tone(990,.22),130)};
document.querySelectorAll('.gull').forEach(g=>g.onclick=()=>{tone(1400,.09,'square',.05,900);setTimeout(()=>tone(1300,.12,'square',.05,800),140);g.classList.remove('away');void g.offsetWidth;g.classList.add('away')});
$('#tram').onclick=()=>{tone(1568,.12,'triangle',.15);setTimeout(()=>tone(1568,.2,'triangle',.15),210)};
$('#hudHome').onclick=()=>{show('home');renderHome()};
window.addEventListener('resize',()=>{if(!$('#play').hidden&&game){layoutRoad();fitStage($('#pStage'))}});""")

p.write_text(s, encoding='utf-8')
print("ok", len(s))
