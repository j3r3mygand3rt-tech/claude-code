/* ==========================================================================
   La Beaute de Savin - Interaktion
   Vanilla JavaScript, keine Abhaengigkeiten, keine Build-Kette.
   Die Seite funktioniert vollstaendig ohne dieses Skript. Es ergaenzt nur
   Komfort: Menue, Eingangsanimationen, Formularpruefung.
   ========================================================================== */
(function () {
  'use strict';

  // Markiert, dass JavaScript laeuft. Erst dann werden Elemente fuer die
  // Eingangsanimation ausgeblendet, sonst blieben sie ohne JS unsichtbar.
  document.documentElement.classList.add('js');

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function on(el, evt, fn, opts) {
    if (el) el.addEventListener(evt, fn, opts);
  }

  /* ----------------------------------------------------------------------
     1. Kopfzeile: bekommt beim Scrollen eine Kante
     ---------------------------------------------------------------------- */
  var header = document.querySelector('.site-header');
  var actionBar = document.querySelector('.action-bar');
  var lastKnownY = 0;
  var ticking = false;

  function onScrollFrame() {
    var y = lastKnownY;

    if (header) {
      header.classList.toggle('is-stuck', y > 8);
    }

    // Die mobile Aktionsleiste erscheint erst, wenn der Hero-CTA
    // aus dem Blick ist. Vorher waere sie doppelt.
    if (actionBar) {
      actionBar.classList.toggle('is-visible', y > 420);
    }

    ticking = false;
  }

  function onScroll() {
    lastKnownY = window.scrollY || window.pageYOffset;
    if (!ticking) {
      // Scroll-Arbeit in den Frame verlegen, damit das Scrollen fluessig bleibt
      window.requestAnimationFrame(onScrollFrame);
      ticking = true;
    }
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  if (actionBar) {
    document.body.classList.add('has-action-bar');
  }

  /* ----------------------------------------------------------------------
     2. Mobiles Menue
     ---------------------------------------------------------------------- */
  var navToggle = document.querySelector('.nav-toggle');
  var mobileNav = document.getElementById('mobile-nav');
  var scrollLockY = 0;

  function setMenu(open) {
    if (!navToggle || !mobileNav) return;

    navToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    navToggle.setAttribute('aria-label', open ? 'Menü schließen' : 'Menü öffnen');
    mobileNav.classList.toggle('is-open', open);

    if (open) {
      // Hintergrund festhalten, ohne die Scrollposition zu verlieren
      scrollLockY = window.scrollY;
      document.body.style.position = 'fixed';
      document.body.style.top = '-' + scrollLockY + 'px';
      document.body.style.width = '100%';
    } else {
      document.body.style.position = '';
      document.body.style.top = '';
      document.body.style.width = '';
      window.scrollTo(0, scrollLockY);
    }
  }

  on(navToggle, 'click', function () {
    setMenu(navToggle.getAttribute('aria-expanded') !== 'true');
  });

  if (mobileNav) {
    mobileNav.addEventListener('click', function (e) {
      if (e.target.closest('a')) setMenu(false);
    });
  }

  on(document, 'keydown', function (e) {
    if (e.key === 'Escape' && navToggle && navToggle.getAttribute('aria-expanded') === 'true') {
      setMenu(false);
      navToggle.focus();
    }
  });

  // Wechselt der Nutzer auf Desktopbreite, darf kein gesperrter Body zurueckbleiben
  var desktopQuery = window.matchMedia('(min-width: 1024px)');
  var onBreakpoint = function (e) {
    if (e.matches) setMenu(false);
  };
  if (desktopQuery.addEventListener) {
    desktopQuery.addEventListener('change', onBreakpoint);
  } else if (desktopQuery.addListener) {
    desktopQuery.addListener(onBreakpoint);
  }

  /* ----------------------------------------------------------------------
     3. Eingangsanimationen
     ---------------------------------------------------------------------- */
  var revealTargets = document.querySelectorAll('[data-reveal], [data-reveal-group]');

  if (reduceMotion || !('IntersectionObserver' in window)) {
    // Kein Beobachter oder Nutzer moechte keine Bewegung: sofort sichtbar
    Array.prototype.forEach.call(revealTargets, function (el) {
      el.classList.add('is-in');
    });
  } else {
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          entry.target.classList.add('is-in');
          // Einmal eingeblendet bleibt eingeblendet. Wiederholtes
          // Ein- und Ausblenden beim Zurueckscrollen wirkt unruhig.
          observer.unobserve(entry.target);
        });
      },
      { rootMargin: '0px 0px -12% 0px', threshold: 0.08 }
    );

    Array.prototype.forEach.call(revealTargets, function (el) {
      observer.observe(el);
    });
  }

  /* ----------------------------------------------------------------------
     4. Aktiver Navigationspunkt beim Scrollen
     ---------------------------------------------------------------------- */
  var sections = document.querySelectorAll('main section[id]');
  var navLinks = document.querySelectorAll('.nav__link[href^="#"]');

  if (sections.length && navLinks.length && 'IntersectionObserver' in window) {
    var linkFor = {};
    Array.prototype.forEach.call(navLinks, function (link) {
      linkFor[link.getAttribute('href').slice(1)] = link;
    });

    var spy = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          var link = linkFor[entry.target.id];
          if (!link) return;
          if (entry.isIntersecting) {
            Array.prototype.forEach.call(navLinks, function (l) {
              l.removeAttribute('aria-current');
            });
            link.setAttribute('aria-current', 'page');
          }
        });
      },
      { rootMargin: '-45% 0px -50% 0px' }
    );

    Array.prototype.forEach.call(sections, function (s) {
      spy.observe(s);
    });
  }

  /* ----------------------------------------------------------------------
     5. Kontaktformular
     Ohne konfiguriertes Ziel (data-endpoint) wird eine vorbereitete
     E-Mail im Mailprogramm geoeffnet. Das funktioniert ohne Server.
     Mit data-endpoint wird stattdessen dorthin gesendet.
     ---------------------------------------------------------------------- */
  var form = document.querySelector('[data-contact-form]');

  if (form) {
    var status = form.querySelector('.form__status');

    var showError = function (field, message) {
      var box = field.parentNode.querySelector('.field__error');
      field.setAttribute('aria-invalid', 'true');
      if (box) {
        box.textContent = message;
        box.classList.add('is-visible');
      }
    };

    var clearError = function (field) {
      var box = field.parentNode.querySelector('.field__error');
      field.removeAttribute('aria-invalid');
      if (box) box.classList.remove('is-visible');
    };

    // Fehler verschwinden, sobald der Nutzer korrigiert
    Array.prototype.forEach.call(form.querySelectorAll('input, textarea, select'), function (f) {
      on(f, 'input', function () {
        clearError(f);
      });
    });

    var validate = function () {
      var firstBad = null;

      Array.prototype.forEach.call(form.querySelectorAll('[required]'), function (field) {
        var value = (field.value || '').trim();
        var bad = false;
        var message = 'Bitte ausfüllen.';

        if (field.type === 'checkbox') {
          bad = !field.checked;
          message = 'Bitte bestätigen Sie die Einwilligung.';
        } else if (!value) {
          bad = true;
        } else if (field.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(value)) {
          bad = true;
          message = 'Bitte prüfen Sie die E-Mail-Adresse.';
        }

        if (bad) {
          showError(field, message);
          if (!firstBad) firstBad = field;
        } else {
          clearError(field);
        }
      });

      return firstBad;
    };

    on(form, 'submit', function (e) {
      e.preventDefault();

      var firstBad = validate();
      if (firstBad) {
        firstBad.focus();
        return;
      }

      var data = new FormData(form);
      var endpoint = form.getAttribute('data-endpoint');

      var succeed = function () {
        if (status) {
          status.classList.add('is-visible');
          // Vorlesegeraete melden die Bestaetigung ueber role="status"
          status.focus();
        }
        form.reset();
      };

      if (endpoint) {
        var button = form.querySelector('button[type="submit"]');
        if (button) button.disabled = true;

        fetch(endpoint, { method: 'POST', body: data, headers: { Accept: 'application/json' } })
          .then(function (res) {
            if (!res.ok) throw new Error('Status ' + res.status);
            succeed();
          })
          .catch(function () {
            if (status) {
              status.textContent =
                'Das Formular konnte nicht gesendet werden. Bitte rufen Sie uns an unter 040 41 46 68 49.';
              status.classList.add('is-visible');
            }
          })
          .finally(function () {
            if (button) button.disabled = false;
          });
        return;
      }

      // Kein Server hinterlegt: vorbereitete E-Mail oeffnen
      var lines = [
        'Name: ' + (data.get('name') || ''),
        'E-Mail: ' + (data.get('email') || ''),
        'Telefon: ' + (data.get('phone') || ''),
        'Wunschleistung: ' + (data.get('service') || ''),
        '',
        (data.get('message') || '')
      ];

      window.location.href =
        'mailto:elena@labeaute-savin.de' +
        '?subject=' + encodeURIComponent('Terminanfrage über die Website') +
        '&body=' + encodeURIComponent(lines.join('\n'));

      succeed();
    });
  }

  /* ----------------------------------------------------------------------
     6. Jahreszahl in der Fusszeile
     ---------------------------------------------------------------------- */
  var year = document.querySelector('[data-year]');
  if (year) year.textContent = String(new Date().getFullYear());
})();
