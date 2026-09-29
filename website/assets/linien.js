/*
 * Hintergrund "Shader-Linien"
 * Derselbe Fragment-Shader wie die React-Komponente ShaderAnimation,
 * hier ohne React und ohne Three.js direkt in WebGL umgesetzt.
 * Es wird nichts von fremden Servern geladen.
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
    "precision highp float;",
    "uniform vec2 resolution;",
    "uniform float time;",
    "float random(in float x) { return fract(sin(x) * 1e4); }",
    "void main(void) {",
    "  vec2 uv = (gl_FragCoord.xy * 2.0 - resolution.xy) / min(resolution.x, resolution.y);",
    "  vec2 fMosaicScal = vec2(4.0, 2.0);",
    "  vec2 vScreenSize = vec2(256.0, 256.0);",
    "  uv.x = floor(uv.x * vScreenSize.x / fMosaicScal.x) / (vScreenSize.x / fMosaicScal.x);",
    "  uv.y = floor(uv.y * vScreenSize.y / fMosaicScal.y) / (vScreenSize.y / fMosaicScal.y);",
    "  float t = time * 0.06 + random(uv.x) * 0.4;",
    "  float lineWidth = 0.0008;",
    "  vec3 color = vec3(0.0);",
    "  for (int j = 0; j < 3; j++) {",
    "    for (int i = 0; i < 5; i++) {",
    "      color[j] += lineWidth * float(i * i) / abs(fract(t - 0.01 * float(j) + float(i) * 0.01) * 1.0 - length(uv));",
    "    }",
    "  }",
    "  gl_FragColor = vec4(color[2], color[1], color[0], 1.0);",
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

  function groesse() {
    // Pixeldichte begrenzen: der Shader rechnet ohnehin mosaikartig
    var dichte = Math.min(window.devicePixelRatio || 1, 1.5);
    var b = Math.round(huelle.clientWidth * dichte);
    var h = Math.round(huelle.clientHeight * dichte);
    if (canvas.width !== b || canvas.height !== h) {
      canvas.width = b;
      canvas.height = h;
      gl.viewport(0, 0, b, h);
    }
    gl.uniform2f(uAufloesung, b, h);
  }

  var zeit = 1.0;
  var letzte = 0;
  var laeuft = false;
  var ruhig = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)");

  function zeichnen() {
    gl.uniform1f(uZeit, zeit);
    gl.drawArrays(gl.TRIANGLES, 0, 6);
  }

  function schritt(jetzt) {
    if (!laeuft) return;
    // Wie im Original +0.05 pro Bild, bezogen auf 60 Bilder pro Sekunde
    var delta = letzte ? Math.min((jetzt - letzte) / 16.667, 4) : 1;
    letzte = jetzt;
    zeit += 0.05 * delta;
    zeichnen();
    window.requestAnimationFrame(schritt);
  }

  function starten() {
    if (laeuft || document.hidden || (ruhig && ruhig.matches)) return;
    laeuft = true;
    letzte = 0;
    window.requestAnimationFrame(schritt);
  }

  function anhalten() { laeuft = false; }

  groesse();
  zeit = 8.0;   // Startbild mit gut verteilten Ringen
  zeichnen();   // Standbild, auch bei reduzierter Bewegung
  starten();

  window.addEventListener("resize", function () { groesse(); zeichnen(); });
  document.addEventListener("visibilitychange", function () {
    if (document.hidden) anhalten(); else starten();
  });
  if (ruhig && ruhig.addEventListener) {
    ruhig.addEventListener("change", function () {
      if (ruhig.matches) anhalten(); else starten();
    });
  }
})();
