import os
import re

file_path = r"c:\Users\User\Downloads\tilda dododo\pages\memos\sri-lanka.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix the unclosed section tags mess
# We will identify each section and re-wrap it properly.
sections_needed = [
    ("pered-otezdom", "Перед отъездом"),
    ("sobiraya-bagazh", "Собирая багаж"),
    ("v-rossijskom-aeroportu", "В российском аэропорту вылета/прилёта"),
    ("tamozhennyj-kontrol-sri-lanka", "Таможенный контроль в Шри-Ланке"),
    ("v-aeroportu-sri-lanka", "В аэропорту прилета/вылета Республики Шри-Ланка"),
    ("pasportnyj-kontrol-viza", "Паспортный контроль. Виза"),
    ("about-sri-lanka", "Демократическая Социалистическая Республика Шри-Ланка"),
    ("pravila-gigieny", "Правила личной гигиены и безопасности"),
    ("poterya-pasporta", "В случае потери паспорта"),
    ("poleznaya-info", "Полезная информация"),
]

# I'll use a more surgical approach for the script within the HTML.
# First, let's fix the navigation links if they are broken
content = content.replace('href="#v-rossijskom-aeroportu-vyleta-prilyota"', 'href="#v-rossijskom-aeroportu"')
content = content.replace('id="v-rossijskom-aeroportu-vyleta-prilyota"', 'id="v-rossijskom-aeroportu"')
content = content.replace('id="tamozhennyj-kontrol-v-shri-lanke"', 'id="tamozhennyj-kontrol-sri-lanka"')
content = content.replace('id="v-aeroportu-prileta-vyleta-respubliki-shri-lanka"', 'id="v-aeroportu-sri-lanka"')
content = content.replace('id="demokraticheskaya-sotsialisticheskaya-respublika-shri-lanka"', 'id="about-sri-lanka"')
content = content.replace('id="pravila-lichnoj-gigieny-i-bezopasnosti"', 'id="pravila-gigieny"')
content = content.replace('id="v-sluchae-poteri-pasporta"', 'id="poterya-pasporta"')
content = content.replace('id="poleznaya-informatsiya"', 'id="poleznaya-info"')

# 2. Fix the duplicate "sobiraya-bagazh"
# The first one is at line 341, the second at 357. 
# Let's find the unclosed section tags and fix them.
content = re.sub(r'</section>\s*</section>\s*</section>\s*</section>\s*</section>\s*</section>\s*</section>\s*</section>\s*</section>\s*</section>\s*</section>', '</section>', content)

# 3. Fix the Smooth Scroll Script (Event Delegation)
old_script = r'document.querySelectorAll\(\'a\[href\^="#"]\'\).forEach\(anchor => \{.*?\}\);'
new_script = r"""document.addEventListener('click', function(e) {
      const anchor = e.target.closest('a[href^="#"]');
      if (!anchor || anchor.getAttribute('href') === '#') return;

      const targetId = anchor.getAttribute('href');
      const targetElement = document.querySelector(targetId);

      if (targetElement) {
        e.preventDefault();
        if (anchor.closest('#mobile-drawer')) toggleMenu();
        isScrolling = true;
        document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
        anchor.classList.add('active');
        const desktopLink = document.querySelector(`#quick-links .nav-link[href="${targetId}"]`);
        if (desktopLink) desktopLink.classList.add('active');

        const headerOffset = 100;
        const elementPosition = targetElement.getBoundingClientRect().top;
        const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

        window.scrollTo({
          top: offsetPosition,
          behavior: "smooth"
        });
        setTimeout(() => { isScrolling = false; }, 1000);
      }
    });"""

content = re.sub(r'// Плавный скролл для всех ссылок\s*document.querySelectorAll\(\'a\[href\^="#"]\'\).forEach\(anchor => \{.*?\n\s+?\}\);', 
                 r"// Плавный скролл для всех ссылок (делегирование)\n    " + new_script, 
                 content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done! Fixed IDs, JS delegation and cleaned up structure.")
