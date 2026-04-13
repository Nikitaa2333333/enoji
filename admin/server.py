#!/usr/bin/env python3
"""
Локальный сервер для админки Emoji Tours.
Запуск:  python admin/server.py
Открыть: http://localhost:5001
"""

import json, os, re, mimetypes, secrets
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE = os.path.join(ROOT, 'js', 'site-config.js')
PASSWORD = 'emoji2026'
PORT = 5001

# Active sessions: token -> True
SESSIONS = {}

# ── Config helpers ────────────────────────────────────────────────────────────

def read_config():
    if not os.path.exists(CONFIG_FILE):
        return {}
    src = open(CONFIG_FILE, encoding='utf-8').read()
    m = re.search(r'window\.SITE_CONFIG\s*=\s*(\{.*\});', src, re.S)
    if m:
        return json.loads(m.group(1))
    return {}

def write_config(data):
    js = 'window.SITE_CONFIG = ' + json.dumps(data, ensure_ascii=False, indent=2) + ';\n'
    open(CONFIG_FILE, 'w', encoding='utf-8').write(js)

# ── Admin HTML ────────────────────────────────────────────────────────────────

def admin_html(cfg, error='', success=''):
    t = cfg.get('testimonials', [])
    t_json = json.dumps(t, ensure_ascii=False)

    def v(*keys):
        val = cfg
        for k in keys:
            val = val.get(k, '') if isinstance(val, dict) else ''
        return str(val).replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')

    return f'''<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Админка — Emoji Tours</title>
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:system-ui,-apple-system,sans-serif;background:#f5f5f5;color:#111;min-height:100vh}}
.page{{max-width:860px;margin:0 auto;padding:40px 20px 80px}}
header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:32px}}
header h1{{font-size:1.4rem;font-weight:700}}
.card{{background:#fff;border-radius:16px;padding:28px 32px;margin-bottom:24px;box-shadow:0 1px 4px rgba(0,0,0,.08)}}
.card h2{{font-size:.75rem;font-weight:700;margin-bottom:20px;color:#333;letter-spacing:.02em;text-transform:uppercase}}
.fields{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}
.field{{display:flex;flex-direction:column;gap:6px}}
.field.full{{grid-column:1/-1}}
label{{font-size:.8rem;font-weight:600;color:#555}}
input[type=text],input[type=email],input[type=url],input[type=password],textarea{{border:1.5px solid #e0e0e0;border-radius:10px;padding:10px 14px;font-size:.95rem;font-family:inherit;width:100%;transition:border-color .15s}}
input:focus,textarea:focus{{outline:none;border-color:#f4a300}}
textarea{{resize:vertical;min-height:90px}}
.testimonials-list{{display:flex;flex-direction:column;gap:16px}}
.testimonial-item{{border:1.5px solid #e8e8e8;border-radius:12px;padding:16px 18px;position:relative;background:#fafafa}}
.t-row{{display:grid;grid-template-columns:80px 1fr 1fr 130px;gap:10px;margin-bottom:10px;align-items:end}}
.btn-remove{{position:absolute;top:12px;right:14px;background:none;border:none;cursor:pointer;font-size:1.1rem;color:#ccc;padding:2px 6px;border-radius:6px}}
.btn-remove:hover{{background:#fee2e2;color:#dc2626}}
.btn-add{{display:inline-flex;align-items:center;gap:6px;padding:10px 18px;border-radius:10px;border:1.5px dashed #ccc;background:none;cursor:pointer;font-size:.9rem;color:#666;font-family:inherit;transition:border-color .15s,color .15s}}
.btn-add:hover{{border-color:#f4a300;color:#f4a300}}
.style-select{{width:100%;border:1.5px solid #e0e0e0;border-radius:10px;padding:10px 14px;font-size:.9rem;font-family:inherit;background:#fff}}
.style-select:focus{{outline:none;border-color:#f4a300}}
.actions{{display:flex;gap:12px;align-items:center;margin-top:8px}}
.btn-save{{padding:13px 32px;background:#f4a300;color:#fff;font-weight:700;border:none;border-radius:12px;font-size:1rem;cursor:pointer;font-family:inherit;transition:background .15s}}
.btn-save:hover{{background:#d98f00}}
.btn-logout{{padding:8px 18px;background:none;border:1.5px solid #e0e0e0;border-radius:10px;font-size:.85rem;cursor:pointer;font-family:inherit;color:#666}}
.btn-logout:hover{{border-color:#999;color:#111}}
.alert{{padding:12px 18px;border-radius:10px;margin-bottom:20px;font-size:.9rem;font-weight:500}}
.alert-success{{background:#dcfce7;color:#166534}}
.alert-error{{background:#fee2e2;color:#991b1b}}
@media(max-width:600px){{.fields{{grid-template-columns:1fr}}.t-row{{grid-template-columns:1fr 1fr}}.t-row>*:last-child{{grid-column:1/-1}}}}
</style>
</head>
<body>
<div class="page">
  <header>
    <h1>🌍 Управление сайтом</h1>
    <form method="POST" action="/admin/logout" style="display:inline">
      <button class="btn-logout">Выйти</button>
    </form>
  </header>
  {'<div class="alert alert-error">' + error + '</div>' if error else ''}
  {'<div class="alert alert-success">' + success + '</div>' if success else ''}
  <form method="POST" action="/admin/save" id="main-form">
    <div class="card">
      <h2>Контакты</h2>
      <div class="fields">
        <div class="field">
          <label>Телефон</label>
          <input type="text" name="phone" value="{v('phone')}" placeholder="+7 000-000-00-00">
        </div>
        <div class="field">
          <label>Email</label>
          <input type="email" name="email" value="{v('email')}" placeholder="mail@example.com">
        </div>
      </div>
    </div>
    <div class="card">
      <h2>Социальные сети</h2>
      <div class="fields">
        <div class="field full">
          <label>Ссылка MAX</label>
          <input type="url" name="social_max" value="{v('social','max')}">
        </div>
        <div class="field full">
          <label>Ссылка VK</label>
          <input type="url" name="social_vk" value="{v('social','vk')}">
        </div>
      </div>
    </div>
    <div class="card">
      <h2>Юридические данные</h2>
      <div class="fields">
        <div class="field full">
          <label>ФИО предпринимателя</label>
          <input type="text" name="legal_name" value="{v('legal','name')}">
        </div>
        <div class="field">
          <label>ИНН</label>
          <input type="text" name="legal_inn" value="{v('legal','inn')}">
        </div>
        <div class="field">
          <label>ОГРН ИП</label>
          <input type="text" name="legal_ogrn" value="{v('legal','ogrn')}">
        </div>
      </div>
    </div>
    <div class="card">
      <h2>Отзывы</h2>
      <div class="testimonials-list" id="testimonials-list"></div>
      <br>
      <button type="button" class="btn-add" onclick="addTestimonial()">+ Добавить отзыв</button>
      <input type="hidden" name="testimonials_json" id="testimonials-json">
    </div>
    <div class="actions">
      <button type="submit" class="btn-save">Сохранить</button>
      <span style="font-size:.85rem;color:#888">Изменения сразу появятся на сайте</span>
    </div>
  </form>
</div>
<script>
var testimonials = {t_json};
function renderList() {{
  var list = document.getElementById('testimonials-list');
  list.innerHTML = '';
  testimonials.forEach(function(t, i) {{
    var div = document.createElement('div');
    div.className = 'testimonial-item';
    div.innerHTML =
      '<button type="button" class="btn-remove" onclick="removeTestimonial(' + i + ')" title="Удалить">✕</button>' +
      '<div class="t-row">' +
        field('Инициалы','text',t.initials||'','initials',i,'М') +
        field('Имя','text',t.name||'','name',i,'Иван И.') +
        field('Подпись','text',t.label||'','label',i,'Отдых в Таиланде') +
        '<div class="field"><label>Стиль</label>' +
        '<select class="style-select" data-i="'+i+'" data-f="style" onchange="updateField(this)">' +
        '<option value="filled"'+(t.style==='filled'?' selected':'')+'>Заливка (оранжевая)</option>' +
        '<option value="outlined"'+(t.style==='outlined'?' selected':'')+'>Контур (белая)</option>' +
        '</select></div>' +
      '</div>' +
      '<div class="t-text"><label>Текст отзыва</label>' +
      '<textarea rows="4" data-i="'+i+'" data-f="text" onchange="updateField(this)" oninput="updateField(this)">'+escHtml(t.text||'')+'</textarea>' +
      '</div>';
    list.appendChild(div);
  }});
  syncJson();
}}
function field(label,type,value,fname,idx,placeholder) {{
  return '<div class="field"><label>'+label+'</label>' +
    '<input type="'+type+'" value="'+escAttr(value)+'" placeholder="'+placeholder+'" ' +
    'data-i="'+idx+'" data-f="'+fname+'" oninput="updateField(this)"></div>';
}}
function escAttr(s) {{ return String(s).replace(/&/g,'&amp;').replace(/"/g,'&quot;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }}
function escHtml(s) {{ return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }}
function updateField(el) {{ testimonials[parseInt(el.dataset.i)][el.dataset.f] = el.value; syncJson(); }}
function removeTestimonial(i) {{ testimonials.splice(i,1); renderList(); }}
function addTestimonial() {{
  testimonials.push({{initials:'',name:'',label:'',style:'outlined',text:''}});
  renderList();
  var items = document.querySelectorAll('.testimonial-item');
  if(items.length) items[items.length-1].scrollIntoView({{behavior:'smooth',block:'center'}});
}}
function syncJson() {{ document.getElementById('testimonials-json').value = JSON.stringify(testimonials); }}
document.getElementById('main-form').addEventListener('submit', syncJson);
renderList();
</script>
</body></html>'''


