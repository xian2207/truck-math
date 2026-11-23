# 垃圾车数学 (truck-math)

给 5–6 岁、还不认字的小朋友学加减法的网页小游戏。主题是垃圾车、分类垃圾桶、红绿灯、吸尘车。

- **在线地址**：https://xian2207.github.io/truck-math/
- **仓库**：https://github.com/xian2207/truck-math （GitHub Pages，`main` 分支根目录）

> 给 AI agent：先读完本文件再改代码。整个游戏是**一个 HTML 文件**（`index.html`），没有构建步骤、没有框架、没有依赖包。

---

## 1. 这个游戏是做什么的

教学目标：
- 认识数字 0–10，区分 0、1、2 和其他数字
- 认识符号 `+` `−` `=` `( )`
- 10 / 20 / 30 以内加减法，特别是 `0 + 5`、`17 − 9`
- 理解「零」= 一个也没有（空垃圾桶、扫干净的地面）

设计原则：孩子不认字，所以**全部靠图画和语音**。每一句话都会朗读，屏幕上的字只是给家长看的字幕。

### 关卡（`LEVELS`）

| id | 名称 | 内容 |
|---|---|---|
| `num` | 认数字 | 0 到 10 |
| `sym` | 认符号 | 加号、减号、等号 |
| `l10` | 10以内 | 加法、减法 |
| `l20` | 20以内 | 加法、减法 |
| `l30` | 30以内 | 加减法和括号 |

另有「学一学」区：数字、加号、减号、等号、零、括号的动画讲解。

### 激励机制

- 街道一开始很脏：有雾霾、垃圾堆，还有一坨卡通狗屎。
- 每答对一题，垃圾车开过去收走一堆垃圾，地上长出一朵小花。随后太阳出来、海鸥飞来、有轨电车开动，最后出现彩虹，洒水车开来做结束动画。
- 左边的卡通人物「环卫工乐乐叔叔」是原创角色。答对时他很开心，头上有太阳；答错时他捏着鼻子，苍蝇围着他飞。
- 星星可以解锁 7 辆垃圾车（车库），另外还有连对奖励。

---

## 2. 怎么打开 / 运行

- **手机、iPad**：Safari 或系统浏览器打开在线地址。
  - **推荐横屏**，界面主要按横屏设计。
  - 在微信里打开时，要先开启「我 → 设置 → 通用 → 开启横屏模式」，或者点右上角「···」选「在浏览器打开」。
  - 用 Safari「分享 → 添加到主屏幕」，可以像 App 一样全屏打开。
- **电脑**：Chrome、Edge 或 Safari 打开在线地址。右上角可以全屏（Esc 退出），A+ / A− 调整大小。
- **本地运行**：直接双击 `index.html` 也能玩，但录音要从在线地址下载，所以需要联网。如果要完全离线，在仓库根目录起一个静态服务器：
  ```bash
  python3 -m http.server 8000   # 然后打开 http://localhost:8000/
  ```
- **浏览器要求**：2022 年以后的 Chrome、Edge、Safari。用到了 CSS container queries、`dvh` 和 Web Animations API。
- **进度保存**：星星、解锁的车、缩放比例、声音开关存在浏览器 `localStorage`，key 前缀是 `gtm_`。每台设备各存各的，不同步。

---

## 3. 文件结构

```
index.html          整个游戏：HTML + CSS + JS，全部内联，无外部依赖（字体用 Google Fonts，加载失败有回退）
.nojekyll           让 GitHub Pages 原样发布
audio/<hash>.mp3    预先录好的语音片段（约 290 个，约 2MB）
tools/
  extract_lines.py  从 index.html 的 JS 里抽取所有中文台词片段 → chunks.json
  gen_clips.py      用 edge-tts 为每个片段生成 mp3 → audio/，并输出 clips.json（文字 → 文件名）
  embed_clips.py    把 clips.json 写回 index.html 里的 /*CLIPS*/…/*CLIPS_END*/
  clips.json        当前的片段清单（和 index.html 里嵌入的一致）
  check_voice_coverage.js  自检：所有可能说出的句子（约 7000 句）都能用录音拼出来。node tools/check_voice_coverage.js
  playback_test.sh  无头 Chrome 冒烟测试：切句 → 下载 → 解码 → 排程播放，输出 OK。需本机装有 Chrome
  gen_samples.py    生成试听样本（4 种音色各说几句），用于挑选音色
dev/
  voice-samples/    当初挑音色用的试听样本：晓伊、云夏、晓北（辽宁话）、云希。最终选用云夏 + 云希
  history/patch_world.py  一次性脚本：v5 改版（全屏街景）时用来拼接代码的工具，仅作留档，不需再运行
README.md           本文件
```

更早的版本看 git 历史：`git log --oneline`。每次改版都是一个 commit。

---

## 4. 代码导读（`index.html`）

