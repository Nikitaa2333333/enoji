window.PDFDownload = {
  async download(countryName, contentId = 'main-content') {
    const btn = window.event ? window.event.currentTarget : null;
    const originalContent = btn ? btn.innerHTML : null;
    
    try {
      if (btn) {
        btn.innerHTML = '<span class="animate-spin inline-block mr-2">↻</span>Создание...';
        btn.style.opacity = '0.7';
        btn.style.pointerEvents = 'none';
      }

      const content = document.getElementById(contentId);
      if (!content) throw new Error('Главный блок контента не найден');

      // Создаем временный контейнер
      const pdfContainer = document.createElement('div');
      pdfContainer.id = 'pdf-export-container';
      
      // Клонируем
      const clone = content.cloneNode(true);
      // Оставляем только текст и заголовки, убираем интерактив и тяжелые элементы
      const toRemove = clone.querySelectorAll('img, form, iframe, script, .no-pdf, button, .action-buttons, .material-symbols-outlined, #mobile-drawer, #drawer-overlay, nav');
      toRemove.forEach(el => el.remove());

      // Добавляем заголовок прямо текстом
      const header = document.createElement('div');
      header.innerHTML = `
        <div style="border-bottom: 2px solid #000; padding-bottom: 15px; margin-bottom: 25px; text-align: center;">
          <h1 style="font-size: 20pt; margin: 0; color: black; font-weight: bold;">ПАМЯТКА ТУРИСТУ: ${countryName.toUpperCase()}</h1>
          <div style="font-size: 10pt; color: #333; margin-top: 5px;">Эмоджи Турс • +7 (963) 649-18-52 • www.emojitours.ru</div>
        </div>
      `;
      
      pdfContainer.appendChild(header);
      pdfContainer.appendChild(clone);
      document.body.appendChild(pdfContainer);

      const style = document.createElement('style');
      style.innerHTML = `
        #pdf-export-container {
          position: fixed !important;
          left: -10000px !important; /* Убираем далеко за экран */
          top: 0 !important;
          width: 700px !important; /* Узкий формат лучше ложится в PDF без обрезки */
          padding: 40px !important;
          background: white !important;
          color: black !important;
          font-family: Arial, sans-serif !important;
          z-index: -9999 !important;
          visibility: visible !important;
          display: block !important;
          line-height: 1.4 !important;
        }
        #pdf-export-container * {
          background: transparent !important;
          color: black !important;
          visibility: visible !important;
          opacity: 1 !important;
          box-shadow: none !important;
          text-shadow: none !important;
        }
        #pdf-export-container p, #pdf-export-container li {
          font-size: 11pt !important;
          margin-bottom: 10pt !important;
          display: block !important;
          page-break-inside: auto !important;
        }
        #pdf-export-container h1, #pdf-export-container h2, #pdf-export-container h3 {
          font-weight: bold !important;
          margin-top: 15pt !important;
          margin-bottom: 10pt !important;
          page-break-after: avoid !important;
        }
        #pdf-export-container .table-container td {
          border: 1px solid #ddd !important;
          padding: 8px !important;
        }
        #pdf-export-container ul { padding-left: 20pt !important; margin-bottom: 10pt !important; }
        #pdf-export-container li { display: list-item !important; list-style-type: disc !important; }
      `;
      pdfContainer.appendChild(style);

      const opt = {
        margin: [15, 10, 15, 10], // top, left, bottom, right
        filename: 'Памятка_' + countryName + '.pdf',
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 1.5, useCORS: true, backgroundColor: '#ffffff' },
        jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
      };

      // Ждем отрисовки
      await new Promise(resolve => setTimeout(resolve, 800));
      
      await html2pdf().set(opt).from(pdfContainer).save();
      
      document.body.removeChild(pdfContainer);

    } catch (error) {
       console.error('PDF Error:', error);
       alert('Ошибка: ' + error.message);
    } finally {
      if (btn) {
        btn.innerHTML = originalContent;
        btn.style.opacity = '1';
        btn.style.pointerEvents = 'auto';
      }
    }
  }
};
