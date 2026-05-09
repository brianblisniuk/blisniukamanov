(function () {
  "use strict";

  // ========== Sticky header shadow on scroll ==========
  const header = document.getElementById("siteHeader");
  const onScroll = () => {
    if (!header) return;
    if (window.scrollY > 8) header.classList.add("scrolled");
    else header.classList.remove("scrolled");
  };
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  // ========== Mobile drawer ==========
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
    window.addEventListener("resize", () => { if (window.innerWidth > 800) close(); });
  }

  // ========== Spotlight crossfade ==========
  const slides = document.querySelectorAll("#spotlightFrame .slide");
  const slidePrev = document.getElementById("slidePrev");
  const slideNext = document.getElementById("slideNext");
  if (slides.length) {
    let idx = 0;
    const go = (next) => {
      slides[idx].classList.remove("active");
      idx = (next + slides.length) % slides.length;
      slides[idx].classList.add("active");
    };
    if (slidePrev) slidePrev.addEventListener("click", () => go(idx - 1));
    if (slideNext) slideNext.addEventListener("click", () => go(idx + 1));
    setInterval(() => go(idx + 1), 6500);
  }

  // ========== Tabs ==========
  const tabs = document.querySelectorAll(".tabs .tab");
  if (tabs.length) {
    tabs.forEach((t) => {
      t.addEventListener("click", () => {
        tabs.forEach((x) => x.classList.remove("active"));
        t.classList.add("active");
      });
    });
  }

  // ========== Reveal on scroll ==========
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
      { threshold: 0.1, rootMargin: "0px 0px -40px 0px" }
    );
    els.forEach((el) => io.observe(el));
  } else {
    els.forEach((el) => el.classList.add("in"));
  }

  // ========== Smooth anchor offset for sticky header ==========
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
})();
