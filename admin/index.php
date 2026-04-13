<?php
session_start();

define('ADMIN_PASSWORD', 'emoji2026');
define('CONFIG_FILE', __DIR__ . '/../js/site-config.js');

$error = '';
$success = '';

// --- Actions ---
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $action = $_POST['action'] ?? '';

    if ($action === 'login') {
        if ($_POST['password'] === ADMIN_PASSWORD) {
            $_SESSION['admin'] = true;
        } else {
            $error = 'Неверный пароль';
        }
    }

    if ($action === 'logout') {
        session_destroy();
        header('Location: index.php');
        exit;
    }

    if ($action === 'save' && !empty($_SESSION['admin'])) {
        $phone     = trim($_POST['phone'] ?? '');
        $phone_raw = preg_replace('/\D/', '', $phone);
        $email     = trim($_POST['email'] ?? '');
        $max_link  = trim($_POST['social_max'] ?? '');
        $vk_link   = trim($_POST['social_vk'] ?? '');
        $leg_name  = trim($_POST['legal_name'] ?? '');
        $leg_inn   = trim($_POST['legal_inn'] ?? '');
        $leg_ogrn  = trim($_POST['legal_ogrn'] ?? '');

        $testimonials_raw = $_POST['testimonials_json'] ?? '[]';
        $testimonials = json_decode($testimonials_raw, true);
        if (!is_array($testimonials)) $testimonials = [];

        $data = [
            'phone'     => $phone,
            'phone_raw' => $phone_raw,
            'email'     => $email,
            'social'    => ['max' => $max_link, 'vk' => $vk_link],
            'legal'     => ['name' => $leg_name, 'inn' => $leg_inn, 'ogrn' => $leg_ogrn],
            'testimonials' => $testimonials,
        ];

        $js = 'window.SITE_CONFIG = ' . json_encode($data, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT) . ";\n";

        if (file_put_contents(CONFIG_FILE, $js) !== false) {
            $success = '✓ Настройки сохранены!';
        } else {
            $error = 'Ошибка: не удалось записать файл. Проверьте права на js/site-config.js';
        }
    }
}

// --- Read current config ---
function readConfig() {
    if (!file_exists(CONFIG_FILE)) return [];
    $src = file_get_contents(CONFIG_FILE);
    if (preg_match('/window\.SITE_CONFIG\s*=\s*(\{.*\});/s', $src, $m)) {
        $data = json_decode($m[1], true);
        return is_array($data) ? $data : [];
    }
    return [];
}

$cfg = readConfig();
$isAuth = !empty($_SESSION['admin']);

