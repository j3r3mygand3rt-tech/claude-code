/*
 * Hintergrund: weiche, langsam wandernde Farbverläufe in den Blautönen
 * des Logos. Reines WebGL, es wird nichts von fremden Servern geladen.
 * Weil das Bild ohnehin unscharf ist, wird es in geringer Auflösung
 * berechnet und vom Browser hochskaliert – das schont Akku und Grafikkarte.
 */
(function () {
  "use strict";

  var huelle = document.querySelector(".hintergrund");
  if (!huelle) return;

  var canvas = document.createElement("canvas");
  canvas.setAttribute("aria-hidden", "true");
  var gl = canvas.getContext("webgl", { antialias: false, alpha: false, powerPreference: "low-power" }) ||
           canvas.getContext("experimental-webgl");
  // Ohne WebGL bleibt der CSS-Farbverlauf als Hintergrund stehen.
  if (!gl) return;

  var vertexQuelle =
    "attribute vec2 position;" +
    "void main() { gl_Position = vec4(position, 0.0, 1.0); }";

  var fragmentQuelle = [
    "precision mediump float;",
    "uniform vec2 resolution;",
    "uniform float time;",
    "",
    "vec3 fleck(vec2 p, vec2 mitte, float radius, vec3 farbe) {",
    "  vec2 d = p - mitte;",
    "  return farbe * exp(-dot(d, d) / (radius * radius));",
    "}",
    "",
    "float rauschen(vec2 st) {",
    "  return fract(sin(dot(st, vec2(12.9898, 78.233))) * 43758.5453);",
    "}",
    "",
    "void main(void) {",
    "  float seite = resolution.x / resolution.y;",
    "  vec2 p = gl_FragCoord.xy / resolution.xy;",
    "  p.x *= seite;",
    "  float t = time;",
    "",
    // Farben: Grund #070b14, Himmelblau #38BDF8, Blau #0EA5E9, Königsblau, Petrol
    "  vec3 farbe = vec3(0.027, 0.043, 0.078);",
    // Jeder Fleck wandert quer über die ganze Breite (etwas über den Rand hinaus)
    // und wieder zurück. Eigene Dauer und eigener Startpunkt je Fleck, damit
    // sie nie im Gleichtakt laufen: ca. 38 s, 52 s, 67 s und 83 s pro Durchgang.
    "  farbe += fleck(p, vec2(seite * (0.5 + 0.62 * sin(t * 0.165)),        0.32 + 0.14 * sin(t * 0.090 + 1.0)), 0.42, vec3(0.22, 0.74, 0.97) * 0.30);",
    "  farbe += fleck(p, vec2(seite * (0.5 + 0.62 * sin(t * 0.121 + 2.4)),  0.64 + 0.12 * cos(t * 0.070)),       0.48, vec3(0.05, 0.53, 0.91) * 0.28);",
    "  farbe += fleck(p, vec2(seite * (0.5 + 0.62 * cos(t * 0.094 + 4.1)),  0.18 + 0.12 * sin(t * 0.110 + 2.0)), 0.40, vec3(0.14, 0.26, 0.78) * 0.26);",
    "  farbe += fleck(p, vec2(seite * (0.5 + 0.62 * sin(t * 0.076 + 5.3)),  0.86 + 0.10 * cos(t * 0.080 + 0.5)), 0.36, vec3(0.03, 0.45, 0.60) * 0.22);",
    "",
    // Leichtes Rauschen verhindert Farbstufen in den Verläufen
    "  farbe += (rauschen(gl_FragCoord.xy + t) - 0.5) / 255.0 * 2.0;",
    "  gl_FragColor = vec4(farbe, 1.0);",
    "}"
  ].join("\n");

  function shader(typ, quelle) {
    var s = gl.createShader(typ);
    gl.shaderSource(s, quelle);
    gl.compileShader(s);
    if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) {
      gl.deleteShader(s);
      return null;
    }
    return s;
  }

  var vs = shader(gl.VERTEX_SHADER, vertexQuelle);
  var fs = shader(gl.FRAGMENT_SHADER, fragmentQuelle);
  if (!vs || !fs) return;

  var programm = gl.createProgram();
  gl.attachShader(programm, vs);
  gl.attachShader(programm, fs);
  gl.linkProgram(programm);
  if (!gl.getProgramParameter(programm, gl.LINK_STATUS)) return;
  gl.useProgram(programm);

  // Ein Rechteck über die ganze Fläche (zwei Dreiecke)
  var puffer = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, puffer);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, -1, 1, 1, -1, 1, 1]), gl.STATIC_DRAW);
  var position = gl.getAttribLocation(programm, "position");
  gl.enableVertexAttribArray(position);
  gl.vertexAttribPointer(position, 2, gl.FLOAT, false, 0, 0);

  var uZeit = gl.getUniformLocation(programm, "time");
  var uAufloesung = gl.getUniformLocation(programm, "resolution");

  huelle.appendChild(canvas);

  var MASSSTAB = 0.25; // Rechenauflösung: ein Viertel der Fenstergröße

  function groesse() {
    var b = Math.max(1, Math.round(huelle.clientWidth * MASSSTAB));
    var h = Math.max(1, Math.round(huelle.clientHeight * MASSSTAB));
    if (canvas.width !== b || canvas.height !== h) {
      canvas.width = b;
      canvas.height = h;
      gl.viewport(0, 0, b, h);
    }
    gl.uniform2f(uAufloesung, b, h);
  }

  var start = 0;
  var versatz = 20; // Startbild mit gut verteilten Farbflecken
  var laeuft = false;
  var ruhig = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)");

  function zeichnen(sekunden) {
    gl.uniform1f(uZeit, versatz + sekunden);
    gl.drawArrays(gl.TRIANGLES, 0, 6);
  }

  var letzteSekunden = 0;
  var letztesBild = 0;
  function schritt(jetzt) {
    if (!laeuft) return;
    if (!start) start = jetzt - letzteSekunden * 1000;
    // Die Bewegung ist sehr langsam – 30 Bilder pro Sekunde genügen
    if (jetzt - letztesBild >= 33) {
      letztesBild = jetzt;
      letzteSekunden = (jetzt - start) / 1000;
      zeichnen(letzteSekunden);
    }
    window.requestAnimationFrame(schritt);
  }

  function starten() {
    if (laeuft || document.hidden || (ruhig && ruhig.matches)) return;
    laeuft = true;
    start = 0;
    window.requestAnimationFrame(schritt);
  }

  function anhalten() { laeuft = false; }

  groesse();
  zeichnen(0);   // Standbild, auch bei reduzierter Bewegung
  starten();

  window.addEventListener("resize", function () { groesse(); zeichnen(letzteSekunden); });
  document.addEventListener("visibilitychange", function () {
    if (document.hidden) anhalten(); else starten();
  });
  if (ruhig && ruhig.addEventListener) {
    ruhig.addEventListener("change", function () {
      if (ruhig.matches) anhalten(); else starten();
    });
  }
})();
