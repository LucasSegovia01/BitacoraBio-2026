// Desplegable de usuario
document.addEventListener('click', function (e) {
  const btn = e.target.closest('.user-btn');
  const dropdown = document.querySelector('.user-dropdown');
  if (!dropdown) return;
  if (btn) {
    dropdown.classList.toggle('open');
  } else if (!e.target.closest('.user-dropdown')) {
    dropdown.classList.remove('open');
  }
});

// Pestañas (Resumen / Parámetros / Resultados / Notas)
document.querySelectorAll('.tabs').forEach(function (tabGroup) {
  tabGroup.addEventListener('click', function (e) {
    const tab = e.target.closest('.tab');
    if (!tab) return;
    const panelId = tab.getAttribute('data-tab');
    const container = tabGroup.closest('.tabs-container') || document;

    tabGroup.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    tab.classList.add('active');

    container.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
    const panel = container.querySelector('#' + panelId);
    if (panel) panel.classList.add('active');
  });
});

// Agregar / quitar filas de parámetro dinámicas (carga y búsqueda)
document.querySelectorAll('.add-param-btn').forEach(function (btn) {
  btn.addEventListener('click', function () {
    const list = document.querySelector(btn.getAttribute('data-target'));
    if (!list) return;
    const row = document.createElement('div');
    row.className = 'param-row';
    row.innerHTML = `
      <div class="field" style="margin-bottom:0">
        <input type="text" placeholder="Nombre del parámetro (ej. pH)">
      </div>
      <div class="field" style="margin-bottom:0">
        <input type="text" placeholder="Valor">
      </div>
      <button type="button" class="remove" title="Quitar parámetro">✕ Quitar</button>
    `;
    list.appendChild(row);
  });
});

document.addEventListener('click', function (e) {
  if (e.target.closest('.remove')) {
    e.target.closest('.param-row').remove();
  }
});

// Dropzone: resaltar al arrastrar un archivo
document.querySelectorAll('.dropzone').forEach(function (zone) {
  ['dragover', 'dragenter'].forEach(evt =>
    zone.addEventListener(evt, e => { e.preventDefault(); zone.style.borderColor = '#2F6FED'; })
  );
  ['dragleave', 'drop'].forEach(evt =>
    zone.addEventListener(evt, e => { e.preventDefault(); zone.style.borderColor = ''; })
  );
});

// Toast de confirmación de guardado (heurística 1 — Inicio)
function showToast(id) {
  document.querySelectorAll('.toast').forEach(t => t.classList.remove('show'));
  const el = document.getElementById(id);
  if (el) { el.classList.add('show'); el.scrollIntoView({ behavior: 'smooth', block: 'center' }); }
}
document.addEventListener('click', function (e) {
  if (e.target.closest('.close-toast')) {
    e.target.closest('.toast').classList.remove('show');
  }
});
const saveForm = document.querySelector('#form-cargar');
if (saveForm) {
  saveForm.addEventListener('submit', function (e) {
    e.preventDefault();
    showToast('toast-ok');
  });
}

// Preselección de proyecto al llegar desde "Cargar experimento para este proyecto"
document.addEventListener('DOMContentLoaded', function () {
  const params = new URLSearchParams(location.search);
  const proyecto = params.get('proyecto');
  const select = document.querySelector('#campo-proyecto');
  if (proyecto && select) select.value = proyecto;
});

// Búsqueda: habilitar "Hasta" solo si el filtro de fecha es por rango
const tipoFecha = document.querySelector('#tipo-fecha');
if (tipoFecha) {
  const hasta = document.querySelector('#fecha-hasta');
  function toggleHasta() {
    const esRango = tipoFecha.value === 'Rango de fechas';
    hasta.disabled = !esRango;
    hasta.closest('.field').style.opacity = esRango ? '1' : '0.5';
  }
  tipoFecha.addEventListener('change', toggleHasta);
  toggleHasta();
}

// Búsqueda: demo del estado "sin resultados"
const toggleEmptyBtn = document.querySelector('#toggle-empty-demo');
if (toggleEmptyBtn) {
  toggleEmptyBtn.addEventListener('click', function () {
    const results = document.querySelector('#results-table-wrap');
    const empty = document.querySelector('#results-empty');
    const showingEmpty = empty.style.display !== 'none';
    empty.style.display = showingEmpty ? 'none' : 'block';
    results.style.display = showingEmpty ? 'block' : 'none';
    toggleEmptyBtn.textContent = showingEmpty ? 'Ver ejemplo: sin resultados' : 'Ver ejemplo: con resultados';
  });
}