function val($cfg, ...$keys) {
    $v = $cfg;
    foreach ($keys as $k) $v = $v[$k] ?? '';
    return htmlspecialchars((string)$v, ENT_QUOTES);
}
?>
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Админка — Emoji Tours</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: system-ui, -apple-system, sans-serif; background: #f5f5f5; color: #111; min-height: 100vh; }

    /* Layout */
    .page { max-width: 860px; margin: 0 auto; padding: 40px 20px 80px; }
    header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 32px; }
    header h1 { font-size: 1.4rem; font-weight: 700; }
    header span { font-size: .85rem; color: #666; }

    /* Card */
    .card { background: #fff; border-radius: 16px; padding: 28px 32px; margin-bottom: 24px; box-shadow: 0 1px 4px rgba(0,0,0,.08); }
    .card h2 { font-size: 1rem; font-weight: 700; margin-bottom: 20px; color: #333; letter-spacing: .02em; text-transform: uppercase; font-size: .75rem; }

    /* Fields */
    .fields { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
    .field { display: flex; flex-direction: column; gap: 6px; }
    .field.full { grid-column: 1 / -1; }
    label { font-size: .8rem; font-weight: 600; color: #555; }
    input[type=text], input[type=email], input[type=url], input[type=password], textarea {
      border: 1.5px solid #e0e0e0; border-radius: 10px; padding: 10px 14px;
      font-size: .95rem; font-family: inherit; transition: border-color .15s;
      width: 100%;
    }
    input:focus, textarea:focus { outline: none; border-color: #f4a300; }
    textarea { resize: vertical; min-height: 90px; }

    /* Testimonials */
    .testimonials-list { display: flex; flex-direction: column; gap: 16px; }
    .testimonial-item {
      border: 1.5px solid #e8e8e8; border-radius: 12px; padding: 16px 18px;
      position: relative; background: #fafafa;
    }
    .t-row { display: grid; grid-template-columns: 80px 1fr 1fr 130px; gap: 10px; margin-bottom: 10px; align-items: end; }
    .t-text { margin-top: 4px; }
    .t-text label { display: block; margin-bottom: 6px; }
    .btn-remove {
      position: absolute; top: 12px; right: 14px;
      background: none; border: none; cursor: pointer; font-size: 1.1rem; color: #ccc;
      line-height: 1; padding: 2px 6px; border-radius: 6px;
    }
    .btn-remove:hover { background: #fee2e2; color: #dc2626; }
    .btn-add {
      display: inline-flex; align-items: center; gap: 6px;
      padding: 10px 18px; border-radius: 10px; border: 1.5px dashed #ccc;
      background: none; cursor: pointer; font-size: .9rem; color: #666; font-family: inherit;
      transition: border-color .15s, color .15s;
    }
    .btn-add:hover { border-color: #f4a300; color: #f4a300; }
    .style-select { width: 100%; border: 1.5px solid #e0e0e0; border-radius: 10px; padding: 10px 14px; font-size: .9rem; font-family: inherit; background: #fff; }
    .style-select:focus { outline: none; border-color: #f4a300; }

    /* Buttons */
    .actions { display: flex; gap: 12px; align-items: center; margin-top: 8px; }
    .btn-save {
      padding: 13px 32px; background: #f4a300; color: #fff; font-weight: 700;
      border: none; border-radius: 12px; font-size: 1rem; cursor: pointer; font-family: inherit;
      transition: background .15s;
    }
    .btn-save:hover { background: #d98f00; }
    .btn-logout {
      padding: 8px 18px; background: none; border: 1.5px solid #e0e0e0;
      border-radius: 10px; font-size: .85rem; cursor: pointer; font-family: inherit; color: #666;
      transition: border-color .15s;
    }
    .btn-logout:hover { border-color: #999; color: #111; }

    /* Alerts */
    .alert { padding: 12px 18px; border-radius: 10px; margin-bottom: 20px; font-size: .9rem; font-weight: 500; }
    .alert-success { background: #dcfce7; color: #166534; }
    .alert-error { background: #fee2e2; color: #991b1b; }

    /* Login */
    .login-wrap { display: flex; justify-content: center; padding-top: 80px; }
    .login-card { background: #fff; border-radius: 20px; padding: 40px 40px 36px; width: 100%; max-width: 360px; box-shadow: 0 4px 20px rgba(0,0,0,.1); }
    .login-card h1 { font-size: 1.3rem; font-weight: 800; margin-bottom: 8px; }
    .login-card p { color: #666; font-size: .9rem; margin-bottom: 28px; }
    .login-card .field { margin-bottom: 16px; }
    .login-card .btn-save { width: 100%; margin-top: 8px; }

    @media (max-width: 600px) {
      .fields { grid-template-columns: 1fr; }
      .t-row { grid-template-columns: 1fr 1fr; }
      .t-row > *:last-child { grid-column: 1/-1; }
    }
  </style>
</head>
<body>

<?php if (!$isAuth): ?>
<!-- LOGIN -->
<div class="login-wrap">
  <div class="login-card">
    <h1>🌍 Emoji Tours</h1>
    <p>Войдите, чтобы изменить контактные данные, ссылки и отзывы.</p>
    <?php if ($error): ?><div class="alert alert-error"><?= htmlspecialchars($error) ?></div><?php endif; ?>
    <form method="POST">
      <input type="hidden" name="action" value="login">
      <div class="field">
        <label for="pw">Пароль</label>
        <input type="password" id="pw" name="password" autofocus placeholder="••••••••">
      </div>
      <button type="submit" class="btn-save">Войти</button>
    </form>
  </div>
</div>

<?php else: ?>
<!-- ADMIN -->
<div class="page">
  <header>
    <h1>🌍 Управление сайтом</h1>
    <form method="POST" style="display:inline">
      <input type="hidden" name="action" value="logout">
      <button class="btn-logout">Выйти</button>
    </form>
  </header>

  <?php if ($error): ?><div class="alert alert-error"><?= htmlspecialchars($error) ?></div><?php endif; ?>
  <?php if ($success): ?><div class="alert alert-success"><?= htmlspecialchars($success) ?></div><?php endif; ?>

  <form method="POST" id="main-form">
    <input type="hidden" name="action" value="save">

    <!-- Contacts -->
    <div class="card">
      <h2>Контакты</h2>
      <div class="fields">
        <div class="field">
          <label for="phone">Телефон</label>
          <input type="text" id="phone" name="phone" value="<?= val($cfg, 'phone') ?>" placeholder="+7 000-000-00-00">
        </div>
        <div class="field">
          <label for="email">Email</label>
          <input type="email" id="email" name="email" value="<?= val($cfg, 'email') ?>" placeholder="mail@example.com">
        </div>
      </div>
    </div>

    <!-- Social -->
    <div class="card">
      <h2>Социальные сети</h2>
      <div class="fields">
        <div class="field full">
          <label for="social_max">Ссылка MAX</label>
          <input type="url" id="social_max" name="social_max" value="<?= val($cfg, 'social', 'max') ?>">
        </div>
        <div class="field full">
          <label for="social_vk">Ссылка VK</label>
          <input type="url" id="social_vk" name="social_vk" value="<?= val($cfg, 'social', 'vk') ?>">
        </div>
      </div>
    </div>

    <!-- Legal -->
    <div class="card">
      <h2>Юридические данные</h2>
      <div class="fields">
        <div class="field full">
          <label for="legal_name">ФИО предпринимателя</label>
          <input type="text" id="legal_name" name="legal_name" value="<?= val($cfg, 'legal', 'name') ?>">
        </div>
        <div class="field">
          <label for="legal_inn">ИНН</label>
          <input type="text" id="legal_inn" name="legal_inn" value="<?= val($cfg, 'legal', 'inn') ?>">
        </div>
        <div class="field">
          <label for="legal_ogrn">ОГРН ИП</label>
          <input type="text" id="legal_ogrn" name="legal_ogrn" value="<?= val($cfg, 'legal', 'ogrn') ?>">
        </div>
      </div>
    </div>

    <!-- Testimonials -->
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
var testimonials = <?= json_encode($cfg['testimonials'] ?? [], JSON_UNESCAPED_UNICODE) ?>;

function renderList() {
  var list = document.getElementById('testimonials-list');
  list.innerHTML = '';
  testimonials.forEach(function(t, i) {
    var div = document.createElement('div');
    div.className = 'testimonial-item';
    div.innerHTML =
      '<button type="button" class="btn-remove" onclick="removeTestimonial(' + i + ')" title="Удалить">✕</button>' +
      '<div class="t-row">' +
        field('Инициалы', 'text', t.initials || '', 'initials', i, 'М') +
        field('Имя', 'text', t.name || '', 'name', i, 'Иван И.') +
        field('Подпись', 'text', t.label || '', 'label', i, 'Отдых в Таиланде') +
        '<div class="field">' +
          '<label>Стиль карточки</label>' +
          '<select class="style-select" data-i="' + i + '" data-f="style" onchange="updateField(this)">' +
            '<option value="filled"' + (t.style === 'filled' ? ' selected' : '') + '>Заливка (оранжевая)</option>' +
            '<option value="outlined"' + (t.style === 'outlined' ? ' selected' : '') + '>Контур (белая)</option>' +
          '</select>' +
        '</div>' +
      '</div>' +
      '<div class="t-text">' +
        '<label>Текст отзыва</label>' +
        '<textarea rows="4" data-i="' + i + '" data-f="text" onchange="updateField(this)" oninput="updateField(this)">' + escAttr(t.text || '') + '</textarea>' +
      '</div>';
    list.appendChild(div);
  });
  syncJson();
}

function field(label, type, value, fname, idx, placeholder) {
  return '<div class="field">' +
    '<label>' + label + '</label>' +
    '<input type="' + type + '" value="' + escAttr(value) + '" placeholder="' + placeholder + '" ' +
    'data-i="' + idx + '" data-f="' + fname + '" oninput="updateField(this)">' +
    '</div>';
}

function escAttr(s) {
  return String(s).replace(/&/g,'&amp;').replace(/"/g,'&quot;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

function updateField(el) {
  var i = parseInt(el.dataset.i);
  var f = el.dataset.f;
  testimonials[i][f] = el.value;
  syncJson();
}

function removeTestimonial(i) {
  testimonials.splice(i, 1);
  renderList();
}

function addTestimonial() {
  testimonials.push({ initials: '', name: '', label: '', style: 'outlined', text: '' });
  renderList();
  // scroll to new item
  var items = document.querySelectorAll('.testimonial-item');
  if (items.length) items[items.length - 1].scrollIntoView({ behavior: 'smooth', block: 'center' });
}

function syncJson() {
  document.getElementById('testimonials-json').value = JSON.stringify(testimonials);
}

// Sync before submit
document.getElementById('main-form').addEventListener('submit', syncJson);

renderList();
</script>
<?php endif; ?>
</body>
</html>