LOGIN_HTML = '''<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Войти — Emoji Tours</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{font-family:system-ui,-apple-system,sans-serif;background:#f5f5f5;display:flex;justify-content:center;padding-top:80px}
.card{background:#fff;border-radius:20px;padding:40px;width:100%;max-width:360px;box-shadow:0 4px 20px rgba(0,0,0,.1)}
h1{font-size:1.3rem;font-weight:800;margin-bottom:8px}
p{color:#666;font-size:.9rem;margin-bottom:28px}
label{display:block;font-size:.8rem;font-weight:600;color:#555;margin-bottom:6px}
input{width:100%;border:1.5px solid #e0e0e0;border-radius:10px;padding:10px 14px;font-size:.95rem;font-family:inherit;margin-bottom:16px}
input:focus{outline:none;border-color:#f4a300}
button{width:100%;padding:13px;background:#f4a300;color:#fff;font-weight:700;border:none;border-radius:12px;font-size:1rem;cursor:pointer;font-family:inherit}
button:hover{background:#d98f00}
.err{background:#fee2e2;color:#991b1b;padding:10px 14px;border-radius:10px;font-size:.9rem;margin-bottom:16px}
</style>
</head>
<body>
<div class="card">
  <h1>🌍 Emoji Tours</h1>
  <p>Введите пароль для входа в админку.</p>
  {error_block}
  <form method="POST" action="/admin/login">
    <label for="pw">Пароль</label>
    <input type="password" id="pw" name="password" autofocus placeholder="••••••••">
    <button type="submit">Войти</button>
  </form>
</div>
</body></html>'''

