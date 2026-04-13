(function () {
  function esc(str) {
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function renderTestimonials(list) {
    return list.map(function (t, i) {
      var filled = t.style === 'filled';
      var cardCls = filled
        ? 'min-w-[85vw] md:min-w-[500px] p-10 bg-primary rounded-[3rem] shadow-sm snap-center flex flex-col'
        : 'min-w-[85vw] md:min-w-[400px] p-10 border border-primary/30 rounded-[3rem] shadow-sm snap-center flex flex-col';
      var textCls = 'text-base md:text-xl leading-relaxed font-medium' + (filled ? '' : ' text-black');
      var id = 'testimonial-' + i;
      var isLong = t.text.length > 300;

      var paragraphs = t.text.split('\n\n').map(function (p) {
        return p.trim() ? '<p>' + esc(p) + '</p>' : '';
      }).filter(Boolean).join('');

      var textBlock;
      if (isLong) {
        var fromColor = filled ? 'primary' : 'white';
        textBlock =
          '<div id="' + id + '-text" class="' + textCls + ' space-y-4 max-h-[320px] md:max-h-none overflow-hidden relative transition-all duration-500">' +
            paragraphs +
            '<div id="' + id + '-gradient" class="md:hidden absolute bottom-0 left-0 w-full h-16 bg-gradient-to-t from-' + fromColor + ' to-transparent pointer-events-none"></div>' +
          '</div>' +
          '<button id="' + id + '-btn" onclick="toggleTestimonialDyn(\'' + id + '\',\'' + fromColor + '\')" class="md:hidden flex items-center gap-1.5 text-sm font-bold opacity-70 hover:opacity-100 transition-opacity">' +
            '<span>Читать полностью</span>' +
            '<span class="material-symbols-outlined text-[20px]">expand_more</span>' +
          '</button>';
      } else {
        textBlock = '<p class="' + textCls + '">' + esc(t.text) + '</p>';
      }

      return '<div class="' + cardCls + '">' +
        '<div class="space-y-6">' + textBlock + '</div>' +
        '<div class="pt-8 flex items-center gap-4">' +
          '<div class="w-12 h-12 flex-shrink-0 bg-white/40 border border-black/5 rounded-full flex items-center justify-center font-bold text-lg text-black">' + esc(t.initials) + '</div>' +
          '<div>' +
            '<p class="font-bold">' + esc(t.name) + '</p>' +
            '<p class="text-sm opacity-60">' + esc(t.label) + '</p>' +
          '</div>' +
        '</div>' +
      '</div>';
    }).join('');
  }

  function init() {
    var c = window.SITE_CONFIG;
    if (!c) return;

    // Phone
    document.querySelectorAll('a[href^="tel:"]').forEach(function (el) {
      el.href = 'tel:+' + c.phone_raw;
      el.textContent = c.phone;
    });

    // Email
    document.querySelectorAll('a[href^="mailto:"]').forEach(function (el) {
      el.href = 'mailto:' + c.email;
      el.textContent = c.email;
    });

    // Social links
    document.querySelectorAll('a[href*="max.ru"]').forEach(function (el) {
      el.href = c.social.max;
    });
    document.querySelectorAll('a[href*="vk.com"]').forEach(function (el) {
      el.href = c.social.vk;
    });

    // Legal block — find div inside footer containing ИНН and ОГРН
    var footer = document.querySelector('footer');
    if (footer) {
      footer.querySelectorAll('div').forEach(function (div) {
        // Must have <strong> as direct child (the name) — avoids matching the parent wrapper div
        var hasDirectStrong = Array.from(div.children).some(function (ch) { return ch.tagName === 'STRONG'; });
        if (hasDirectStrong && div.textContent.includes('ИНН') && div.textContent.includes('ОГРН')) {
          div.innerHTML =
            'Индивидуальный предприниматель <br>' +
            '<strong class="text-black">' + esc(c.legal.name) + '</strong><br>' +
            'ИНН ' + esc(c.legal.inn) + ' <br>' +
            'ОГРН ИП ' + esc(c.legal.ogrn);
        }
      });
    }

    // Testimonials (index page only)
    var container = document.getElementById('testimonials-scroll');
    if (container && c.testimonials && c.testimonials.length) {
      container.innerHTML =
        renderTestimonials(c.testimonials) +
        '<div class="min-w-[8vw] md:hidden"></div>';
    }
  }

  // Expand/collapse for long testimonials rendered by this script
  window.toggleTestimonialDyn = function (id, fromColor) {
    var text = document.getElementById(id + '-text');
    var btn = document.getElementById(id + '-btn');
    var grad = document.getElementById(id + '-gradient');
    if (!text) return;
    if (text.style.maxHeight === 'none') {
      text.style.maxHeight = '320px';
      btn.querySelector('span:first-child').textContent = 'Читать полностью';
      btn.querySelector('span:last-child').textContent = 'expand_more';
      if (grad) grad.classList.remove('opacity-0');
    } else {
      text.style.maxHeight = 'none';
      btn.querySelector('span:first-child').textContent = 'Свернуть';
      btn.querySelector('span:last-child').textContent = 'expand_less';
      if (grad) grad.classList.add('opacity-0');
    }
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
