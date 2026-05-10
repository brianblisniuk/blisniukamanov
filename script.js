(function () {
  "use strict";

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
