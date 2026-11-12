#!/usr/bin/env python3
"""
Interactive Beginner Code Visualizer GUI
Runs a lightweight web GUI where students can write/edit code,
click 'Run / Step', and see the execution line-by-line with variables changing.
"""
import sys
import json
import trace
import io
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = 8089

INDEX_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Python Beginner Code Visualizer</title>
  <style>
    * { box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
    body { margin: 0; padding: 20px; background: #0f172a; color: #f8fafc; }
    h1 { font-size: 22px; margin-top: 0; color: #38bdf8; display: flex; align-items: center; gap: 8px; }
    .subtitle { color: #94a3b8; font-size: 14px; margin-bottom: 20px; }
    .grid { display: grid; grid-template-columns: 1.1fr 1fr; gap: 20px; }
    .panel { background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 16px; display: flex; flex-direction: column; }
    .panel-title { font-weight: 600; font-size: 15px; margin-bottom: 12px; color: #cbd5e1; display: flex; justify-content: space-between; align-items: center; }
    textarea { width: 100%; height: 260px; background: #0b1120; color: #38bdf8; border: 1px solid #475569; border-radius: 8px; padding: 12px; font-family: "Fira Code", monospace; font-size: 14px; resize: none; outline: none; }
    .btn-row { display: flex; gap: 10px; margin-top: 14px; }
    button { padding: 8px 16px; border-radius: 6px; border: none; font-weight: 600; cursor: pointer; transition: 0.15s; font-size: 13px; }
    .btn-primary { background: #38bdf8; color: #0f172a; }
    .btn-primary:hover { background: #0284c7; color: #fff; }
    .btn-secondary { background: #334155; color: #f8fafc; }
    .btn-secondary:hover { background: #475569; }
    .btn-step { background: #10b981; color: #fff; }
    .btn-step:hover { background: #059669; }
    .btn-step:disabled { background: #1e3a30; color: #64748b; cursor: not-allowed; }
    
    /* Code Viewer with Line Highlights */
    .code-view { background: #0b1120; border: 1px solid #475569; border-radius: 8px; padding: 8px 0; font-family: "Fira Code", monospace; font-size: 14px; min-height: 260px; overflow-y: auto; }
    .code-line { padding: 3px 12px; display: flex; gap: 12px; }
    .line-no { color: #64748b; width: 28px; text-align: right; user-select: none; }
    .line-text { color: #e2e8f0; white-space: pre; }
    .active-line { background: #0284c7; color: #fff; font-weight: bold; border-left: 4px solid #38bdf8; }
    .active-line .line-no { color: #ffffff; }

    /* Variables Table */
    .var-table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 13px; font-family: monospace; }
    .var-table th { text-align: left; background: #0b1120; padding: 8px; color: #94a3b8; border-bottom: 1px solid #334155; }
    .var-table td { padding: 8px; border-bottom: 1px solid #334155; color: #f1f5f9; }
    .var-changed { background: rgba(16, 185, 129, 0.2); color: #34d399 !important; font-weight: bold; }
    .step-counter { color: #38bdf8; font-size: 13px; font-weight: bold; }
    .terminal-out { background: #0b1120; border: 1px solid #334155; border-radius: 8px; padding: 10px; font-family: monospace; font-size: 13px; color: #a7f3d0; min-height: 60px; white-space: pre-wrap; margin-top: 10px; }
  </style>
</head>
<body>

  <h1>🔍 Python Beginner Code Visualizer (Step-by-Step)</h1>
  <div class="subtitle">Designed for students to visualize how memory, variables, and line execution work in real-time.</div>

  <div class="grid">
    <!-- Left: Code Editor -->
    <div class="panel">
      <div class="panel-title">
        <span>📝 1. Write Python Code</span>
        <select id="exampleSelect" onchange="loadExample()" style="background:#0b1120;color:#94a3b8;border:1px solid #475569;border-radius:4px;padding:4px 8px;font-size:12px;">
          <option value="ex1">Example 1: Basic Variables & Addition</option>
          <option value="ex2">Example 2: For Loop & Sum</option>
          <option value="ex3">Example 3: If-Else Condition</option>
          <option value="ex4">Example 4: Function Call (Energy Calculation)</option>
        </select>
      </div>
      <textarea id="codeEditor"># Student Code Example
x = 5
y = 10
total = x + y
total = total * 2
print("Final Total is:", total)</textarea>
      <div class="btn-row">
        <button class="btn-primary" onclick="startVisualization()">🚀 Start Visualizer</button>
        <button class="btn-secondary" onclick="resetVisualizer()">↺ Reset</button>
      </div>
      
      <div class="panel-title" style="margin-top:20px;">💻 Console Output (print)</div>
      <div class="terminal-out" id="termOutput">(Output will appear here)</div>
    </div>

    <!-- Right: Visualizer & Memory -->
    <div class="panel">
      <div class="panel-title">
        <span>👀 2. Live Execution Stepper</span>
        <span class="step-counter" id="stepIndicator">Step: 0 / 0</span>
      </div>

      <!-- Live Code Window -->
      <div class="code-view" id="codeViewer">
        <div style="color:#64748b;padding:20px;text-align:center;">Click "Start Visualizer" to trace code.</div>
      </div>

      <!-- Controls -->
      <div class="btn-row" style="margin-top:14px;">
        <button class="btn-step" id="prevBtn" onclick="prevStep()" disabled>◀ Prev Step</button>
        <button class="btn-step" id="nextBtn" onclick="nextStep()" disabled>Next Step ▶</button>
      </div>

      <!-- Live Variables Table -->
      <div class="panel-title" style="margin-top:20px;">📦 Computer Memory (Variables)</div>
      <table class="var-table">
        <thead>
          <tr>
            <th>Variable Name</th>
            <th>Type</th>
            <th>Current Value</th>
          </tr>
        </thead>
        <tbody id="varBody">
          <tr><td colspan="3" style="color:#64748b;text-align:center;">No variables active yet</td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <script>
    const EXAMPLES = {
      ex1: `# Basic Arithmetic\\nx = 5\\ny = 10\\ntotal = x + y\\ntotal = total * 2\\nprint("Final Total is:", total)`,
      ex2: `# Loop Example\\nsum_val = 0\\nfor i in [1, 2, 3, 4]:\\n    sum_val = sum_val + i\\n    print("i is", i, "running sum is", sum_val)`,
      ex3: `# If-Else Decision\\nenergy = -4.5\\nif energy < -3.0:\\n    status = "Strong Adsorption"\\nelse:\\n    status = "Weak Adsorption"\\nprint("Status is:", status)`,
      ex4: `# Function Call Example\\ndef calc_cdd(tot, slab, mol):\\n    diff = tot - (slab + mol)\\n    return diff\\n\\ne_tot = -312048.8\\ne_slab = -309116.6\\ne_mol = -2927.7\\nads_energy = calc_cdd(e_tot, e_slab, e_mol)\\nprint("Adsorption energy:", ads_energy)`
    };

    function loadExample() {
      const val = document.getElementById("exampleSelect").value;
      document.getElementById("codeEditor").value = EXAMPLES[val];
      resetVisualizer();
    }

    let traceSteps = [];
    let currentStepIdx = 0;
    let codeLines = [];

    async function startVisualization() {
      const code = document.getElementById("codeEditor").value;
      document.getElementById("termOutput").innerText = "Executing & tracing...";
      
      const res = await fetch("/api/trace", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code })
      });
      const data = await res.json();

      if (data.error) {
        document.getElementById("termOutput").innerText = "Error: " + data.error;
        return;
      }

      traceSteps = data.steps;
      codeLines = data.code_lines;
      currentStepIdx = 0;
      
      renderCodeView();
      renderStep(currentStepIdx);
      
      document.getElementById("nextBtn").disabled = traceSteps.length <= 1;
      document.getElementById("prevBtn").disabled = true;
    }

    function renderCodeView() {
      const viewer = document.getElementById("codeViewer");
      viewer.innerHTML = "";
      codeLines.forEach((text, i) => {
        const lineNo = i + 1;
        const div = document.createElement("div");
        div.className = "code-line";
        div.id = `line-${lineNo}`;
        div.innerHTML = `<span class="line-no">${lineNo}</span><span class="line-text">${escapeHtml(text)}</span>`;
        viewer.appendChild(div);
      });
    }

    function renderStep(idx) {
      if (!traceSteps || traceSteps.length === 0) return;
      const step = traceSteps[idx];

      // Update indicator
      document.getElementById("stepIndicator").innerText = `Step: ${idx + 1} / ${traceSteps.length}`;

      // Update Highlighted line
      document.querySelectorAll(".code-line").forEach(el => el.classList.remove("active-line"));
      const lineEl = document.getElementById(`line-${step.line}`);
      if (lineEl) {
        lineEl.classList.add("active-line");
        lineEl.scrollIntoView({ block: "nearest", behavior: "smooth" });
      }

      // Update Variables Table
      const varBody = document.getElementById("varBody");
      varBody.innerHTML = "";
      const vars = step.vars || {};
      const keys = Object.keys(vars);

      if (keys.length === 0) {
        varBody.innerHTML = `<tr><td colspan="3" style="color:#64748b;text-align:center;">No variables created yet</td></tr>`;
      } else {
        keys.forEach(k => {
          const item = vars[k];
          const tr = document.createElement("tr");
          tr.innerHTML = `
            <td style="color:#38bdf8;">${k}</td>
            <td style="color:#94a3b8;">${item.type}</td>
            <td class="var-changed">${escapeHtml(String(item.val))}</td>
          `;
          varBody.appendChild(tr);
        });
      }

      // Output update
      document.getElementById("termOutput").innerText = step.stdout || "(No output yet)";
    }

    function nextStep() {
      if (currentStepIdx < traceSteps.length - 1) {
        currentStepIdx++;
        renderStep(currentStepIdx);
      }
      document.getElementById("prevBtn").disabled = (currentStepIdx === 0);
      document.getElementById("nextBtn").disabled = (currentStepIdx === traceSteps.length - 1);
    }

    function prevStep() {
      if (currentStepIdx > 0) {
        currentStepIdx--;
        renderStep(currentStepIdx);
      }
      document.getElementById("prevBtn").disabled = (currentStepIdx === 0);
      document.getElementById("nextBtn").disabled = (currentStepIdx === traceSteps.length - 1);
    }

    function resetVisualizer() {
      traceSteps = [];
      currentStepIdx = 0;
      document.getElementById("codeViewer").innerHTML = '<div style="color:#64748b;padding:20px;text-align:center;">Click "Start Visualizer" to trace code.</div>';
      document.getElementById("varBody").innerHTML = '<tr><td colspan="3" style="color:#64748b;text-align:center;">No variables active yet</td></tr>';
      document.getElementById("stepIndicator").innerText = "Step: 0 / 0";
      document.getElementById("termOutput").innerText = "(Output will appear here)";
      document.getElementById("nextBtn").disabled = true;
      document.getElementById("prevBtn").disabled = true;
    }

    function escapeHtml(text) {
      return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    }
  </script>
</body>
</html>
"""

def execute_trace(code_str):
    """Executes Python code and records line numbers, stdout, and local variables at each step."""
    steps = []
    lines = code_str.splitlines()

    # Capture stdout
    old_stdout = sys.stdout
    captured_out = io.StringIO()
    sys.stdout = captured_out

    def tracer(frame, event, arg):
        if event == 'line' and frame.f_code.co_filename == '<student_code>':
            line_no = frame.f_lineno
            # Filter user variables
            user_vars = {}
            for k, v in frame.f_locals.items():
                if not k.startswith("__"):
                    val_str = repr(v)
                    if len(val_str) > 50:
                        val_str = val_str[:47] + "..."
                    user_vars[k] = {"val": val_str, "type": type(v).__name__}
            
            steps.append({
                "line": line_no,
                "vars": user_vars,
                "stdout": captured_out.getvalue()
            })
        return tracer

    try:
        compiled = compile(code_str, '<student_code>', 'exec')
        sys.settrace(tracer)
        exec(compiled, {})
    except Exception as e:
        sys.settrace(None)
        sys.stdout = old_stdout
        return {"error": str(e), "code_lines": lines, "steps": []}
    finally:
        sys.settrace(None)
        sys.stdout = old_stdout

    # Add final end step
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


class VisualizerHandler(SimpleHTTPRequestHandler):
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
    server = HTTPServer(("0.0.0.0", PORT), VisualizerHandler)
    print(f"============================================================")
    print(f"🎓 Python Beginner Code Visualizer GUI is RUNNING!")
    print(f"👉 Open in your browser: http://localhost:{PORT}")
    print(f"============================================================")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Visualizer Server.")
