import os
from flask import Flask, render_template_string, request, jsonify
from groq import Groq # Replacing Ollama with Groq
from datetime import datetime

app = Flask(__name__)

# This gets your API key from the Render environment settings
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def get_hud_design():
    # (I'm using the same high-end HUD code you liked)
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>JARVIS | CLOUD COMMAND CENTER</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;500;700&family=Fira+Code:wght@300;500&display=swap');
        :root { --neon: #00f2ff; --neon-dark: #005f73; --bg: #010812; --panel: rgba(0, 15, 30, 0.7); --border: rgba(0, 242, 255, 0.3); }
        body, html { margin: 0; padding: 0; width: 100%; height: 100%; background-color: var(--bg); color: var(--neon); font-family: 'Rajdhani', sans-serif; overflow: hidden; }
        #bg-system { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; background: radial-gradient(circle at center, #0a203d 0%, #01050a 100%); overflow: hidden; }
        canvas#code-rain { position: absolute; top: 0; left: 0; width: 100%; height: 100%; opacity: 0.4; z-index: -2; }
        .dashboard { display: grid; grid-template-columns: 280px 1fr; grid-template-rows: 60px 1fr 120px; height: 100vh; width: 100vw; position: relative; }
        .sidebar { background: rgba(0, 5, 15, 0.9); border-right: 1px solid var(--border); display: flex; flex-direction: column; padding: 30px 0; backdrop-filter: blur(20px); z-index: 20; }
        .logo { font-family: 'Orbitron', sans-serif; font-size: 26px; font-weight: bold; text-align: center; margin-bottom: 40px; letter-spacing: 10px; color: white; text-shadow: 0 0 20px var(--neon); }
        .nav-item { padding: 15px 25px; font-size: 13px; cursor: pointer; transition: 0.3s; border-left: 4px solid transparent; color: rgba(0, 242, 255, 0.6); text-transform: uppercase; }
        .nav-item:hover { background: rgba(0, 212, 255, 0.1); color: white; border-left: 4px solid var(--neon); }
        .top-bar { grid-column: 2 / 3; display: flex; justify-content: space-between; align-items: center; padding: 0 30px; background: var(--panel); border-bottom: 1px solid var(--border); backdrop-filter: blur(10px); font-size: 13px; font-family: 'Orbitron', sans-serif; }
        .content { grid-column: 2 / 3; display: grid; grid-template-columns: 320px 1fr 320px; grid-template-rows: 1fr 220px; gap: 20px; padding: 20px; }
        .panel { background: var(--panel); border: 1px solid var(--border); border-radius: 20px; padding: 20px; backdrop-filter: blur(20px); position: relative; }
        .panel-title { font-family: 'Orbitron', sans-serif; font-size: 11px; text-transform: uppercase; margin-bottom: 15px; border-bottom: 1px solid var(--border); padding-bottom: 8px; display: flex; justify-content: space-between; color: white; }
        .center-area { display: flex; justify-content: center; align-items: center; position: relative; }
        .ring { position: absolute; border-radius: 50%; border: 2px solid transparent; animation: spin linear infinite; }
        .r1 { width: 400px; height: 400px; border-top: 2px solid var(--neon); animation-duration: 10s; opacity: 0.3; }
        .r2 { width: 320px; height: 320px; border-bottom: 2px solid var(--neon); animation-duration: 6s; opacity: 0.5; animation-direction: reverse; }
        .r3 { width: 240px; height: 240px; border-left: 2px solid var(--neon); animation-duration: 3s; opacity: 0.8; }
        @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
        .core-center { width: 120px; height: 120px; background: radial-gradient(circle, white 0%, var(--neon) 30%, transparent 70%); border-radius: 50%; box-shadow: 0 0 60px var(--neon); animation: pulse 2s infinite ease-in-out; z-index: 10; }
        @keyframes pulse { 0%, 100% { transform: scale(1); opacity: 0.8; } 50% { transform: scale(1.1); opacity: 1; } }
        #chat-box { height: 120px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; font-size: 13px; }
        .msg { padding: 8px 12px; border-radius: 8px; max-width: 80%; }
        .user-msg { align-self: flex-end; background: var(--neon-dark); color: white; border-right: 3px solid var(--neon); }
        .ai-msg { align-self: flex-start; background: rgba(255,255,255,0.05); border-left: 3px solid var(--neon); }
        .bottom-bar { grid-column: 1 / span 3; background: rgba(0, 10, 20, 0.9); border-top: 1px solid var(--border); display: flex; align-items: center; padding: 0 40px; backdrop-filter: blur(30px); }
        .input-container { flex: 1; position: relative; display: flex; align-items: center; margin: 0 30px; }
        .input-field { width: 100%; background: rgba(0, 0, 0, 0.6); border: 1px solid var(--border); padding: 18px 25px; color: white; outline: none; border-radius: 50px; font-size: 16px; transition: 0.4s; box-shadow: inset 0 0 15px rgba(0, 242, 255, 0.1); }
        .execute-btn { background: var(--neon); border: none; padding: 18px 35px; border-radius: 50px; font-weight: bold; cursor: pointer; text-transform: uppercase; transition: 0.3s; }
        .execute-btn:hover { background: white; transform: scale(1.05); box-shadow: 0 0 30px var(--neon); }
    </style>
</head>
<body>
    <div id="bg-system"><canvas id="code-rain"></canvas></div>
    <div class="dashboard">
        <div class="sidebar">
            <div class="logo">JARVIS</div>
            <div class="nav-item active">COMMAND CENTER</div>
            <div class="nav-item" onclick="runAction('browser')">🌐 WEB LINK</div>
            <div class="nav-item" onclick="runAction('notepad')">📝 DATA LOG</div>
            <div class="nav-item" onclick="runAction('calc')">🧮 ANALYSIS</div>
            <div class="nav-item" onclick="runAction('taskmgr')">⚙️ SYSTEM CORE</div>
        </div>
        <div class="top-bar">
            <div>S-STATUS: <span style="color: #0f0;">CLOUDSYNC ACTIVE</span></div>
            <div id="clock">Loading...</div>
            <div>USER: <span style="color: white;">S-CLASS ADMIN</span></div>
        </div>
        <div class="content">
            <div class="panel"><div class="panel-title">CORE METRICS</div><div style="font-size: 13px; line-height: 2.2;">UPLINK: <span style="color:white">S-CLOUD</span><br>LATENCY: <span style="color:white">2ms</span><br>SENSORS: <span style="color:white">SYNCED</span></div></div>
            <div class="center-area"><div class="ring r1"></div><div class="ring r2"></div><div class="ring r3"></div><div class="core-center" id="reactor"></div></div>
            <div class="panel"><div class="panel-title">SATELLITE FEED</div><div id="feed" style="font-size: 11px;">> Cloud link established...<br> > Monitoring...</div></div>
            <div class="panel"><div class="panel-title">HARDWARE</div><div style="text-align:center; font-size: 20px; font-weight: bold;">S-CLOUD</div></div>
            <div class="panel"><div class="panel-title">COMMS CHANNEL</div><div id="chat-box"><div class="msg ai-msg">Cloud link established. Awaiting directive, Sir.</div></div></div>
            <div class="panel"><div class="panel-title">S-NODE</div><div style="font-size: 12px;">Encryption: <span style="color:#0f0">S-CLASS</span></div></div>
            <div class="bottom-bar"><div style="font-family: 'Orbitron'; font-size: 13px; color: var(--neon);">COMMAND:</div><div class="input-container"><input type="text" id="user-input" class="input-field" placeholder="Awaiting your voice, Sir..." autocomplete="off"></div><button class="execute-btn" onclick="sendMessage()">EXECUTE</button></div>
        </div>
    </div>
    <script>
        const canvas = document.getElementById('code-rain');
        const ctx = canvas.getContext('2d');
        let w, h, cols;
        const chars = "01XyZ89ABCDEF<>/{}[]()$#@%";
        let drops = [];
        function init() { w = canvas.width = window.innerWidth; h = canvas.height = window.innerHeight; cols = Math.floor(w / 20); drops = []; for(let i=0; i<cols; i++) drops[i] = Math.random() * h; }
        function draw() { ctx.clearRect(0,0,w,h); ctx.fillStyle = "#00f2ff"; ctx.font = "14px monospace"; for(let i=0; i<drops.length; i++) { ctx.fillText(chars[Math.floor(Math.random()*chars.length)], i*20, drops[i]); if(drops[i] > h && Math.random() > 0.975) drops[i] = 0; drops[i] += 2; } }
        setInterval(draw, 50); window.addEventListener('resize', init); init();
        function updateClock() { document.getElementById('clock').innerText = new Date().toLocaleTimeString(); }
        setInterval(updateClock, 1000); updateClock();
        const inputField = document.getElementById('user-input');
        inputField.addEventListener("keypress", (e) => { if(e.key === "Enter") sendMessage(); });
        async function runAction(actionType) {
            const cb = document.getElementById('chat-box');
            cb.innerHTML += `<div class="msg ai-msg">Sir, in Cloud Mode, local system access is disabled for security.</div>`;
            cb.scrollTop = cb.scrollHeight;
        }
        async function sendMessage() {
            const text = inputField.value; if (!text) return;
            const cb = document.getElementById('chat-box');
            cb.innerHTML += `<div class="msg user-msg">${text}</div>`;
            inputField.value = '';
            const aiDiv = document.createElement('div'); aiDiv.className = 'msg ai-msg'; aiDiv.innerText = 'Thinking...';
            cb.appendChild(aiDiv);
            try {
                const response = await fetch('/ask', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({message: text}) });
                const data = await response.json(); aiDiv.innerText = data.response;
            } catch (e) { aiDiv.innerText = "Critical Error, Sir."; }
            cb.scrollTop = cb.scrollHeight;
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(get_hud_design())

@app.route('/action', methods=['POST'])
def action():
    return jsonify({'status': 'Cloud Mode: Local OS access restricted, Sir.'})

@app.route('/ask', methods=['POST'])
def ask():
    try:
        user_message = request.json.get('message')
        now = datetime.now()
        system_prompt = f"You are JARVIS. Date: {now.strftime('%B %d, %Y')}. Be professional and loyal. Refer to the user as 'Sir'."
        
        # Using Groq API instead of Ollama
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            model="llama3-8b-8192",
        )
        return jsonify({'response': chat_completion.choices[0].message.content})
    except Exception as e:
        return jsonify({'response': f"System Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
