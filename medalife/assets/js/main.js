/* MEDALIFE, Gesundheitszentrum Hamburg Gross Borstel
   Vier Aufgaben: Menue, Eingangsanimation, Aktionsleiste, Formularpruefung.
   Kein Framework, keine Abhaengigkeit. Ohne JavaScript bleibt die Seite
   vollstaendig lesbar und bedienbar.                                        */
(function () {
  'use strict';

  var root = document.documentElement;
  root.classList.add('js');

  var sanft = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------------------------------------------------------------- Menue */
  var schalter = document.querySelector('.nav-toggle');
  var schublade = document.getElementById('menu');

  if (schalter && schublade) {
    var umschalten = function (offen) {
      schalter.setAttribute('aria-expanded', String(offen));
      schublade.classList.toggle('is-open', offen);
      schalter.setAttribute(
        'aria-label',
        offen ? 'Menü schließen' : 'Menü öffnen'
      );
      document.body.style.overflow = offen ? 'hidden' : '';
    };

    schalter.addEventListener('click', function () {
      umschalten(schalter.getAttribute('aria-expanded') !== 'true');
    });

    schublade.addEventListener('click', function (e) {
      if (e.target.closest('a')) umschalten(false);
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && schalter.getAttribute('aria-expanded') === 'true') {
        umschalten(false);
        schalter.focus();
      }
    });

    /* Beim Wechsel auf die Breitbildnavigation darf kein offenes Menue
       zurueckbleiben, sonst bleibt der Scroll gesperrt. */
    var breit = window.matchMedia('(min-width: 1024px)');
    var aufBreit = function (m) {
      if (m.matches) umschalten(false);
    };
    if (breit.addEventListener) breit.addEventListener('change', aufBreit);
    else if (breit.addListener) breit.addListener(aufBreit);
  }

  /* -------------------------------------------------------- Eingaenge */
  var ziele = document.querySelectorAll('[data-reveal], [data-reveal-group]');

  if (!('IntersectionObserver' in window) || sanft) {
    Array.prototype.forEach.call(ziele, function (el) {
      el.classList.add('is-in');
    });
  } else {
    var beobachter = new IntersectionObserver(
      function (eintraege) {
        eintraege.forEach(function (e) {
          if (!e.isIntersecting) return;
          e.target.classList.add('is-in');
          beobachter.unobserve(e.target);
        });
      },
      { rootMargin: '0px 0px -8% 0px', threshold: 0.08 }
    );
    Array.prototype.forEach.call(ziele, function (el) {
      beobachter.observe(el);
    });
  }

  /* --------------------------------------------------- Aktionsleiste */
  var leiste = document.querySelector('.dock');

  if (leiste) {
    document.body.classList.add('has-dock');
    var letzte = 0;
    var geplant = false;

    var pruefen = function () {
      geplant = false;
      var y = window.pageYOffset || root.scrollTop;
      /* Erst nach einer knappen Bildschirmhoehe einblenden, damit die Leiste
         den ersten Eindruck nicht ueberdeckt. Beim Hochscrollen bleibt sie. */
      var zeigen = y > 320 || (y > 120 && y < letzte);
      leiste.classList.toggle('is-visible', zeigen);
      letzte = y;
    };

    window.addEventListener(
      'scroll',
      function () {
        if (geplant) return;
        geplant = true;
        window.requestAnimationFrame(pruefen);
      },
      { passive: true }
    );
    pruefen();
  }

  /* ------------------------------------------------------- Formular */
  var formular = document.querySelector('form[data-pruefen]');

  if (formular) {
    var meldung = formular.querySelector('.form-status');

    var fehlerZeigen = function (feld, text) {
      var kasten = document.getElementById(feld.id + '-fehler');
      feld.setAttribute('aria-invalid', 'true');
      if (kasten) {
        kasten.textContent = text;
        kasten.classList.add('is-visible');
      }
    };

    var fehlerLoeschen = function (feld) {
      var kasten = document.getElementById(feld.id + '-fehler');
      feld.removeAttribute('aria-invalid');
      if (kasten) kasten.classList.remove('is-visible');
    };

    var pruefeFeld = function (feld) {
      if (feld.type === 'checkbox') {
        if (feld.required && !feld.checked) {
          fehlerZeigen(feld, 'Bitte bestätigen Sie die Datenschutzhinweise.');
          return false;
        }
        fehlerLoeschen(feld);
        return true;
      }
      var wert = feld.value.trim();
      if (feld.required && !wert) {
        fehlerZeigen(feld, 'Dieses Feld brauchen wir für Ihre Anfrage.');
        return false;
      }
      if (feld.type === 'email' && wert && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(wert)) {
        fehlerZeigen(feld, 'Bitte prüfen Sie die E-Mail-Adresse.');
        return false;
      }
      if (feld.type === 'tel' && wert && wert.replace(/[^\d]/g, '').length < 6) {
        fehlerZeigen(feld, 'Bitte geben Sie eine erreichbare Nummer an.');
        return false;
      }
      fehlerLoeschen(feld);
      return true;
    };

    var felder = formular.querySelectorAll('input, select, textarea');

    Array.prototype.forEach.call(felder, function (feld) {
      feld.addEventListener('blur', function () {
        if (feld.value || feld.type === 'checkbox') pruefeFeld(feld);
      });
      feld.addEventListener('input', function () {
        if (feld.getAttribute('aria-invalid') === 'true') pruefeFeld(feld);
      });
    });

    formular.addEventListener('submit', function (e) {
      e.preventDefault();
      var erster = null;

      Array.prototype.forEach.call(felder, function (feld) {
        if (!pruefeFeld(feld) && !erster) erster = feld;
      });

      if (erster) {
        erster.focus();
        return;
      }

      /* Diese Vorschau verschickt nichts. Der Versand braucht ein Skript auf
         dem Server des Hosters, das die Anfrage an info@medalife.de weiterleitet. */
      if (meldung) {
        meldung.classList.add('is-visible');
        meldung.focus();
      }
      formular.reset();
      Array.prototype.forEach.call(felder, fehlerLoeschen);
    });
  }
})();
