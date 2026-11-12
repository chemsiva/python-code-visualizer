#!/usr/bin/env python3
"""
Python Beginner Code Visualizer - Game Edition 🎮
Cyberpunk / Arcade gamified visualizer with CPU register HUD,
RAM memory banks, sound FX synthesis, sound effects toggle,
combo counter, and step animations.
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
  <title>🎮 CodeQuest: Python Arcade Visualizer</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Fira+Code:wght@400;600;700&display=swap');
    
    * { box-sizing: border-box; }
    body {
      margin: 0;
      padding: 16px;
      background: radial-gradient(circle at 50% 20%, #1a103c 0%, #080614 100%);
      color: #e0e7ff;
      font-family: 'Fira Code', monospace;
      min-height: 100vh;
      overflow-x: hidden;
    }

    /* Scanline effect */
    body::before {
      content: " ";
      display: block;
      position: fixed;
      top: 0; left: 0; bottom: 0; right: 0;
      background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%);
      background-size: 100% 4px;
      z-index: 1000;
      pointer-events: none;
      opacity: 0.6;
    }

    /* Top Arcade Header */
    .arcade-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 12px 20px;
      background: rgba(15, 12, 41, 0.85);
      border: 2px solid #ec4899;
      border-radius: 12px;
      box-shadow: 0 0 20px rgba(236, 72, 153, 0.4), inset 0 0 15px rgba(236, 72, 153, 0.2);
      margin-bottom: 20px;
    }
    .logo {
      font-family: 'Press Start 2P', cursive;
      font-size: 16px;
      color: #38bdf8;
      text-shadow: 0 0 8px #38bdf8, 0 0 16px #0284c7;
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .hud-stats {
      display: flex;
      gap: 20px;
      align-items: center;
      font-family: 'Press Start 2P', cursive;
      font-size: 11px;
    }
    .hud-box {
      background: #110d2e;
      border: 1px solid #6366f1;
      padding: 8px 14px;
      border-radius: 6px;
      box-shadow: 0 0 8px rgba(99, 102, 241, 0.5);
    }
    .hud-label { color: #94a3b8; font-size: 8px; margin-bottom: 4px; }
    .hud-val { color: #facc15; text-shadow: 0 0 6px #facc15; }

    /* Layout */
    .main-grid {
      display: grid;
      grid-template-columns: 1.1fr 1fr;
      gap: 20px;
    }
    .arcade-card {
      background: rgba(17, 14, 38, 0.9);
      border: 2px solid #3b82f6;
      border-radius: 12px;
      padding: 16px;
      box-shadow: 0 0 16px rgba(59, 130, 246, 0.25);
      position: relative;
    }
    .card-title {
      font-family: 'Press Start 2P', cursive;
      font-size: 11px;
      color: #a855f7;
      text-shadow: 0 0 6px #a855f7;
      margin-bottom: 14px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    textarea {
      width: 100%;
      height: 250px;
      background: #09061c;
      color: #38bdf8;
      border: 2px solid #4338ca;
      border-radius: 8px;
      padding: 12px;
      font-family: 'Fira Code', monospace;
      font-size: 13px;
      resize: none;
      outline: none;
      box-shadow: inset 0 0 10px rgba(0,0,0,0.8);
    }
    textarea:focus { border-color: #ec4899; box-shadow: 0 0 12px rgba(236, 72, 153, 0.5); }

    /* Buttons */
    .btn-row { display: flex; gap: 10px; margin-top: 14px; align-items: center; }
    .arcade-btn {
      font-family: 'Press Start 2P', cursive;
      font-size: 10px;
      padding: 12px 18px;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      transition: all 0.15s ease;
      text-transform: uppercase;
      box-shadow: 0 4px 0 rgba(0,0,0,0.4);
    }
    .btn-run {
      background: #ec4899;
      color: #fff;
      box-shadow: 0 4px 0 #9d174d, 0 0 12px rgba(236, 72, 153, 0.6);
    }
    .btn-run:hover { background: #f472b6; transform: translateY(-2px); box-shadow: 0 6px 0 #9d174d, 0 0 18px rgba(236, 72, 153, 0.9); }
    .btn-run:active { transform: translateY(2px); box-shadow: 0 2px 0 #9d174d; }

    .btn-step-next {
      background: #10b981;
      color: #064e3b;
      font-weight: bold;
      box-shadow: 0 4px 0 #047857, 0 0 12px rgba(16, 185, 129, 0.5);
    }
    .btn-step-next:hover:not(:disabled) { background: #34d399; transform: translateY(-2px); }
    .btn-step-next:disabled { background: #1e293b; color: #475569; box-shadow: none; cursor: not-allowed; }

    .btn-step-prev {
      background: #6366f1;
      color: #fff;
      box-shadow: 0 4px 0 #4338ca;
    }
    .btn-step-prev:hover:not(:disabled) { background: #818cf8; transform: translateY(-2px); }
    .btn-step-prev:disabled { background: #1e293b; color: #475569; box-shadow: none; cursor: not-allowed; }

    /* Code Stepper Panel */
    .code-stage {
      background: #09061c;
      border: 2px solid #6366f1;
      border-radius: 8px;
      min-height: 250px;
      max-height: 290px;
      overflow-y: auto;
      padding: 6px 0;
    }
    .code-row {
      display: flex;
      align-items: center;
      padding: 4px 12px;
      gap: 12px;
      font-size: 13px;
      transition: background 0.15s ease;
    }
    .num-col { color: #64748b; width: 26px; text-align: right; user-select: none; font-size: 11px; }
    .text-col { color: #cbd5e1; white-space: pre; }
    
    /* Active Glowing Line in Stepper */
    .laser-active {
      background: linear-gradient(90deg, rgba(236, 72, 153, 0.35) 0%, rgba(99, 102, 241, 0.1) 100%);
      border-left: 4px solid #ec4899;
      color: #fff !important;
      font-weight: 700;
      box-shadow: 0 0 15px rgba(236, 72, 153, 0.5);
      animation: pulseLaser 1.2s infinite alternate;
    }
    .laser-active .num-col { color: #f43f5e; font-weight: bold; }
    .laser-active .text-col { color: #fdf2f8; text-shadow: 0 0 8px #f43f5e; }

    @keyframes pulseLaser {
      from { box-shadow: 0 0 8px rgba(236, 72, 153, 0.4); }
      to { box-shadow: 0 0 16px rgba(236, 72, 153, 0.8); }
    }

    /* RAM Chip Matrix (Memory) */
    .ram-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
      gap: 10px;
      margin-top: 10px;
    }
    .ram-chip {
      background: #0f172a;
      border: 1px solid #10b981;
      border-radius: 8px;
      padding: 10px;
      box-shadow: 0 0 8px rgba(16, 185, 129, 0.25);
      animation: popIn 0.25s cubic-bezier(0.175, 0.885, 0.32, 1.275);
      position: relative;
      overflow: hidden;
    }
    .ram-chip::before {
      content: "RAM";
      position: absolute;
      top: 4px; right: 6px;
      font-size: 7px;
      color: #059669;
      font-family: 'Press Start 2P';
    }
    .ram-name { font-size: 11px; color: #38bdf8; font-weight: bold; margin-bottom: 4px; }
    .ram-type { font-size: 9px; color: #64748b; margin-bottom: 4px; }
    .ram-val {
      font-size: 14px;
      color: #facc15;
      font-weight: bold;
      word-break: break-all;
      text-shadow: 0 0 6px rgba(250, 204, 21, 0.6);
    }
    @keyframes popIn {
      0% { transform: scale(0.85); opacity: 0; }
      100% { transform: scale(1); opacity: 1; }
    }

    /* CRT Terminal Console */
    .crt-screen {
      background: #020617;
      border: 2px solid #22c55e;
      border-radius: 8px;
      padding: 10px;
      color: #4ade80;
      font-size: 12px;
      min-height: 80px;
      max-height: 120px;
      overflow-y: auto;
      white-space: pre-wrap;
      box-shadow: inset 0 0 10px rgba(34, 197, 94, 0.3);
      margin-top: 10px;
    }
  </style>
</head>
<body>

  <!-- Arcade Top Bar -->
  <div class="arcade-header">
    <div class="logo">
      <span>👾 CODEQUEST</span>
      <span style="font-size:9px;color:#ec4899;margin-left:8px;">[PYTHON 3.12 ENGINE]</span>
    </div>
    <div class="hud-stats">
      <div class="hud-box">
        <div class="hud-label">STEP COUNTER</div>
        <div class="hud-val" id="stepCounter">0 / 0</div>
      </div>
      <div class="hud-box">
        <div class="hud-label">ACTIVE VARS</div>
        <div class="hud-val" id="varCount">0 CHIPS</div>
      </div>
      <div class="hud-box">
        <div class="hud-label">AUDIO FX</div>
        <div class="hud-val" id="audioToggle" onclick="toggleAudio()" style="cursor:pointer;color:#38bdf8;">🔊 ON</div>
      </div>
    </div>
  </div>

  <!-- Game Main Grid -->
  <div class="main-grid">

    <!-- Left Quest Deck -->
    <div class="arcade-card" style="border-color:#ec4899;">
      <div class="card-title">
        <span>🎮 LEVEL 1: CODE INPUT</span>
        <select id="exampleSelect" onchange="loadExample()" style="background:#09061c;color:#a855f7;border:1px solid #a855f7;padding:4px;font-size:10px;font-family:'Fira Code';border-radius:4px;">
          <option value="ex1">Mission 1: Variable Alchemy</option>
          <option value="ex2">Mission 2: Loop Extractor</option>
          <option value="ex3">Mission 3: Branch Decision (If-Else)</option>
          <option value="ex4">Mission 4: Adsorption Energy Boss</option>
        </select>
      </div>
      
      <textarea id="codeEditor"># Mission 1: Variable Alchemy
x = 5
y = 10
total = x + y
total = total * 2
print("Final Score is:", total)</textarea>

      <div class="btn-row">
        <button class="arcade-btn btn-run" onclick="startQuest()">⚡ COMPILE & RUN</button>
      </div>

      <div class="card-title" style="margin-top:20px;color:#22c55e;">
        <span>📟 CRT CONSOLE OUTPUT</span>
      </div>
      <div class="crt-screen" id="crtOutput">READY PLAYER ONE...</div>
    </div>

    <!-- Right CPU & Memory Deck -->
    <div class="arcade-card">
      <div class="card-title">
        <span>🛰️ CPU EXECUTION STAGE</span>
      </div>

      <!-- Laser Code Line Viewer -->
      <div class="code-stage" id="codeStage">
        <div style="color:#64748b;padding:30px;text-align:center;">Press COMPILE & RUN to start execution</div>
      </div>

      <!-- Controls -->
      <div class="btn-row">
        <button class="arcade-btn btn-step-prev" id="prevBtn" onclick="prevStep()" disabled>◀ PREV</button>
        <button class="arcade-btn btn-step-next" id="nextBtn" onclick="nextStep()" disabled>NEXT STEP ▶</button>
      </div>

      <!-- RAM Memory Matrix -->
      <div class="card-title" style="margin-top:24px;color:#10b981;">
        <span>💾 RAM CHIP MATRIX (MEMORY SLOTS)</span>
      </div>
      <div class="ram-grid" id="ramGrid">
        <div style="color:#64748b;font-size:11px;">RAM clear. No active variables.</div>
      </div>
    </div>

  </div>

  <script>
    // Web Audio Synthesizer (Zero external audio files needed!)
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
      if (audioEnabled) playBeep(600, "square", 0.1);
    }

    const MISSIONS = {
      ex1: `# Mission 1: Variable Alchemy\\nx = 5\\ny = 10\\ntotal = x + y\\ntotal = total * 2\\nprint("Final Score is:", total)`,
      ex2: `# Mission 2: Loop Extractor\\nscore = 0\\nfor coin in [10, 20, 50]:\\n    score = score + coin\\n    print("Collected coin:", coin, "Total score:", score)`,
      ex3: `# Mission 3: Branch Decision\\nadsorption_energy = -4.5\\nif adsorption_energy < -3.0:\\n    status = "Exothermic (Strong Binding)"\\nelse:\\n    status = "Weak Interaction"\\nprint("Passivation Status:", status)`,
      ex4: `# Mission 4: Adsorption Energy Boss\\ndef compute_eads(complex_e, slab_e, mol_e):\\n    return complex_e - (slab_e + mol_e)\\n\\ne_complex = -312048.8\\ne_slab = -309116.6\\ne_mol = -2928.5\\nresult = compute_eads(e_complex, e_slab, e_mol)\\nprint("E_ads Result (eV):", result)`
    };

    function loadExample() {
      const v = document.getElementById("exampleSelect").value;
      document.getElementById("codeEditor").value = MISSIONS[v];
      playBeep(330, "triangle", 0.1);
    }

    let steps = [];
    let currentIdx = 0;
    let lines = [];

    async function startQuest() {
      playBeep(520, "square", 0.15);
      const code = document.getElementById("codeEditor").value;
      document.getElementById("crtOutput").innerText = ">> COMPILING PROGRAM INTO CPU REGISTERS...";

      const res = await fetch("/api/trace", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code })
      });
      const data = await res.json();

      if (data.error) {
        playBeep(180, "sawtooth", 0.3);
        document.getElementById("crtOutput").innerText = ">> SYNTAX CORRUPTION ERROR: " + data.error;
        return;
      }

      steps = data.steps;
      lines = data.code_lines;
      currentIdx = 0;

      renderCodeStage();
      renderStep(currentIdx);
      playBeep(880, "triangle", 0.12);
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

    function renderStep(idx) {
      if (!steps || steps.length === 0) return;
      const step = steps[idx];

      // Update HUD
      document.getElementById("stepCounter").innerText = `${idx + 1} / ${steps.length}`;
      const varKeys = Object.keys(step.vars || {});
      document.getElementById("varCount").innerText = `${varKeys.length} CHIPS`;

      // Highlight active line
      document.querySelectorAll(".code-row").forEach(r => r.classList.remove("laser-active"));
      const activeEl = document.getElementById(`row-${step.line}`);
      if (activeEl) {
        activeEl.classList.add("laser-active");
        activeEl.scrollIntoView({ block: "nearest", behavior: "smooth" });
      }

      // Render RAM Chips
      const ram = document.getElementById("ramGrid");
      ram.innerHTML = "";
      if (varKeys.length === 0) {
        ram.innerHTML = `<div style="color:#64748b;font-size:11px;">RAM clear. No active variables.</div>`;
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
      document.getElementById("crtOutput").innerText = step.stdout || ">> CPU EXECUTING LINE " + step.line;

      // Button states
      document.getElementById("prevBtn").disabled = (idx === 0);
      document.getElementById("nextBtn").disabled = (idx === steps.length - 1);
    }

    function nextStep() {
      if (currentIdx < steps.length - 1) {
        currentIdx++;
        playBeep(660 + (currentIdx * 25), "sine", 0.07);
        renderStep(currentIdx);
      }
    }

    function prevStep() {
      if (currentIdx > 0) {
        currentIdx--;
        playBeep(400, "triangle", 0.07);
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
        if event == 'line' and frame.f_code.co_filename == '<game_code>':
            line_no = frame.f_lineno
            user_vars = {}
            for k, v in frame.f_locals.items():
                if not k.startswith("__"):
                    val_str = repr(v)
                    if len(val_str) > 40:
                        val_str = val_str[:37] + "..."
                    user_vars[k] = {"val": val_str, "type": type(v).__name__}
            steps.append({
                "line": line_no,
                "vars": user_vars,
                "stdout": captured_out.getvalue()
            })
        return tracer

    try:
        compiled = compile(code_str, '<game_code>', 'exec')
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


class GameVisualizerHandler(SimpleHTTPRequestHandler):
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
    server = HTTPServer(("0.0.0.0", PORT), GameVisualizerHandler)
    print(f"🎮 CodeQuest Arcade Visualizer is RUNNING at http://localhost:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Game Visualizer.")