整个 JS 包在一个 IIFE `(function(){ ... })();` 里，**没有全局变量**。在控制台调试要在 IIFE 内部加代码。

| 区块 / 函数 | 作用 |
|---|---|
| `S` | 状态：`zoom`、`sound`、`stars`、`truck`、`piles`。由 `LS.get/set` 读写 localStorage（带 try/catch） |
| `LEVELS`、`genLevel(id)` | 关卡定义和出题 |
| `TRUCKS`、`curTruck()` | 7 辆可解锁的车（`need` = 所需星星数） |
| `cn(n)` / `cnM(n)` | 数字转中文（`cnM` 把 2 读成「两」） |
| `addScene` / `subScene` / `binScene` | 加法（倒垃圾进车）、减法（吸尘车吸纸片）、数数的图示场景 |
| `animAdd` / `animSub` / `animCount` / `animParen` | 讲解动画。可以取消：用 `runId` 令牌判断是否已被新的动画顶替 |
| `renderQ` / `nextQ` / `onAnswer` / `help` / `finish` | 答题流程 |
| `buildCity` / `buildStreet` / `updateWorld` / `grandFinale` | 全屏街景、清洁进度（CSS 变量 `--dirty`）、通关结束动画 |
| `BUDDY` / `setMood('idle'｜'happy'｜'sad')` | 乐乐叔叔 SVG 和他的表情 |
| `say(text)` | **所有语音的入口**，返回 Promise。详见下节 |
| `tone()` / `sfx` | WebAudio 合成的音效 |

布局：`#play` 是 CSS grid，铺满一屏。横屏手机用 `@media (max-height:540px) and (orientation:landscape)`，竖屏用 `@media (orientation:portrait)`。`fitStage()` 按比例缩放题目图示，保证放得下。

---

## 5. 语音系统

`say(text)` 的流程：

1. `planClips(text)` 按标点把句子切成小块。每一块用 `segCore`（动态规划，取片段数最少）匹配 `CLIPS` 里的录音片段。比如「十七减九，等于几？」会切成 `十七` `减` `九` `等于几`。
2. 能全部匹配，就用 WebAudio 下载、解码，按顺序无缝播放。片段之间留短暂停顿：句号约 0.3 秒，逗号约 0.16 秒。
3. 出现以下情况，就回退到浏览器自带的 `speechSynthesis` 机器朗读：
   - 句子匹配不上；
   - 3.5 秒内没下载完；
   - 连续失败 3 次，这次打开期间不再尝试录音。
4. `hush()` 立即停止所有声音。

**音色**：微软 Edge 神经网络语音，通过 `edge-tts` 生成。
- 讲解、出题、表扬用 `zh-CN-YunxiaNeural`（云夏，卡通小男孩）。
- 乐乐叔叔的台词用 `zh-CN-YunxiNeural`（云希）。具体是哪几句，见 `gen_clips.py` 里的 `BUDDY_LINES`。

**录音地址**：`AUDIO_BASE` 在 `file://` 下指向线上 `https://xian2207.github.io/truck-math/audio/`，其他情况用相对路径 `audio/`。GitHub Pages 会返回 `Access-Control-Allow-Origin: *`。

### 改了台词之后必须重新生成录音

如果新增或修改了任何会被 `say()` 说出来的中文，按下面的步骤重新生成：

```bash
python3 -m venv .venv && .venv/bin/pip install edge-tts      # 另需 ffmpeg（brew install ffmpeg）
python3 tools/extract_lines.py index.html > tools/chunks.json
.venv/bin/python tools/gen_clips.py tools/chunks.json audio tools/clips.json   # 只生成缺的文件
python3 tools/embed_clips.py index.html tools/clips.json
```

- 文件名是「音色 + 文字」的 md5 前 10 位，已经有的文件不会重新生成。
- 不再使用的旧 mp3 可以手动删除。
- 含阿拉伯数字的 UI 文字不录音。例外是 `10以内` 这类关卡名，在 `gen_clips.py` 里单独映射成中文读法。
- 公司网络会拦截 HTTPS、报证书错误时，把系统根证书追加到 venv 里 `certifi` 的 `cacert.pem`。

**自检**：改完后确认每一句台词都能被 `planClips` 拼出来。切不出来的句子会自动改用机器音，不会报错，但最好补上录音。

---

## 6. 发布

```bash
git add -A && git commit -m "..." && git push
```

推送到 `main` 后，GitHub Pages 一两分钟内自动更新。用户那边刷新一下页面即可。

---

## 7. 注意事项

- 目标用户是**学龄前儿童**：按钮要大，不能依赖文字，每一步都要有语音和动画反馈。答错时不惩罚，只提示「再想想」并给出图示帮助。
- 乐乐叔叔是**原创角色**，不要换成任何现有游戏、动画里的角色或美术素材。
- 国内访问 github.io 可能较慢；微信内置浏览器可能拦截，可以改用「在浏览器打开」。
