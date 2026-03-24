import os, io, requests, sys, traceback
from flask import Flask, request, render_template_string, send_file, redirect, session
from PIL import Image, ImageOps, ImageDraw, ImageFont

app = Flask(__name__)
app.secret_key = "faisal_super_secret_key_99"

# --- MASTER CONFIG ---
config = {
    "site_name": "Faisal Ali AI Master Studio",
    "theme_color": "#1a73e8",
    "world_live": False,
    "admin_pass": "Faisal@1234", # Hard Password as requested
    "announcement": "System Online - Faisal Ali",
    "custom_css": ""
}

REMOVE_BG_KEY = "q9kbXX1nZpBXeekxQQAxNngT"

# --- HTML TEMPLATE (Full Features Restored) ---
BASE_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>{{ cfg.site_name }}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        :root { --p-color: {{ cfg.theme_color }}; }
        body { font-family: 'Poppins', sans-serif; background: #f0f2f5; margin: 0; padding: 10px; }
        .card { max-width: 600px; margin: auto; background: white; padding: 20px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); }
        .btn { background: var(--p-color); color: white; border: none; padding: 15px; width: 100%; border-radius: 10px; cursor: pointer; font-weight: bold; font-size: 16px; transition: 0.3s; }
        .btn:hover { opacity: 0.9; transform: scale(0.98); }
        input, select { width: 100%; padding: 12px; margin: 8px 0; border: 1px solid #ddd; border-radius: 8px; box-sizing: border-box; }
        .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
        {{ cfg.custom_css | safe }}
    </style>
</head>
<body>
    <div class="card">
        {% if not cfg.world_live and not session.get('is_admin') %}
            <div style="text-align:center; padding:40px;">
                <h1 style="font-size:50px;">🚧</h1>
                <h2>Under Maintenance</h2>
                <p>Faisal bhai is adding new AI Features. Stay tuned!</p>
            </div>
        {% else %}
            <h2 style="text-align:center; color: var(--p-color);">{{ cfg.site_name }}</h2>
            <p style="text-align:center; color: #666; font-size:13px;">{{ cfg.announcement }}</p>

            <form action="/process" method="POST" enctype="multipart/form-data">
                <label><b>1. Select Image:</b></label>
                <input type="file" name="image" required>

                <label><b>2. AI Background & Color:</b></label>
                <div class="grid-2">
                    <select name="bg_mode">
                        <option value="original">Original BG</option>
                        <option value="remove">Remove BG (AI)</option>
                        <option value="custom_color">Custom Solid Color</option>
                    </select>
                    <input type="color" name="bg_color" value="#ffffff">
                </div>

                <label><b>3. Custom Size (mm):</b></label>
                <div class="grid-2">
                    <input type="number" name="w_mm" placeholder="Width (e.g. 35)" value="35">
                    <input type="number" name="h_mm" placeholder="Height (e.g. 45)" value="45">
                </div>

                <label><b>4. Layout & Quantity:</b></label>
                <select name="paper">
                    <option value="A4">A4 Sheet (Full)</option>
                    <option value="4x6">4x6 Photo Paper</option>
                </select>
                <input type="number" name="qty" value="30" min="1" max="100">

                <button type="submit" class="btn">✨ Generate Master Print</button>
            </form>
        {% endif %}
    </div>
    
    <div style="text-align:center; margin-top:20px;">
        <a href="/admin" style="color:#eee; text-decoration:none; font-size:10px;">.</a>
    </div>
</body>
</html>
'''

ADMIN_HTML = '''
<!DOCTYPE html>
<html>
<head><title>Faisal's Secret Lab</title></head>
<body style="background:#0d1117; color:#c9d1d9; font-family:monospace; padding:20px;">
    <h1 style="color:#58a6ff;">🛠️ Master Admin Portal</h1>
    <hr border="1" color="#30363d">
    
    <form method="POST">
        <h3>1. Global Settings</h3>
        Site Name: <input type="text" name="site_name" value="{{ cfg.site_name }}" style="width:100%;"><br><br>
        Theme Color: <input type="color" name="theme_color" value="{{ cfg.theme_color }}"><br><br>
        
        World Host Status: 
        <select name="world_live">
            <option value="True" {% if cfg.world_live %}selected{% endif %}>🌍 LIVE (Public)</option>
            <option value="False" {% if not cfg.world_live %}selected{% endif %}>🔒 PRIVATE (Faisal Only)</option>
        </select><br><br>

        <h3>2. Advanced Python Code Injector</h3>
        <p style="color:orange;">Warning: Enter raw Python code to execute on server.</p>
        <textarea name="python_code" style="width:100%; height:150px; background:#000; color:#0f0; border:1px solid #333;" placeholder="print('New Logic Added')"></textarea><br><br>

        <button type="submit" style="background:#238636; color:white; padding:15px; border:none; width:100%; cursor:pointer; font-weight:bold;">💾 SAVE & SYNC TO WORLD</button>
    </form>
    <br>
    <div style="border:1px solid #333; padding:10px;">
        <a href="/" style="color:#58a6ff;">Return to Studio</a> | <a href="/logout" style="color:red;">Secure Logout</a>
    </div>
</body>
</html>
'''

# --- ROUTES ---

@app.route("/")
def index():
    return render_template_string(BASE_HTML, cfg=config)

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        if not session.get('is_admin'):
            if request.form.get("password") == config["admin_pass"]:
                session['is_admin'] = True
                return redirect("/admin")
            else: return "Access Denied!"
        
        # Update Settings
        config["site_name"] = request.form.get("site_name")
        config["theme_color"] = request.form.get("theme_color")
        config["world_live"] = request.form.get("world_live") == "True"
        
        # Code Injector Logic
        injected_code = request.form.get("python_code")
        if injected_code:
            try:
                exec(injected_code) # Executes your custom code!
            except Exception as e:
                return f"Code Error: {str(e)}"

        return redirect("/admin")

    if not session.get('is_admin'):
        return '''<body style="background:black; color:green; text-align:center; padding-top:100px; font-family:monospace;">
                  <h2>IDENTITY VERIFICATION REQUIRED</h2>
                  <form method="POST"><input type="password" name="password" placeholder="Passkey" style="padding:10px;"><button type="submit">Unlock</button></form></body>'''
    
    return render_template_string(ADMIN_HTML, cfg=config)

@app.route("/process", methods=["POST"])
def process():
    try:
        file = request.files['image']
        bg_mode = request.form.get('bg_mode')
        bg_color = request.form.get('bg_color')
        w_mm = int(request.form.get('w_mm', 35))
        h_mm = int(request.form.get('h_mm', 45))
        qty = int(request.form.get('qty', 30))
        
        img = Image.open(file).convert("RGB")
        
        # 1. AI Background Logic
        if bg_mode == "remove" or bg_mode == "custom_color":
            res = requests.post("https://api.remove.bg/v1.0/removebg",
                files={'image_file': file.read()}, data={'size': 'auto'},
                headers={'X-Api-Key': REMOVE_BG_KEY})
            if res.status_code == 200:
                face = Image.open(io.BytesIO(res.content)).convert("RGBA")
                hex_color = bg_color.lstrip('#')
                rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
                canvas = Image.new("RGBA", face.size, rgb + (255,))
                canvas.paste(face, (0,0), face)
                img = canvas.convert("RGB")

        # 2. Resizing & Border (300 DPI calculation)
        w_px = int(w_mm * 11.81)
        h_px = int(h_mm * 11.81)
        photo = img.resize((w_px, h_px), Image.LANCZOS)
        photo = ImageOps.expand(photo, border=2, fill="black")

        # 3. Sheet Creation (A4 default)
        sheet = Image.new("RGB", (2480, 3508), "white")
        x, y = 100, 100
        for _ in range(qty):
            if x + w_px + 50 > 2380: x = 100; y += h_px + 50
            if y + h_px + 50 > 3400: break
            sheet.paste(photo, (x, y))
            x += w_px + 50

        pdf_out = io.BytesIO()
        sheet.save(pdf_out, format="PDF")
        pdf_out.seek(0)
        return send_file(pdf_out, mimetype="application/pdf", as_attachment=True, download_name="faisal_master_print.pdf")

    except Exception as e:
        return f"System Error: {str(e)}"

@app.route("/logout")
def logout():
    session.pop('is_admin', None)
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
