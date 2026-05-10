(function () {
  "use strict";

  /* ==========================================================
     Floating action stack: WhatsApp + "Speak to expert" pill
     Both injected once site-wide
     ========================================================== */
  if (!document.getElementById("fabStack")) {
    const stack = document.createElement("div");
    stack.id = "fabStack";
    stack.className = "fab-stack";

    // "Hablá con un experto" pill (opens modal)
    const expert = document.createElement("button");
    expert.type = "button";
    expert.className = "expert-fab js-expert-trigger";
    expert.setAttribute("aria-haspopup", "dialog");
    expert.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg><span>Hablá con un experto</span>';
    stack.appendChild(expert);

    // WhatsApp circular FAB
    const wa = document.createElement("a");
    wa.id = "waButton";
    wa.className = "whatsapp-fab";
    wa.href = "https://wa.me/5491161395550?text=" + encodeURIComponent("Hola, me gustaría hablar con un asesor de Blisniuk & Amanov.");
    wa.target = "_blank";
    wa.rel = "noopener";
    wa.setAttribute("aria-label", "Chatear por WhatsApp");
    wa.innerHTML = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M17.5 14.4c-.3-.1-1.7-.8-2-.9-.3-.1-.5-.1-.7.1-.2.3-.8.9-1 1.1-.2.2-.4.2-.7.1-.3-.1-1.2-.5-2.4-1.5-.9-.8-1.5-1.7-1.7-2-.2-.3 0-.5.1-.6.1-.1.3-.4.4-.5.1-.2.2-.3.3-.5.1-.2 0-.4 0-.5-.1-.1-.7-1.6-.9-2.2-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.7.4-.2.3-.9.9-.9 2.2 0 1.3.9 2.5 1.1 2.7.1.2 1.9 2.9 4.6 4 .6.3 1.1.4 1.5.6.6.2 1.2.2 1.6.1.5-.1 1.7-.7 1.9-1.4.2-.7.2-1.3.2-1.4-.1-.1-.3-.2-.6-.3zM12 2C6.5 2 2 6.5 2 12c0 1.8.5 3.5 1.4 5L2 22l5.2-1.4c1.5.8 3.1 1.3 4.8 1.3 5.5 0 10-4.5 10-10S17.5 2 12 2zm0 18c-1.6 0-3.1-.4-4.4-1.2l-.3-.2-3.2.9.9-3.1-.2-.3C3.9 14.9 3.5 13.5 3.5 12c0-4.7 3.8-8.5 8.5-8.5s8.5 3.8 8.5 8.5-3.8 8.5-8.5 8.5z"/></svg>';
    stack.appendChild(wa);

    document.body.appendChild(stack);
  }

  /* ==========================================================
     "Hablá con un experto" modal — injected once
     ========================================================== */
  function ctxFromPage() {
    // Detect region/country from the page context
    const path = location.pathname.toLowerCase();
    if (path.includes("europe")) return { region: "Europa", country: "" };
    if (path.includes("gran-migracion")) return { region: "África", country: "Kenia y Tanzania" };
    if (path.includes("small-group")) return { region: "", country: "" };
    return { region: "", country: "" };
  }

  if (!document.getElementById("expertModal")) {
    const ctx = ctxFromPage();
    const ctxLabel = ctx.region ? "Consultar sobre " + ctx.region : "Hablá con un experto";

    const wrap = document.createElement("div");
    wrap.id = "expertModal";
    wrap.className = "modal-wrap";
    wrap.setAttribute("aria-hidden", "true");
    wrap.setAttribute("role", "dialog");
    wrap.setAttribute("aria-labelledby", "expertModalTitle");
    wrap.innerHTML = `
      <div class="modal-backdrop" data-close></div>
      <div class="modal-card">
        <button class="modal-close" data-close aria-label="Cerrar">×</button>
        <h2 id="expertModalTitle" class="modal-title">${ctxLabel}</h2>

        <form name="consulta-experto" method="POST" data-netlify="true" data-netlify-honeypot="bot-field" action="/gracias.html" class="modal-form">
          <input type="hidden" name="form-name" value="consulta-experto" />
          <p class="hidden-field"><label>No completar: <input name="bot-field" /></label></p>
          <input type="hidden" name="contexto" value="${location.pathname}" />

          <fieldset class="radios m-radios">
            <legend>¿Sos asesor de viajes?</legend>
            <label><input type="radio" name="asesor" value="si" /> Sí</label>
            <label><input type="radio" name="asesor" value="no" checked /> No</label>
          </fieldset>

          <label class="field">
            <span>Elegí una región</span>
            <select name="region" required>
              <option value="">Seleccionar región</option>
              <option ${ctx.region==='África'?'selected':''}>África</option>
              <option ${ctx.region==='Asia'?'selected':''}>Asia</option>
              <option ${ctx.region==='Europa'?'selected':''}>Europa</option>
              <option ${ctx.region==='Sudamérica'?'selected':''}>Sudamérica</option>
              <option ${ctx.region==='Norteamérica'?'selected':''}>Norteamérica</option>
              <option ${ctx.region==='Oceanía'?'selected':''}>Oceanía</option>
              <option ${ctx.region==='Antártida y polos'?'selected':''}>Antártida y polos</option>
              <option ${ctx.region==='Oriente Próximo y Norte de África'?'selected':''}>Oriente Próximo y Norte de África</option>
              <option ${ctx.region==='Caribe'?'selected':''}>Caribe</option>
              <option>Aún no lo sé</option>
            </select>
          </label>

          <label class="field">
            <span>Elegí un país</span>
            <input type="text" name="pais" placeholder="Cualquiera" value="${ctx.country}" />
          </label>

          <label class="field">
            <span>Contanos sobre tu viaje ideal</span>
            <textarea name="mensaje" rows="4" placeholder="Fechas tentativas, intereses, viajeros…"></textarea>
          </label>

          <label class="check"><input type="checkbox" name="acepta_privacidad" value="si" required /> Acepto la <a href="#" target="_blank">política de privacidad</a></label>
          <label class="check"><input type="checkbox" name="acepta_news" value="si" /> Quiero recibir novedades, salidas exclusivas y otra información de Blisniuk &amp; Amanov</label>

          <button type="submit" class="btn btn-laurel modal-submit">Hablar con un experto</button>

          <p class="modal-legal">Al enviar este formulario nos autorizás a que te contactemos con respecto a esta consulta. Tus datos no se comparten con terceros. Podés darte de baja en cualquier momento.</p>
        </form>
      </div>
    `;
    document.body.appendChild(wrap);

    const open = () => {
      wrap.classList.add("open");
      wrap.setAttribute("aria-hidden", "false");
      document.body.style.overflow = "hidden";
    };
    const close = () => {
      wrap.classList.remove("open");
      wrap.setAttribute("aria-hidden", "true");
      document.body.style.overflow = "";
    };

    document.addEventListener("click", (e) => {
      const trig = e.target.closest(".js-expert-trigger");
      if (trig) { e.preventDefault(); open(); return; }
      const closer = e.target.closest("[data-close]");
      if (closer && wrap.contains(closer)) { e.preventDefault(); close(); }
    });
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && wrap.classList.contains("open")) close();
    });
  }

  /* ==========================================================
     Sticky header shadow on scroll
     ========================================================== */
  const header = document.getElementById("siteHeader");
  const onScroll = () => {
    if (!header) return;
    if (window.scrollY > 8) header.classList.add("scrolled");
    else header.classList.remove("scrolled");
  };
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ==========================================================
     Mobile drawer
     ========================================================== */
  const trigger = document.getElementById("menuTrigger");
  const drawer = document.getElementById("mobileDrawer");
  if (trigger && drawer) {
    const close = () => {
      trigger.classList.remove("open");
      drawer.classList.remove("open");
      drawer.setAttribute("aria-hidden", "true");
      document.body.style.overflow = "";
    };
    trigger.addEventListener("click", () => {
      const open = trigger.classList.toggle("open");
      drawer.classList.toggle("open", open);
      drawer.setAttribute("aria-hidden", String(!open));
      document.body.style.overflow = open ? "hidden" : "";
    });
    drawer.querySelectorAll("a").forEach((a) => a.addEventListener("click", close));
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") close();
    });
    window.addEventListener("resize", () => { if (window.innerWidth > 800) close(); });
  }

  /* ==========================================================
     Spotlight crossfade with autoplay + manual controls
     ========================================================== */
  const slides = document.querySelectorAll("#spotlightFrame .slide");
  const slidePrev = document.getElementById("slidePrev");
  const slideNext = document.getElementById("slideNext");
  if (slides.length) {
    let idx = 0;
    let autoTimer;
    const go = (next) => {
      slides[idx].classList.remove("active");
      idx = (next + slides.length) % slides.length;
      slides[idx].classList.add("active");
    };
    const restartAuto = () => {
      clearInterval(autoTimer);
      autoTimer = setInterval(() => go(idx + 1), 7000);
    };
    if (slidePrev) slidePrev.addEventListener("click", () => { go(idx - 1); restartAuto(); });
    if (slideNext) slideNext.addEventListener("click", () => { go(idx + 1); restartAuto(); });
    restartAuto();
  }

  /* ==========================================================
     Tabs (homepage "Where to go" — swap visible cards)
     Also supports rec-tabs (filter tabs)
     ========================================================== */
  document.querySelectorAll(".tabs").forEach((group) => {
    const buttons = Array.from(group.querySelectorAll(".tab"));
    const panelKey = (b) => b.dataset.tab;
    const panels = Array.from(document.querySelectorAll(".tab-panel"));

    buttons.forEach((b) => b.addEventListener("click", () => {
      buttons.forEach((x) => x.classList.remove("active"));
      b.classList.add("active");
      const key = panelKey(b);
      panels.forEach((p) => {
        const match = p.dataset.panel === key;
        p.style.display = match ? "" : (panels.length > 1 ? "none" : "");
        if (match) {
          p.classList.add("just-tabbed");
          setTimeout(() => p.classList.remove("just-tabbed"), 600);
        }
      });
    }));
  });

  // Rec tabs (small-group page — visual feedback only)
  document.querySelectorAll(".rec-tabs").forEach((group) => {
    const tabs = Array.from(group.querySelectorAll(".rec-tab"));
    tabs.forEach((t) => t.addEventListener("click", () => {
      tabs.forEach((x) => x.classList.remove("active"));
      t.classList.add("active");
      const list = group.parentElement.querySelector(".rec-list");
      if (list) {
        list.style.opacity = "0";
        setTimeout(() => { list.style.opacity = "1"; }, 250);
      }
    }));
  });

  /* ==========================================================
     Filter button (toggles sidebar visibility on mobile)
     ========================================================== */
  document.querySelectorAll(".filter-button").forEach((btn) => {
    btn.addEventListener("click", () => {
      const filters = document.querySelector(".filters");
      if (filters) {
        filters.classList.toggle("filters--open");
        filters.scrollIntoView({ behavior: "smooth", block: "nearest" });
      }
    });
  });

  /* ==========================================================
     Filter sidebar — visual checkbox toggle on links
     ========================================================== */
  document.querySelectorAll(".filters .filter-list a").forEach((a) => {
    a.addEventListener("click", (e) => {
      e.preventDefault();
      a.classList.toggle("active");
      // Update count display if present
      const summary = a.closest("details")?.querySelector("summary");
      if (summary) {
        const active = a.closest(".filter-list").querySelectorAll("a.active").length;
        const baseLabel = summary.dataset.label || summary.textContent.replace(/\s*\(\d+\)\s*$/, "").trim();
        summary.dataset.label = baseLabel;
        summary.textContent = active > 0 ? `${baseLabel} (${active})` : baseLabel;
      }
    });
  });

  /* ==========================================================
     Forms — newsletter and any inline form: prevent submit, show feedback
     ========================================================== */
  document.querySelectorAll("form.newsletter, form.newsletter-form").forEach((form) => {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const email = form.querySelector('input[type="email"]');
      if (!email || !email.value || !/.+@.+\..+/.test(email.value)) {
        showToast("Por favor ingresá un correo válido.", "error");
        return;
      }
      // simulate submit
      form.querySelectorAll("input").forEach((i) => i.value = "");
      showToast("¡Suscripción confirmada! Revisa tu correo.", "ok");
    });
  });

  /* ==========================================================
     Toast (small floating message)
     ========================================================== */
  function showToast(message, kind) {
    let toast = document.getElementById("toast");
    if (!toast) {
      toast = document.createElement("div");
      toast.id = "toast";
      toast.className = "toast";
      document.body.appendChild(toast);
    }
    toast.textContent = message;
    toast.dataset.kind = kind || "ok";
    toast.classList.add("show");
    clearTimeout(toast._t);
    toast._t = setTimeout(() => toast.classList.remove("show"), 3500);
  }

  /* ==========================================================
     Subnav scroll-spy (highlight current section in subnav)
     ========================================================== */
  const subnavLinks = document.querySelectorAll(".subnav a[href^='#']");
  if (subnavLinks.length && "IntersectionObserver" in window) {
    const sections = Array.from(subnavLinks)
      .map((l) => document.querySelector(l.getAttribute("href")))
      .filter(Boolean);
    if (sections.length) {
      const obs = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            subnavLinks.forEach((l) => l.classList.remove("active"));
            const link = document.querySelector(`.subnav a[href="#${entry.target.id}"]`);
            if (link) link.classList.add("active");
          }
        });
      }, { rootMargin: "-30% 0px -55% 0px" });
      sections.forEach((s) => obs.observe(s));
    }
  }

  /* ==========================================================
     Smooth anchor offset for sticky header
     ========================================================== */
  document.querySelectorAll('a[href^="#"]').forEach((a) => {
    a.addEventListener("click", (e) => {
      const id = a.getAttribute("href");
      if (!id || id === "#" || id.length < 2) return;
      const target = document.querySelector(id);
      if (!target) return;
      e.preventDefault();
      const headerH = header ? header.getBoundingClientRect().height : 80;
      const top = target.getBoundingClientRect().top + window.scrollY - headerH - 12;
      window.scrollTo({ top, behavior: "smooth" });
    });
  });

  /* ==========================================================
     Reveal on scroll
     ========================================================== */
  const targets = [
    ".section-head",
    ".intro-text",
    ".img-card",
    ".trip-kinds-text",
    ".philanthropy-text",
    ".philanthropy-image",
    ".stat",
    ".rec-card",
    ".j-card",
    ".tailormade",
    ".feature",
    ".rec-row",
    ".day",
    ".ext-card",
    ".lodge-card",
    ".review",
    ".highlight",
  ];
  const els = document.querySelectorAll(targets.join(","));
  els.forEach((el) => el.classList.add("reveal"));
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("in");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.08, rootMargin: "0px 0px -40px 0px" }
    );
    els.forEach((el) => io.observe(el));
  } else {
    els.forEach((el) => el.classList.add("in"));
  }

  /* ==========================================================
     "Reservar" buttons in dates table — open contact CTA
     ========================================================== */
  document.querySelectorAll(".dates-table a.link-arrow").forEach((a) => {
    a.addEventListener("click", (e) => {
      e.preventDefault();
      const row = a.closest("tr");
      const date = row?.cells?.[0]?.textContent?.trim() || "";
      showToast(`Tu solicitud para la salida del ${date} se envió a tu asesor.`, "ok");
    });
  });

  /* ==========================================================
     Search trigger (header magnifier) — focuses on /viajes filter
     ========================================================== */
  document.querySelectorAll(".search-trigger").forEach((a) => {
    if (a.getAttribute("href") === "journeys.html") return; // anchor handles itself
  });

})();
