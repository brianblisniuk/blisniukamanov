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

/* El video del hero pesa 15 MB por pieza y son tres. En pantalla chica se le
   quitan las fuentes al elemento antes de que ningun script pida reproducir:
   queda el poster, que es la misma imagen. En escritorio se carga solo el de
   la diapositiva visible. Corre en el parseo, antes de DOMContentLoaded. */
(function () {
  var chica = window.innerWidth < 900 || (navigator.connection && navigator.connection.saveData);
  var videos = document.querySelectorAll('.spotlight-frame video.slide-media');
  if (!videos.length) return;

  if (chica) {
    for (var i = 0; i < videos.length; i++) {
      var v = videos[i];
      var fuentes = v.querySelectorAll('source');
      for (var k = 0; k < fuentes.length; k++) fuentes[k].parentNode.removeChild(fuentes[k]);
      v.removeAttribute('autoplay');
      v.setAttribute('preload', 'none');
      try { v.load(); } catch (e) {}
      var poster = v.getAttribute('poster');
      if (poster) { v.style.background = 'center/cover no-repeat url("' + poster + '")'; }
    }
    return;
  }

  function activar(v) {
    if (!v) return;
    if (v.getAttribute('preload') === 'none') { v.setAttribute('preload', 'auto'); try { v.load(); } catch (e) {} }
    var p = v.play(); if (p && p.catch) p.catch(function () {});
  }
  function arrancar() {
    activar(videos[0]);
    document.querySelectorAll('.spotlight-frame .slide').forEach(function (s) {
      new MutationObserver(function () {
        var v = s.querySelector('video.slide-media');
        if (!v) return;
        if (s.classList.contains('active')) activar(v);
        else { try { v.pause(); } catch (e) {} }
      }).observe(s, { attributes: true, attributeFilter: ['class'] });
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', arrancar);
  else arrancar();
})();
