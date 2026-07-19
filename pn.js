/* Pasaporte Negro — envío de consultas al backend de la casa. */
(function () {
  var API = 'https://onnqcdjkvpvpvtsorpup.supabase.co/functions/v1/public-lead';

  function estadoDe(f) { return f.querySelector('.pn-form-estado'); }

  document.addEventListener('submit', function (ev) {
    var f = ev.target;
    if (!f || !f.classList || !f.classList.contains('pn-form')) return;
    ev.preventDefault();

    var estado = estadoDe(f);
    var boton = f.querySelector('button[type="submit"]');
    var datos = {};
    new FormData(f).forEach(function (v, k) { datos[k] = v; });
    datos.referrer = document.location.href;

    if (!datos.nombre || !datos.nombre.trim()) {
      estado.className = 'pn-form-estado error'; estado.textContent = 'Falta tu nombre.'; return;
    }
    if (!datos.email || datos.email.indexOf('@') < 1) {
      estado.className = 'pn-form-estado error'; estado.textContent = 'Revisá el correo.'; return;
    }

    boton.disabled = true;
    estado.className = 'pn-form-estado';
    estado.textContent = 'Enviando…';

    fetch(API, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(datos)
    })
      .then(function (r) { return r.json(); })
      .then(function (d) {
        if (!d || !d.ok) throw new Error((d && d.error) || 'error');
        f.reset();
        var oculto = f.querySelector('input[name="destino"]');
        if (oculto && oculto.dataset.valor) oculto.value = oculto.dataset.valor;
        estado.className = 'pn-form-estado ok';
        estado.textContent = 'Recibido. Te contesto por correo, en persona.';
      })
      .catch(function () {
        estado.className = 'pn-form-estado error';
        estado.textContent = 'No salió. Escribinos a pasaportenegroviajes@gmail.com y lo vemos.';
      })
      .then(function () { boton.disabled = false; });
  });
})();
