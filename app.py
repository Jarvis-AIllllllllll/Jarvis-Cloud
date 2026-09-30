import os
import requests
import json
from flask import Flask, render_template_string, request, jsonify
from datetime import datetime

app = Flask(__name__)

# API Key from Render Environment
api_key = os.environ.get("GROQ_API_KEY")

def get_hud_design():
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>KINGS CLIENT AI | OMNI-ELITE HUD</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;500;700&family=Fira+Code:wght@300;500&display=swap');
        
        :root { 
            --neon: #00f2ff; 
            --gold: #ffcc00; 
            --bg: #020617; 
            --panel: rgba(0, 10, 30, 0.6); 
            --border: rgba(0, 242, 255, 0.3); 
            --shadow: rgba(0, 0, 0, 0.8);
        }

        body, html { 
            margin: 0; padding: 0; width: 100%; height: 100%; 
            background-color: var(--bg); color: var(--neon); 
            font-family: 'Rajdhani', sans-serif; overflow: hidden;
        }

        /* --- THE QUANTUM VOID BACKGROUND --- */
        #canvas-container {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            z-index: -1; background: radial-gradient(circle at center, #0a1a30 0%, #01050a 100%);
        }
        canvas { position: absolute; top: 0; left: 0; width: 100%; height: 100%; }

        .dashboard { 
            display: grid; 
            grid-template-columns: 300px 1fr; 
            grid-template-rows: 70px 1fr 120px; 
            height: 100vh; width: 100vw; 
            box-sizing: border-box;
            position: relative;
            z-index: 10;
        }

        /* GLASS SIDEBAR */
        .sidebar { 
            background: rgba(0, 5, 15, 0.7); 
            border-right: 1px solid var(--border); 
            display: flex; flex-direction: column; 
            padding: 30px 0; backdrop-filter: blur(30px);
            box-shadow: 10px 0 50px var(--shadow);
        }
        .logo { 
            font-family: 'Orbitron', sans-serif; font-size: 24px; font-weight: bold; 
            text-align: center; margin-bottom: 50px; letter-spacing: 6px; color: white; 
            text-shadow: 0 0 20px var(--neon); border-bottom: 1px solid var(--border);
            padding-bottom: 20px; margin-left: 20px; margin-right: 20px;
        }
        .nav-item { 
            padding: 18px 30px; font-size: 13px; cursor: pointer; 
            transition: 0.4s; border-left: 4px solid transparent; 
            color: rgba(0, 242, 255, 0.5); text-transform: uppercase; 
            letter-spacing: 2px;
        }
        .nav-item:hover, .nav-item.active { 
            background: rgba(0, 212, 255, 0.1); color: white; 
            border-left: 4px solid var(--gold); 
            text-shadow: 0 0 15px var(--gold);
            transform: translateX(10px);
        }

        /* TOP BAR */
        .top-bar { 
            grid-column: 2 / 3; display: flex; justify-content: space-between; 
            align-items: center; padding: 0 40px; background: var(--panel); 
            border-bottom: 1px solid var(--border); backdrop-filter: blur(20px); 
            font-size: 14px; font-family: 'Orbitron', sans-serif;
        }

        /* CONTENT GRID */
        .content { 
            grid-column: 2 / 3; display: grid; 
            grid-template-columns: 320px 1fr 320px; 
            grid-template-rows: 1fr 220px; 
            gap: 25px; padding: 25px; 
            box-sizing: border-box;
        }

        .panel { 
            background: var(--panel); border: 1px solid var(--border); 
            border-radius: 25px; padding: 25px; 
            backdrop-filter: blur(30px); position: relative; 
            box-shadow: inset 0 0 25px rgba(0, 242, 255, 0.1), 0 10px 30px rgba(0,0,0,0.5);
            transition: 0.3s;
        }
        .panel:hover { border-color: var(--gold); box-shadow: 0 0 20px rgba(255, 204, 0, 0.2); }
        .panel-title { 
            font-family: 'Orbitron', sans-serif; font-size: 12px; 
            text-transform: uppercase; margin-bottom: 20px; 
            border-bottom: 1px solid var(--border); padding-bottom: 10px; 
            display: flex; justify-content: space-between; color: white; 
        }

        /* THE EVENT HORIZON CORE */
        .center-area { display: flex; justify-content: center; align-items: center; position: relative; }
        .ring { position: absolute; border-radius: 50%; border: 2px solid transparent; animation: spin linear infinite; }
        .r1 { width: 420px; height: 420px; border-top: 2px solid var(--neon); animation-duration: 15s; opacity: 0.2; }
        .r2 { width: 340px; height: 340px; border-bottom: 2px solid var(--gold); animation-duration: 10s; opacity: 0.4; animation-direction: reverse; }
        .r3 { width: 260px; height: 260px; border-left: 2px solid var(--neon); animation-duration: 5s; opacity: 0.6; }
        @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
        .core-center { 
            width: 130px; height: 130px; 
            background: radial-gradient(circle, #fff 0%, var(--neon) 30%, transparent 70%); 
            border-radius: 50%; box-shadow: 0 0 80px var(--neon), 0 0 30px var(--gold); 
            animation: pulse 3s infinite ease-in-out; z-index: 10; 
        }
        @keyframes pulse { 0%, 100% { transform: scale(1); opacity: 0.8; } 50% { transform: scale(1.15); opacity: 1; } }

        /* GAUGE SYSTEM */
        .monitor-row { display: flex; justify-content: space-around; text-align: center; margin-top: 15px; }
        .gauge-container { position: relative; width: 80px; height: 80px; }
        .gauge-svg { transform: rotate(-90deg); width: 80px; height: 80px; }
        .gauge-bg { fill: none; stroke: var(--neon-dark); stroke-width: 6; }
        .gauge-fill { fill: none; stroke: var(--gold); stroke-width: 6; stroke-dasharray: 220; transition: stroke-dashoffset 1s; }
        .gauge-text { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-weight: bold; color: white; }

        /* CHAT AREA */
        #chat-box { height: 140px; overflow-y: auto; display: flex; flex-direction: column; gap: 15px; font-size: 14px; }
        .msg { padding: 12px 18px; border-radius: 15px; max-width: 85%; animation: slideUp 0.4s ease; }
        @keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        .user-msg { align-self: flex-end; background: var(--neon-dark); color: white; border-bottom-right-radius: 2px; border-right: 3px solid var(--gold); }
        .ai-msg { align-self: flex-start; background: rgba(255, 255, 255, 0.07); color: var(--neon); border-bottom-left-radius: 2px; border-left: 3px solid var(--neon); }

        /* COMMAND CAPSULE */
        .bottom-bar { 
            grid-column: 2 / 3; background: rgba(0, 10, 20, 0.9); 
            border-top: 1px solid var(--border); display: flex; align-items: center; 
            padding: 0 40px; backdrop-filter: blur(30px); 
        }
        .input-container { flex: 1; position: relative; display: flex; align-items: center; margin: 0 30px; }
        .input-field { 
            width: 100%; background: rgba(0, 0, 0, 0.6); border: 1px solid var(--border); 
            padding: 20px 30px; color: white; outline: none; border-radius: 50px; 
            font-size: 16px; transition: 0.4s; box-shadow: inset 0 0 20px rgba(0, 242, 255, 0.1); 
        }
        .input-field:focus { border-color: var(--gold); box-shadow: 0 0 30px var(--gold); }
        .execute-btn { 
            background: var(--neon); border: none; padding: 20px 40px; 
            border-radius: 50px; font-weight: bold; cursor: pointer; 
            text-transform: uppercase; transition: 0.4s; 
        }
        .execute-btn:hover { background: white; transform: scale(1.1); box-shadow: 0 0 30px var(--neon); }

        /* GAMES */
        .game-btn { 
            display: block; width: 100%; padding: 12px; margin-bottom: 10px; 
            background: rgba(0, 242, 255, 0.05); border: 1px solid var(--border); 
            color: var(--neon); text-align: center; text-decoration: none; 
            border-radius: 10px; font-size: 12px; transition: 0.3s; 
        }
        .game-btn:hover { background: var(--gold); color: black; box-shadow: 0 0 15px var(--gold); }
    </style>
</head>
<body>
    <div id="bg-system"><canvas id="neural-canvas"></canvas></div>
    <div class="dashboard">
        <div class="sidebar">
            <div class="logo">KINGS CLIENT AI</div>
            <div class="nav-item active">COMMAND CENTER</div>
            <div class="nav-item" onclick="window.open('https://www.google.com', '_blank')">🌐 WEB LINK</div>
            <div class="nav-item" onclick="alert('Cloud restricted, Sir.')">📝 DATA LOG</div>
            <div class="nav-item" onclick="alert('Cloud restricted, Sir.')">🧮 ANALYSIS</div>
            <div class="nav-item" onclick="alert('Cloud restricted, Sir.')">⚙️ SYSTEM CORE</div>
            <div style="margin-top: auto; padding: 20px;">
                <div class="panel-title" style="border-bottom:1px solid var(--border); padding-bottom:5px; margin-bottom:10px;">S-CLASS HUB</div>
                <a href="https://poki.com" target="_blank" class="game-btn">POKI</a>
                <a href="https://crazygames.com" target="_blank" class="game-btn">CRAZYGAMES</a>
                <a href="https://unblockedgames.xyz" target="_blank" class="game-btn">UNBLOCKED X</a>
            </div>
        </div>
        <div class="top-bar">
            <div>SYSTEM STATUS: <span style="color: #0f0; text-shadow: 0 0 10px #0f0;">OMNI-ACTIVE</span></div>
            <div id="clock" style="font-weight: bold;">Loading...</div>
            <div>OPERATOR: <span style="color: white;">KINGS ADMIN</span></div>
        </div>
        <div class="content">
            <div class="panel">
                <div class="panel-title">S-CORE METRICS <span style="color:var(--gold)">ELITE</span></div>
                <div style="font-size: 13px; line-height: 2.5; color: rgba(0,242,255,0.8);">
                    LINK: <span style="color:white">STABLE</span><br>
                    SENSORS: <span style="color:white">SYNCED</span><br>
                    UPLINK: <span style="color:white">S-CLOUD</span><br>
                    S-STATUS: <span style="color:white">OPTIMAL</span>
                </div>
            </div>
            <div class="center-area">
                <div class="ring r1"></div><div class="ring r2"></div><div class="ring r3"></div>
                <div class="core-center" id="reactor"></div>
            </div>
            <div class="panel">
                <div class="panel-title">INTELLIGENCE FEED <span style="color:var(--accent)">LIVE</span></div>
                <div id="feed" style="font-size: 11px; color: rgba(0,242,255,0.6); line-height: 1.8;">
                    > Initializing Quantum Bridge...<br>
                    > Synchronizing Neural Nodes...<br>
                    > Welcome back, Sir.
                </div>
            </div>
            <div class="panel">
                <div class="panel-title">HARDWARE TELEMETRY</div>
                <div class="monitor-row">
                    <div class="gauge-container">
                        <svg class="gauge-svg"><circle class="gauge-bg" cx="40" cy="40" r="35"/><circle class="gauge-fill" id="cpu-gauge" cx="40" cy="40" r="35" stroke-dashoffset="100"/></svg>
                        <div class="gauge-text" id="cpu-text">0%</div>
                    </div>
                    <div class="gauge-container">
                        <svg class="gauge-svg"><circle class="gauge-bg" cx="40" cy="40" r="35"/><circle class="gauge-fill" id="ram-gauge" cx="40" cy="40" r="35" stroke-dashoffset="100"/></svg>
                        <div class="gauge-text" id="ram-text">0%</div>
                    </div>
                    <div class="gauge-container">
                        <svg class="gauge-svg"><circle class="gauge-bg" cx="40" cy="40" r="35"/><circle class="gauge-fill" id="disk-gauge" cx="40" cy="40" r="35" stroke-dashoffset="100"/></svg>
                        <div class="gauge-text" id="disk-text">0%</div>
                    </div>
                </div>
            </div>
            <div class="panel">
                <div class="panel-title">COMMS CHANNEL</div>
                <div id="chat-box">
                    <div class="msg ai-msg">Omni-Elite link active. I am awaiting your command, Sir.</div>
                </div>
            </div>
            <div class="panel">
                <div class="panel-title">NODE STATUS</div>
                <div style="font-size: 12px; line-height: 2; color: rgba(0,242,255,0.7);">
                    Mainframe: <span style="color:#0f0">ONLINE</span><br>
                    Security: <span style="color:#0f0">QUANTUM</span><br>
                    Link: <span style="color:#0f0">S-CLOUD</span>
                </div>
            </div>
            <div class="bottom-bar">
                <div style="font-family: 'Orbitron'; font-size: 13px; color: var(--neon);">COMMAND:</div>
                <div class="input-container">
                    <input type="text" id="user-input" class="input-field" placeholder="Awaiting your directive, Sir..." autocomplete="off">
                </div>
                <button class="execute-btn" onclick="sendMessage()">EXECUTE</button>
            </div>
        </div>
    </script>
    <script>
        const canvas = document.getElementById('neural-canvas');
        const ctx = canvas.getContext('2d');
        let w, h, particles = [];
        function init() {
            canvas.width = w = window.innerWidth;
            canvas.height = h = window.innerHeight;
            particles = [];
            for(let i=0; i<100; i++) particles.push({x: Math.random()*w, y: Math.random()*h, vx: (Math.random()-0.5)*0.5, vy: (Math.random()-0.5)*0.5});
        }
        function draw() {
            ctx.clearRect(0,0,w,h);
            ctx.fillStyle = 'rgba(0, 242, 255, 0.5)';
            ctx.strokeStyle = 'rgba(0, 242, 255, 0.1)';
            particles.forEach((p, i) => {
                p.x += p.vx; p.y += p.vy;
                if(p.x<0 || p.x>w) p.vx*=-1; if(p.y<0 || p.y>h) p.vy*=-1;
                ctx.beginPath(); ctx.arc(p.x, p.y, 1.5, 0, Math.PI*2); ctx.fill();
                for(let j=i+1; j<particles.length; j++) {
                    let p2 = particles[j]; let dist = Math.hypot(p.x-p2.x, p.y-p2.y);
                    if(dist < 150) { ctx.beginPath(); ctx.moveTo(p.x, p.y); ctx.lineTo(p2.x, p2.y); ctx.stroke(); }
                }
            });
            requestAnimationFrame(draw);
        }
        window.addEventListener('resize', init); init(); draw();
        function updateClock() { document.getElementById('clock').innerText = new Date().toLocaleTimeString(); }
        setInterval(updateClock, 1000); updateClock();
        function updateGauges() {
            const cpu = Math.floor(Math.random()*20+10); const ram = Math, ram = Math.floor(Math.random()*20+40); const disk = Math.floor(Math.random()*10+20);
            document.getElementById('cpu-text').innerText = cpu+"%"; document.getElementById('ram-text').innerText = ram+"%"; document.getElementById('disk-text').innerText = disk+"%";
            document.getElementById('cpu-gauge').style.strokeDashoffset = 220 - (220 * cpu/100);
            document.getElementById('ram-gauge').style.strokeDashoffset = 220 - (220 * ram/100);
            document.getElementById('disk-gauge').style.strokeDashoffset = 220 - (220 * disk/100);
        }
        setInterval(updateGauges, 2000); updateGauges();
        const inputField = document.getElementById('user-input');
        inputField.addEventListener("keypress", (e) => { if(e.key === "Enter") sendMessage(); });
        async function sendMessage() {
            const text = inputField.value; if (!text) return;
            const cb = document.getElementById('chat-box');
            cb.innerHTML += `<div class="msg user-msg">${text}</div>`;
            inputField.value = '';
            const aiDiv = document.createElement('div'); aiDiv.className = 'msg ai-msg'; aiDiv.innerText = 'Processing...';
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
    if not api_key:
        return jsonify({'response': "API Key missing from Render environment, Sir."}), 500
    try:
        user_message = request.json.get('message')
        now = datetime.now()
        system_prompt = f"You are Kings Client AI. Date: {now.strftime('%B %d, %Y')}. You are an elite, professional, and high-status AI assistant. Refer to the user as 'Sir'. Be concise and highly technical."
        
        # FINAL STABLE MODEL LIST
        models_to_try = ["llama-3.1-8b-instant", "llama-3.3-70b-versatile", "mixtral-8x7b-32768"]
        
        for model in models_to_try:
            try:
                current_client = Groq(api_key=api_key)
                chat_completion = current_client.chat.completions.create(
                    messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_message}],
                    model=model,
                )
                return jsonify({'response': chat_completion.choices[0].message.content})
            except:
                continue 
        
        return jsonify({'response': "System Error: All models unreachable, Sir."}), 500
    except Exception as e:
        return jsonify({'response': f"Critical System Error: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