# ── Request handler ───────────────────────────────────────────────────────────

class Handler(BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        print(fmt % args)

    # ── Cookie helpers ──

    def get_session(self):
        cookies = self.headers.get('Cookie', '')
        for part in cookies.split(';'):
            part = part.strip()
            if part.startswith('session='):
                token = part[8:]
                if token in SESSIONS:
                    return token
        return None

    def set_session(self, token):
        self.send_header('Set-Cookie', f'session={token}; Path=/; HttpOnly')

    def clear_session(self):
        self.send_header('Set-Cookie', 'session=; Path=/; Max-Age=0')

    # ── Response helpers ──

    def send_html(self, html, code=200, extra_headers=None):
        body = html.encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        if extra_headers:
            for k, v in extra_headers.items():
                self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def redirect(self, location):
        self.send_response(302)
        self.send_header('Location', location)
        self.end_headers()

    def read_body(self):
        length = int(self.headers.get('Content-Length', 0))
        return self.rfile.read(length).decode('utf-8') if length else ''

    def parse_form(self):
        body = self.read_body()
        result = {}
        for pair in body.split('&'):
            if '=' in pair:
                k, _, v = pair.partition('=')
                from urllib.parse import unquote_plus
                result[unquote_plus(k)] = unquote_plus(v)
        return result

    # ── Routes ──

    def do_GET(self):
        path = urlparse(self.path).path.rstrip('/')

        if path in ('/admin', '/admin/'):
            path = '/admin'

        if path == '/admin':
            if not self.get_session():
                self.send_html(LOGIN_HTML.replace('{error_block}', ''))
            else:
                cfg = read_config()
                self.send_html(admin_html(cfg))
            return

        # Static files
        file_path = os.path.join(ROOT, self.path.lstrip('/').split('?')[0])
        # Prevent directory traversal
        if not os.path.abspath(file_path).startswith(os.path.abspath(ROOT)):
            self.send_response(403); self.end_headers(); return

        if os.path.isdir(file_path):
            file_path = os.path.join(file_path, 'index.html')

        if os.path.isfile(file_path):
            mime, _ = mimetypes.guess_type(file_path)
            data = open(file_path, 'rb').read()
            self.send_response(200)
            self.send_header('Content-Type', mime or 'application/octet-stream')
            self.send_header('Content-Length', str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not found')

    def do_POST(self):
        path = urlparse(self.path).path

        if path == '/admin/login':
            form = self.parse_form()
            if form.get('password') == PASSWORD:
                token = secrets.token_hex(16)
                SESSIONS[token] = True
                self.send_response(302)
                self.set_session(token)
                self.send_header('Location', '/admin')
                self.end_headers()
            else:
                err = '<div class="err">Неверный пароль</div>'
                self.send_html(LOGIN_HTML.replace('{error_block}', err))
            return

        if path == '/admin/logout':
            token = self.get_session()
            if token:
                SESSIONS.pop(token, None)
            self.send_response(302)
            self.clear_session()
            self.send_header('Location', '/admin')
            self.end_headers()
            return

        if path == '/admin/save':
            if not self.get_session():
                self.redirect('/admin'); return
            form = self.parse_form()
            phone = form.get('phone', '').strip()
            phone_raw = re.sub(r'\D', '', phone)
            data = {
                'phone': phone,
                'phone_raw': phone_raw,
                'email': form.get('email', '').strip(),
                'social': {
                    'max': form.get('social_max', '').strip(),
                    'vk':  form.get('social_vk', '').strip(),
                },
                'legal': {
                    'name': form.get('legal_name', '').strip(),
                    'inn':  form.get('legal_inn', '').strip(),
                    'ogrn': form.get('legal_ogrn', '').strip(),
                },
                'testimonials': json.loads(form.get('testimonials_json', '[]') or '[]'),
            }
            try:
                write_config(data)
                cfg = read_config()
                self.send_html(admin_html(cfg, success='✓ Настройки сохранены!'))
            except Exception as e:
                cfg = read_config()
                self.send_html(admin_html(cfg, error=f'Ошибка записи: {e}'))
            return

        self.send_response(404); self.end_headers()


if __name__ == '__main__':
    server = HTTPServer(('127.0.0.1', PORT), Handler)
    print(f'Сервер запущен: http://localhost:{PORT}')
    print(f'Админка:        http://localhost:{PORT}/admin')
    print(f'Пароль:         {PASSWORD}')
    print('Нажми Ctrl+C для остановки.')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nОстановлен.')
