// Shared interactions for the preserved static conference pages.
(() => {
  const reveals = document.querySelectorAll('.reveal-hidden');
  if ('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.replace('reveal-hidden', 'reveal-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: .15 });
    reveals.forEach(element => observer.observe(element));
  } else {
    reveals.forEach(element => element.classList.remove('reveal-hidden'));
  }

  const toggle = document.querySelector('header button[aria-label="Toggle menu"]');
  const mobile = document.querySelector('#mobile-navigation');
  const closeMobile = () => {
    if (!toggle || !mobile) return;
    mobile.hidden = true;
    toggle.setAttribute('aria-expanded', 'false');
  };
  toggle?.addEventListener('click', () => {
    mobile.hidden = !mobile.hidden;
    toggle.setAttribute('aria-expanded', String(!mobile.hidden));
  });
  mobile?.querySelectorAll('button[aria-controls]').forEach(button => {
    button.addEventListener('click', () => {
      const submenu = document.getElementById(button.getAttribute('aria-controls'));
      submenu.hidden = !submenu.hidden;
      button.setAttribute('aria-expanded', String(!submenu.hidden));
    });
  });
  mobile?.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMobile));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && mobile && !mobile.hidden) {
      closeMobile(); toggle.focus();
    }
  });

  // The reference contact form composes an email in the visitor's mail app.
  document.querySelector('footer form')?.addEventListener('submit', event => {
    event.preventDefault();
    const form = event.currentTarget;
    if (!form.reportValidity()) return;
    const name = form.querySelector('[name="name"]').value.trim();
    const email = form.querySelector('[name="email"]').value.trim();
    const message = form.querySelector('[name="message"]').value.trim();
    const subject = encodeURIComponent(`AsriyyaMUN inquiry from ${name}`);
    const body = encodeURIComponent(`${message}\n\n— ${name} (${email})`);
    window.location.href = `mailto:info@asriyyamun.net?subject=${subject}&body=${body}`;
  });

  const photos = Array.from(document.querySelectorAll('main button[data-gallery-image]'));
  if (!photos.length) return;
  const dialog = document.createElement('dialog');
  dialog.className = 'photo-lightbox';
  dialog.setAttribute('aria-label', 'Conference photograph');
  dialog.innerHTML = '<button type="button" class="lightbox-close" aria-label="Close photograph">×</button><button type="button" class="lightbox-prev" aria-label="Previous photograph">‹</button><img class="lightbox-image" alt=""><button type="button" class="lightbox-next" aria-label="Next photograph">›</button><p class="lightbox-count" aria-live="polite"></p>';
  document.body.append(dialog);
  let index = 0;
  let opener;
  const show = next => {
    index = (next + photos.length) % photos.length;
    const source = photos[index].querySelector('img');
    const img = dialog.querySelector('img');
    img.src = source.src; img.alt = source.alt;
    dialog.querySelector('.lightbox-count').textContent = `${index + 1} / ${photos.length}`;
  };
  photos.forEach((button, i) => button.addEventListener('click', () => {
    opener = button; show(i); dialog.showModal(); document.body.style.overflow = 'hidden';
  }));
  dialog.querySelector('.lightbox-close').addEventListener('click', () => dialog.close());
  dialog.querySelector('.lightbox-prev').addEventListener('click', () => show(index - 1));
  dialog.querySelector('.lightbox-next').addEventListener('click', () => show(index + 1));
  dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
  dialog.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft') { event.preventDefault(); show(index - 1); }
    if (event.key === 'ArrowRight') { event.preventDefault(); show(index + 1); }
  });
  dialog.addEventListener('close', () => { document.body.style.overflow = ''; opener?.focus(); });
})();
