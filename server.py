#!/usr/bin/env python3
"""
Python Beginner Code Visualizer - Game & Mind Map Edition 🧠🎮
Includes:
- Interactive Visual Mind Map (Tree/Flow of execution)
- Memory RAM Chips
- Step-by-Step Code Laser
- Sound FX
"""
import sys
import json
import io
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = 8089

INDEX_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>🧠 CodeQuest: Visual Mind Map & Python Arcade</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Fira+Code:wght@400;600;700&display=swap');
    
    * { box-sizing: border-box; }
    body {
      margin: 0;
      padding: 16px;
      background: radial-gradient(circle at 50% 15%, #181236 0%, #080614 100%);
      color: #e0e7ff;
      font-family: 'Fira Code', monospace;
      min-height: 100vh;
    }

    /* Top Header */
    .arcade-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 12px 20px;
      background: rgba(15, 12, 41, 0.9);
      border: 2px solid #ec4899;
      border-radius: 12px;
      box-shadow: 0 0 20px rgba(236, 72, 153, 0.35);
      margin-bottom: 16px;
    }
    .logo {
      font-family: 'Press Start 2P', cursive;
      font-size: 15px;
      color: #38bdf8;
      text-shadow: 0 0 8px #38bdf8;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .hud-stats { display: flex; gap: 14px; font-family: 'Press Start 2P', cursive; font-size: 10px; }
    .hud-box {
      background: #110d2e;
      border: 1px solid #6366f1;
      padding: 6px 12px;
      border-radius: 6px;
    }
    .hud-label { color: #94a3b8; font-size: 8px; margin-bottom: 2px; }
    .hud-val { color: #facc15; }

    /* Main Grid */
    .grid-top {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
      margin-bottom: 16px;
    }
    .arcade-card {
      background: rgba(17, 14, 38, 0.95);
      border: 2px solid #3b82f6;
      border-radius: 12px;
      padding: 14px;
      box-shadow: 0 0 14px rgba(59, 130, 246, 0.2);
    }
    .card-title {
      font-family: 'Press Start 2P', cursive;
      font-size: 10px;
      color: #a855f7;
      margin-bottom: 12px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    textarea {
      width: 100%;
      height: 180px;
      background: #09061c;
      color: #38bdf8;
      border: 1px solid #4338ca;
      border-radius: 6px;
      padding: 10px;
      font-family: 'Fira Code', monospace;
      font-size: 13px;
      resize: none;
      outline: none;
    }
    .btn-row { display: flex; gap: 10px; margin-top: 10px; align-items: center; }
    .arcade-btn {
      font-family: 'Press Start 2P', cursive;
      font-size: 10px;
      padding: 10px 16px;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      transition: 0.15s;
    }
    .btn-run { background: #ec4899; color: #fff; box-shadow: 0 3px 0 #9d174d; }
    .btn-run:hover { background: #f472b6; transform: translateY(-1px); }
    .btn-step-next { background: #10b981; color: #064e3b; font-weight: bold; }
    .btn-step-next:disabled { background: #1e293b; color: #475569; cursor: not-allowed; }
    .btn-step-prev { background: #6366f1; color: #fff; }
    .btn-step-prev:disabled { background: #1e293b; color: #475569; cursor: not-allowed; }

    /* Code Stepper */
    .code-stage {
      background: #09061c;
      border: 1px solid #475569;
      border-radius: 6px;
      height: 180px;
      overflow-y: auto;
      padding: 4px 0;
    }
    .code-row { display: flex; padding: 3px 10px; gap: 10px; font-size: 13px; }
    .num-col { color: #64748b; width: 22px; text-align: right; }
    .text-col { color: #cbd5e1; white-space: pre; }
    .laser-active {
      background: linear-gradient(90deg, rgba(236, 72, 153, 0.4) 0%, rgba(99, 102, 241, 0.15) 100%);
      border-left: 4px solid #ec4899;
      color: #fff !important;
      font-weight: bold;
    }
    .laser-active .text-col { color: #fdf2f8; text-shadow: 0 0 6px #f43f5e; }

    /* MIND MAP SECTION */
    .mindmap-card {
      background: rgba(13, 10, 31, 0.95);
      border: 2px solid #10b981;
      border-radius: 12px;
      padding: 16px;
      box-shadow: 0 0 16px rgba(16, 185, 129, 0.25);
      margin-bottom: 16px;
    }
    .mindmap-container {
      display: flex;
      gap: 14px;
      overflow-x: auto;
      padding: 12px 6px;
      align-items: center;
    }
    .mindmap-node {
      background: #0f172a;
      border: 2px solid #475569;
      border-radius: 10px;
      padding: 10px 14px;
      min-width: 170px;
      max-width: 200px;
      flex-shrink: 0;
      position: relative;
      transition: all 0.25s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .node-header {
      font-family: 'Press Start 2P', cursive;
      font-size: 8px;
      color: #94a3b8;
      margin-bottom: 6px;
      display: flex;
      justify-content: space-between;
    }
    .node-code {
      font-size: 12px;
      color: #38bdf8;
      font-weight: bold;
      margin-bottom: 6px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .node-explain {
      font-size: 11px;
      color: #cbd5e1;
      line-height: 1.35;
      background: rgba(0,0,0,0.3);
      padding: 6px;
      border-radius: 4px;
    }
    .node-arrow {
      color: #6366f1;
      font-size: 20px;
      font-weight: bold;
      user-select: none;
    }

    /* Active Mind Map Node */
    .node-current {
      border-color: #ec4899;
      background: #25123d;
      transform: scale(1.06);
      box-shadow: 0 0 16px rgba(236, 72, 153, 0.7);
    }
    .node-current .node-header { color: #f43f5e; }
    .node-current .node-code { color: #facc15; text-shadow: 0 0 6px #facc15; }
    .node-past {
      border-color: #10b981;
      opacity: 0.85;
    }
    .node-past .node-header { color: #34d399; }

    /* Bottom: RAM & Output */
    .grid-bottom {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
    }
    .ram-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
      gap: 10px;
    }
    .ram-chip {
      background: #0f172a;
      border: 1px solid #10b981;
      border-radius: 6px;
      padding: 8px;
      position: relative;
    }
    .ram-name { font-size: 11px; color: #38bdf8; font-weight: bold; }
    .ram-type { font-size: 8px; color: #64748b; }
    .ram-val { font-size: 13px; color: #facc15; font-weight: bold; word-break: break-all; margin-top: 3px; }
    .crt-screen {
      background: #020617;
      border: 1px solid #22c55e;
      border-radius: 6px;
      padding: 8px;
      color: #4ade80;
      font-size: 12px;
      min-height: 80px;
      white-space: pre-wrap;
    }
  </style>
</head>
<body>

  <!-- Top Bar -->
  <div class="arcade-header">
    <div class="logo">
      <span>🧠 CODEQUEST : MIND MAP EDITION</span>
    </div>
    <div class="hud-stats">
      <div class="hud-box">
        <div class="hud-label">EXECUTION STEP</div>
        <div class="hud-val" id="stepCounter">0 / 0</div>
      </div>
      <div class="hud-box">
        <div class="hud-label">AUDIO FX</div>
        <div class="hud-val" id="audioToggle" onclick="toggleAudio()" style="cursor:pointer;color:#38bdf8;">🔊 ON</div>
      </div>
    </div>
  </div>

  <!-- Top Row: Editor + Stepper -->
  <div class="grid-top">
    <div class="arcade-card">
      <div class="card-title">
        <span>📝 1. WRITE CODE</span>
        <select id="exampleSelect" onchange="loadExample()" style="background:#09061c;color:#a855f7;border:1px solid #a855f7;padding:3px;font-size:10px;font-family:'Fira Code';">
          <option value="ex1">Mission 1: Variable Flow</option>
          <option value="ex2">Mission 2: Loop Extractor</option>
          <option value="ex3">Mission 3: Branch Decision (If-Else)</option>
          <option value="ex4">Mission 4: Adsorption Energy</option>
        </select>
      </div>
      <textarea id="codeEditor"># Student Code Example
x = 5
y = 10
total = x + y
total = total * 2
print("Final Score is:", total)</textarea>
      <div class="btn-row">
        <button class="arcade-btn btn-run" onclick="startQuest()">⚡ GENERATE MIND MAP & RUN</button>
      </div>
    </div>

    <div class="arcade-card">
      <div class="card-title"><span>🛰️ 2. LINE EXECUTION</span></div>
      <div class="code-stage" id="codeStage">
        <div style="color:#64748b;padding:30px;text-align:center;">Click GENERATE to trace code</div>
      </div>
      <div class="btn-row">
        <button class="arcade-btn btn-step-prev" id="prevBtn" onclick="prevStep()" disabled>◀ PREV</button>
        <button class="arcade-btn btn-step-next" id="nextBtn" onclick="nextStep()" disabled>NEXT STEP ▶</button>
      </div>
    </div>
  </div>

  <!-- MIDDLE: INTERACTIVE MIND MAP -->
  <div class="mindmap-card">
    <div class="card-title" style="color:#10b981;">
      <span>🗺️ 3. INTERACTIVE EXECUTION MIND MAP (STEP-BY-STEP FLOW)</span>
      <span style="font-size:9px;color:#94a3b8;">[Follows computer decision tree in real-time]</span>
    </div>
    <div class="mindmap-container" id="mindmapFlow">
      <div style="color:#64748b;font-size:12px;padding:12px;">Mind map will dynamically generate after running code...</div>
    </div>
  </div>

  <!-- Bottom: Memory + Console -->
  <div class="grid-bottom">
    <div class="arcade-card">
      <div class="card-title" style="color:#10b981;"><span>💾 COMPUTER MEMORY (RAM CHIPS)</span></div>
      <div class="ram-grid" id="ramGrid">
        <div style="color:#64748b;font-size:11px;">No active variables.</div>
      </div>
    </div>
    <div class="arcade-card">
      <div class="card-title" style="color:#22c55e;"><span>📟 CONSOLE OUTPUT</span></div>
      <div class="crt-screen" id="crtOutput">(Output will appear here)</div>
    </div>
  </div>

  <script>
    let audioCtx = null;
    let audioEnabled = true;

    function playBeep(freq = 440, type = "sine", duration = 0.08) {
      if (!audioEnabled) return;
      try {
        if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = type;
        osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
        gain.gain.setValueAtTime(0.08, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + duration);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + duration);
      } catch(e) {}
    }

    function toggleAudio() {
      audioEnabled = !audioEnabled;
      document.getElementById("audioToggle").innerText = audioEnabled ? "🔊 ON" : "🔇 OFF";
    }

    const MISSIONS = {
      ex1: `# Mission 1: Variable Flow\\nx = 5\\ny = 10\\ntotal = x + y\\ntotal = total * 2\\nprint("Final Score is:", total)`,
      ex2: `# Mission 2: Loop Extractor\\nscore = 0\\nfor coin in [10, 20, 50]:\\n    score = score + coin\\n    print("Got coin:", coin, "Total:", score)`,
      ex3: `# Mission 3: Branch Decision\\ne_ads = -4.5\\nif e_ads < -3.0:\\n    status = "Strong Adsorption"\\nelse:\\n    status = "Weak Adsorption"\\nprint("Status is:", status)`,
      ex4: `# Mission 4: Adsorption Energy\\ndef calc_eads(tot, slab, mol):\\n    return tot - (slab + mol)\\n\\ne_tot = -312048.8\\ne_slab = -309116.6\\ne_mol = -2928.5\\nresult = calc_eads(e_tot, e_slab, e_mol)\\nprint("E_ads is:", result)`
    };

    function loadExample() {
      const v = document.getElementById("exampleSelect").value;
      document.getElementById("codeEditor").value = MISSIONS[v];
    }

    let steps = [];
    let currentIdx = 0;
    let lines = [];

    // Helper: Generate simple beginner explanation for any line
    function explainCode(lineText, vars) {
      const t = lineText.trim();
      if (!t) return "Empty line or comment.";
      if (t.startsWith("#")) return "Comment: Ignored by computer.";
      if (t.startsWith("print(")) return "Output Action: Sends text/values to the screen.";
      if (t.startsWith("def ")) return "Function Blueprint: Memorizes this reusable block.";
      if (t.startsWith("return ")) return "Return: Hands the computed result back to caller.";
      if (t.startsWith("for ")) return "Loop Engine: Picks each item one-by-one from the list.";
      if (t.startsWith("if ")) return "Decision Fork: Checks if condition is TRUE or FALSE.";
      if (t.startsWith("else:")) return "Fallback Fork: Runs when IF condition failed.";
      if (t.includes(" = ")) {
        const parts = t.split(" = ");
        return `Memory Store: Computes '${parts[1]}' and saves into variable '${parts[0].trim()}'.`;
      }
      return "Execution step.";
    }

    async function startQuest() {
      playBeep(520, "square", 0.15);
      const code = document.getElementById("codeEditor").value;

      const res = await fetch("/api/trace", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code })
      });
      const data = await res.json();

      if (data.error) {
        document.getElementById("crtOutput").innerText = "Syntax Error: " + data.error;
        return;
      }

      steps = data.steps;
      lines = data.code_lines;
      currentIdx = 0;

      renderCodeStage();
      buildMindMapFlow();
      renderStep(currentIdx);
    }

    function renderCodeStage() {
      const stage = document.getElementById("codeStage");
      stage.innerHTML = "";
      lines.forEach((t, i) => {
        const no = i + 1;
        const row = document.createElement("div");
        row.className = "code-row";
        row.id = `row-${no}`;
        row.innerHTML = `<span class="num-col">${no}</span><span class="text-col">${escapeHtml(t)}</span>`;
        stage.appendChild(row);
      });
    }

    function buildMindMapFlow() {
      const container = document.getElementById("mindmapFlow");
      container.innerHTML = "";

      steps.forEach((st, idx) => {
        const lineText = lines[st.line - 1] || "";
        const node = document.createElement("div");
        node.className = "mindmap-node";
        node.id = `map-node-${idx}`;
        node.onclick = () => { currentIdx = idx; renderStep(currentIdx); };

        const explain = explainCode(lineText, st.vars);
        node.innerHTML = `
          <div class="node-header"><span>STEP ${idx + 1}</span><span>L${st.line}</span></div>
          <div class="node-code">${escapeHtml(lineText.trim() || "[end]")}</div>
          <div class="node-explain">${explain}</div>
        `;
        container.appendChild(node);

        if (idx < steps.length - 1) {
          const arrow = document.createElement("div");
          arrow.className = "node-arrow";
          arrow.innerText = "➔";
          container.appendChild(arrow);
        }
      });
    }

    function renderStep(idx) {
      if (!steps || steps.length === 0) return;
      const step = steps[idx];

      document.getElementById("stepCounter").innerText = `${idx + 1} / ${steps.length}`;

      // Highlight Stepper Line
      document.querySelectorAll(".code-row").forEach(r => r.classList.remove("laser-active"));
      const activeEl = document.getElementById(`row-${step.line}`);
      if (activeEl) {
        activeEl.classList.add("laser-active");
        activeEl.scrollIntoView({ block: "nearest", behavior: "smooth" });
      }

      // Highlight Mind Map Nodes
      steps.forEach((_, i) => {
        const nodeEl = document.getElementById(`map-node-${i}`);
        if (!nodeEl) return;
        nodeEl.classList.remove("node-current", "node-past");
        if (i === idx) {
          nodeEl.classList.add("node-current");
          nodeEl.scrollIntoView({ inline: "center", behavior: "smooth" });
        } else if (i < idx) {
          nodeEl.classList.add("node-past");
        }
      });

      // RAM Chips
      const ram = document.getElementById("ramGrid");
      ram.innerHTML = "";
      const varKeys = Object.keys(step.vars || {});
      if (varKeys.length === 0) {
        ram.innerHTML = `<div style="color:#64748b;font-size:11px;">No active variables.</div>`;
      } else {
        varKeys.forEach(k => {
          const item = step.vars[k];
          const chip = document.createElement("div");
          chip.className = "ram-chip";
          chip.innerHTML = `
            <div class="ram-name">${k}</div>
            <div class="ram-type">&lt;${item.type}&gt;</div>
            <div class="ram-val">${escapeHtml(String(item.val))}</div>
          `;
          ram.appendChild(chip);
        });
      }

      // Console
      document.getElementById("crtOutput").innerText = step.stdout || "(No output yet)";

      document.getElementById("prevBtn").disabled = (idx === 0);
      document.getElementById("nextBtn").disabled = (idx === steps.length - 1);
    }

    function nextStep() {
      if (currentIdx < steps.length - 1) {
        currentIdx++;
        playBeep(650 + (currentIdx * 20), "sine", 0.06);
        renderStep(currentIdx);
      }
    }

    function prevStep() {
      if (currentIdx > 0) {
        currentIdx--;
        playBeep(400, "triangle", 0.06);
        renderStep(currentIdx);
      }
    }

    function escapeHtml(str) {
      return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    }
  </script>
</body>
</html>
"""

def execute_trace(code_str):
    steps = []
    lines = code_str.splitlines()

    old_stdout = sys.stdout
    captured_out = io.StringIO()
    sys.stdout = captured_out

    def tracer(frame, event, arg):
        if event == 'line' and frame.f_code.co_filename == '<mindmap_code>':
            line_no = frame.f_lineno
            user_vars = {}
            for k, v in frame.f_locals.items():
                if not k.startswith("__"):
                    val_str = repr(v)
                    if len(val_str) > 35:
                        val_str = val_str[:32] + "..."
                    user_vars[k] = {"val": val_str, "type": type(v).__name__}
            steps.append({
                "line": line_no,
                "vars": user_vars,
                "stdout": captured_out.getvalue()
            })
        return tracer

    try:
        compiled = compile(code_str, '<mindmap_code>', 'exec')
        sys.settrace(tracer)
        exec(compiled, {})
    except Exception as e:
        sys.settrace(None)
        sys.stdout = old_stdout
        return {"error": str(e), "code_lines": lines, "steps": []}
    finally:
        sys.settrace(None)
        sys.stdout = old_stdout

    if steps:
        final_vars = steps[-1]["vars"]
    else:
        final_vars = {}
    steps.append({
        "line": len(lines),
        "vars": final_vars,
        "stdout": captured_out.getvalue()
    })

    return {"steps": steps, "code_lines": lines, "error": None}


class MindMapVisualizerHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(INDEX_HTML.encode("utf-8"))

    def do_POST(self):
        if self.path == "/api/trace":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode("utf-8")
            data = json.loads(body)
            code = data.get("code", "")
            result = execute_trace(code)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(result).encode("utf-8"))


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), MindMapVisualizerHandler)
    print(f"🧠 CodeQuest Mind Map Visualizer is RUNNING at http://localhost:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Mind Map Server.")
