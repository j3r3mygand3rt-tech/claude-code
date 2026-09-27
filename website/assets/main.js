(function () {
  "use strict";

  /* ---------- Mobilmenü ---------- */

  var knopf = document.querySelector(".nav__knopf");
  var menue = document.getElementById("menue");

  function menueSchliessen(fokusZurueck) {
    if (!menue.classList.contains("ist-offen")) return;
    menue.classList.remove("ist-offen");
    knopf.setAttribute("aria-expanded", "false");
    knopf.setAttribute("aria-label", "Menü öffnen");
    if (fokusZurueck) knopf.focus();
  }

  if (knopf && menue) {
    knopf.addEventListener("click", function () {
      var offen = menue.classList.toggle("ist-offen");
      knopf.setAttribute("aria-expanded", offen ? "true" : "false");
      knopf.setAttribute("aria-label", offen ? "Menü schließen" : "Menü öffnen");
    });

    menue.addEventListener("click", function (e) {
      if (e.target.closest("a")) menueSchliessen(false);
    });

    menue.addEventListener("keydown", function (e) {
      if (e.key === "Escape") menueSchliessen(true);
    });
    knopf.addEventListener("keydown", function (e) {
      if (e.key === "Escape") menueSchliessen(true);
    });
  }

  /* ---------- Paket-Knöpfe füllen das Formular vor ---------- */

  var auswahl = document.getElementById("f-paket");
  document.querySelectorAll("[data-paket]").forEach(function (link) {
    link.addEventListener("click", function () {
      if (auswahl) auswahl.value = link.getAttribute("data-paket");
    });
  });

  /* ---------- Kontaktformular ---------- */

  var formular = document.getElementById("anfrage");
  if (!formular) return;

  var meldung = formular.querySelector(".formular__meldung");
  var absenden = formular.querySelector('button[type="submit"]');

  function zeigen(text, art) {
    meldung.textContent = text;
    meldung.className = "formular__meldung formular__meldung--" + art;
    meldung.hidden = false;
  }

  function pruefen() {
    var felder = [
      { el: formular.elements.name, text: "Bitte geben Sie Ihren Namen an." },
      { el: formular.elements.email, text: "Bitte geben Sie eine gültige E-Mail-Adresse an." },
      { el: formular.elements.nachricht, text: "Bitte schreiben Sie kurz, worum es geht." },
      { el: formular.elements.einwilligung, text: "Bitte bestätigen Sie die Einwilligung zur Datenverarbeitung." }
    ];
    for (var i = 0; i < felder.length; i++) {
      if (!felder[i].el.checkValidity()) {
        zeigen(felder[i].text, "fehler");
        felder[i].el.focus();
        return false;
      }
    }
    return true;
  }

  formular.addEventListener("submit", function (e) {
    e.preventDefault();
    if (!pruefen()) return;

    // In der Vorschau (ohne Server) wird nichts verschickt.
    if (window.GANDERT_VORSCHAU) {
      zeigen("Vorschau: Auf der echten Website wird die Anfrage jetzt per E-Mail verschickt.", "ok");
      return;
    }

    absenden.disabled = true;
    absenden.textContent = "Wird gesendet …";

    fetch(formular.action, {
      method: "POST",
      body: new FormData(formular),
      headers: { Accept: "application/json" }
    })
      .then(function (antwort) {
        return antwort.json().catch(function () { return { ok: false }; });
      })
      .then(function (daten) {
        if (daten.ok) {
          formular.reset();
          zeigen("Danke für Ihre Anfrage. Ich melde mich innerhalb von zwei Werktagen bei Ihnen.", "ok");
        } else {
          zeigen(daten.fehler || "Die Anfrage konnte nicht gesendet werden. Bitte rufen Sie mich an oder schreiben Sie mir eine E-Mail.", "fehler");
        }
      })
      .catch(function () {
        zeigen("Die Verbindung ist fehlgeschlagen. Bitte versuchen Sie es erneut oder schreiben Sie mir eine E-Mail.", "fehler");
      })
      .then(function () {
        absenden.disabled = false;
        absenden.textContent = "Anfrage senden";
      });
  });
})();
