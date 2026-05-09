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
  const hamburger = document.getElementById("hamburger");
  const drawer = document.getElementById("mobileDrawer");
  if (hamburger && drawer) {
    const close = () => {
      hamburger.classList.remove("open");
      drawer.classList.remove("open");
      hamburger.setAttribute("aria-expanded", "false");
      drawer.setAttribute("aria-hidden", "true");
      document.body.style.overflow = "";
    };
    hamburger.addEventListener("click", () => {
      const open = hamburger.classList.toggle("open");
      drawer.classList.toggle("open", open);
      hamburger.setAttribute("aria-expanded", String(open));
      drawer.setAttribute("aria-hidden", String(!open));
      document.body.style.overflow = open ? "hidden" : "";
    });
    drawer.querySelectorAll("a").forEach((a) => a.addEventListener("click", close));
    window.addEventListener("resize", () => {
      if (window.innerWidth > 800) close();
    });
  }

  // ========== Ways carousel: prev/next ==========
  const track = document.getElementById("waysTrack");
  const prevBtn = document.getElementById("waysPrev");
  const nextBtn = document.getElementById("waysNext");
  if (track && prevBtn && nextBtn) {
    const step = () => {
      const card = track.querySelector(".way-card");
      if (!card) return 360;
      const gap = 24;
      return card.getBoundingClientRect().width + gap;
    };
    prevBtn.addEventListener("click", () => track.scrollBy({ left: -step(), behavior: "smooth" }));
    nextBtn.addEventListener("click", () => track.scrollBy({ left: step(), behavior: "smooth" }));
  }

  // ========== Testimonial slider ==========
  const testimonials = Array.from(document.querySelectorAll(".testimonial"));
  const dotsWrap = document.getElementById("testimonialDots");
  if (testimonials.length && dotsWrap) {
    let active = 0;
    testimonials.forEach((_, i) => {
      const dot = document.createElement("button");
      dot.type = "button";
      dot.setAttribute("aria-label", "Mostrar testimonio " + (i + 1));
      if (i === 0) dot.classList.add("active");
      dot.addEventListener("click", () => go(i));
      dotsWrap.appendChild(dot);
    });
    const dots = Array.from(dotsWrap.children);
    const go = (i) => {
      testimonials[active].classList.remove("active");
      dots[active].classList.remove("active");
      active = (i + testimonials.length) % testimonials.length;
      testimonials[active].classList.add("active");
      dots[active].classList.add("active");
    };
    setInterval(() => go(active + 1), 6500);
  }

  // ========== Reveal on scroll ==========
  const targets = [
    ".section-head",
    ".art-card",
    ".dest-card",
    ".editorial-text",
    ".way-card",
    ".mag-card",
    ".heritage-text",
    ".heritage-image",
    ".intro-text",
    ".testimonial.active",
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
      { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
    );
    els.forEach((el) => io.observe(el));
  } else {
    els.forEach((el) => el.classList.add("in"));
  }

  // ========== Smooth anchor offset for sticky header ==========
  document.querySelectorAll('a[href^="#"]').forEach((a) => {
    a.addEventListener("click", (e) => {
      const id = a.getAttribute("href");
      if (!id || id === "#") return;
      const target = document.querySelector(id);
      if (!target) return;
      e.preventDefault();
      const headerH = header ? header.getBoundingClientRect().height : 80;
      const top = target.getBoundingClientRect().top + window.scrollY - headerH - 12;
      window.scrollTo({ top, behavior: "smooth" });
    });
  });
})();
