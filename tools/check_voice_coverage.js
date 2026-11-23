// Checks that every sentence the game can say is playable from recorded clips.
// Usage: node tools/check_voice_coverage.js [index.html]
const fs = require('fs');
const html = fs.readFileSync(process.argv[2] || 'index.html', 'utf8');
const js = html.match(/<script>([\s\S]*?)<\/script>/)[1];
const grab = (from, to) => js.slice(js.indexOf(from), js.indexOf(to));
const CLIPS = JSON.parse(js.match(/\/\*CLIPS\*\/([\s\S]*?)\/\*CLIPS_END\*\//)[1]);
const { planClips } = new Function('CLIPS', grab('function segCore', 'function loadClip') + 'return {planClips};')(CLIPS);
const D = ['零','一','二','三','四','五','六','七','八','九','十'];
const cn = n => n <= 10 ? D[n] : n < 20 ? '十' + D[n - 10] : D[Math.floor(n / 10)] + '十' + (n % 10 ? D[n % 10] : '');
const cnM = n => n === 2 ? '两' : cn(n);
const N = [...Array(31).keys()], T = [];
const trucks = [...js.matchAll(/name:'([^']+车)'/g)].map(m => m[1]);
const levels = [...js.matchAll(/\{id:'\w+',name:'([^']+)',sub:/g)].map(m => m[1]);
for (const a of N) {
  T.push(`垃圾车里有${cnM(a)}袋垃圾。`, `垃圾桶里有${cnM(a)}袋垃圾。`, `从${cn(a)}接着数：`, cn(a), `地上有${cnM(a)}张纸片。`,
    `吸尘车要把${cnM(a)}张，全部吸走！`, `吸尘车要吸走${cnM(a)}张。`, `吸走${cn(a)}`, `地上还剩${cnM(a)}张。`,
    `一共${cnM(a)}袋，就是${cn(a)}。`, `找一找，哪个是${cn(a)}？`, `是${cn(a)}。`, `等于${cn(a)}。`, `连对${cn(a)}题！`,
    `再得${cn(a)}颗星星，就能开它啦！`, `${cn(a)}。一排满满的十个，再加${cnM(a)}个。`,
    `左边${cnM(a)}袋，右边${cnM(a)}袋，两边一样多，中间用等号。`, `${cn(a)}长这样。`);
  for (const b of N) T.push(`现在一共${cnM(a + b)}袋。${cn(a)}加${cn(b)}，等于${cn(a + b)}。`, `${cn(a)}减${cn(b)}，等于几？`,
    `${cn(a)}加${cn(b)}，等于几？`, `${cn(a)}变成了${cn(b)}，中间是加号还是减号？`, `从${cn(a)}变成${cn(b)}，变多了，用加号。`,
    `地上一张也不剩，干干净净，就是零！${cn(a)}减${cn(b)}，等于零。`, `再算外面：${cn(a)}减${cn(b)}，等于${cn(a)}。`);
}
for (const t of trucks) T.push(`嘀嘀！${t}来啦！`, `${t}还锁着。再得三颗星星，就能开它啦！`, `好！现在开${t}！`, `哇！你解锁了${t}！现在就开它！`, `再得两颗星星，就能开${t}啦！`);
for (const l of levels) T.push(`${l}，通关啦！你得到了两颗星星！`);
// literal strings passed straight to say(...) or in RHYME / SYMDESC / praise arrays
for (const m of js.matchAll(/say\('([^']+)'\)/g)) T.push(m[1]);
for (const m of js.matchAll(/(?:RHYME=\[|SYMDESC=\{|say\(\[)([^\]}]+)/g)) for (const s of m[1].matchAll(/'([^']*[一-鿿][^']*)'/g)) T.push(s[1]);
const bad = [...new Set(T.filter(t => !planClips(t)))];
console.log(`tested ${T.length} sentences (${trucks.length} trucks, ${levels.length} levels), unplayable: ${bad.length}`);
bad.slice(0, 50).forEach(b => console.log('  ✗', b));
process.exit(bad.length ? 1 : 0);
