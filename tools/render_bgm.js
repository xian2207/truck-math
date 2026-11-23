// usage: node render_bgm.js <game.html> <out.wav> <seconds>
const fs=require('fs');const {OfflineAudioContext}=require('node-web-audio-api');
const [html,out,secS]=process.argv.slice(2);const SEC=+secS||37,SR=44100;
const js=fs.readFileSync(html,'utf8');
const code=js.slice(js.indexOf('const BGM={'),js.indexOf("document.addEventListener('pointerdown',e=>"));
const off=new OfflineAudioContext(2,SR*SEC,SR);
const w={currentTime:0,sampleRate:SR,state:'running',resume(){},destination:off.destination};
['createOscillator','createGain','createBiquadFilter','createConvolver','createBuffer','createBufferSource'].forEach(k=>w[k]=(...x)=>off[k](...x));
const api=new Function('S','document','getAC','setInterval','W',`let ac=W;${code};return {bgmStart,bgmSchedule,BGM};`)(
  {sound:true},{hidden:false},()=>w,()=>0,w);
api.bgmStart();
for(let t=0;t<SEC-1.5;t+=.3){w.currentTime=t;api.bgmSchedule()}
console.log('bars scheduled',api.BGM.bar);
off.startRendering().then(buf=>{
  const L=buf.getChannelData(0),R=buf.getChannelData(1),n=L.length,b=Buffer.alloc(44+n*4);
  b.write('RIFF',0);b.writeUInt32LE(36+n*4,4);b.write('WAVEfmt ',8);b.writeUInt32LE(16,16);b.writeUInt16LE(1,20);b.writeUInt16LE(2,22);
  b.writeUInt32LE(SR,24);b.writeUInt32LE(SR*4,28);b.writeUInt16LE(4,32);b.writeUInt16LE(16,34);b.write('data',36);b.writeUInt32LE(n*4,40);
  let pk=0;for(let i=0;i<n;i++){pk=Math.max(pk,Math.abs(L[i]),Math.abs(R[i]));b.writeInt16LE(Math.round(Math.max(-1,Math.min(1,L[i]))*32767),44+i*4);b.writeInt16LE(Math.round(Math.max(-1,Math.min(1,R[i]))*32767),46+i*4)}
  fs.writeFileSync(out,b);console.log('peak',pk.toFixed(3));process.exit(0);
});
