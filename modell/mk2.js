/* 3D-Modell des britischen Panzers Mark II für die Seite panzer.html.
   Geometrie übernommen aus dem claude.ai-Entwurf „Mark II Panzer 3D“ (18.11.2026),
   Steuerung und Farben nach dem Muster des Fokker-Dr.I-Modells im Repo erster-Weltkrieg.
   Benötigt modell/vendor/three-0.159.0.min.js (MIT-Lizenz, siehe three-LICENSE.txt). */
(function () {
  "use strict";
  const box = document.getElementById("mk2");
  if (!box) return;
  const cv = box.querySelector("canvas");
  const msg = box.querySelector(".mk2-msg");
  const reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const state = { spin: !reduce, tracks: !reduce, version: "male" };
  const VIEWS = {
    drei: { theta: 0.75, phi: 1.2, dist: 14 },
    seite: { theta: 0.0, phi: 1.52, dist: 13 },
    vorne: { theta: Math.PI / 2, phi: 1.42, dist: 11.5 },
    oben: { theta: 0.0, phi: 0.06, dist: 15 },
    heck: { theta: -2.3, phi: 1.2, dist: 13.5 },
    unten: { theta: 0.6, phi: 2.2, dist: 13.5 }
  };
  const c = { theta: 0.75, phi: 1.2, dist: 14, tTheta: 0.75, tPhi: 1.2, tDist: 14 };
  function fail(text) { if (msg) { msg.textContent = text; msg.hidden = false; } }
  const T = window.THREE;
  if (!T) { fail("Das 3D-Modell konnte nicht geladen werden."); return; }
  let renderer;
  try { renderer = new T.WebGLRenderer({ canvas: cv, antialias: true }); }
  catch (e) { fail("WebGL ist in diesem Browser nicht verfügbar."); return; }
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = T.PCFSoftShadowMap;
  renderer.toneMapping = T.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.05;

  const scene = new T.Scene();
  scene.background = new T.Color(0x181d1a);
  scene.fog = new T.Fog(0x181d1a, 26, 55);
  const cam = new T.PerspectiveCamera(32, 1, 0.1, 150);

  const hemi = new T.HemisphereLight(0xdfe8f5, 0x3a2f28, 0.9);
  scene.add(hemi);
  const key = new T.DirectionalLight(0xfff1dc, 2.4);
  key.position.set(7, 14, 9);
  key.castShadow = true;
  key.shadow.mapSize.set(2048, 2048);
  const sc = key.shadow.camera;
  sc.left = -8; sc.right = 8; sc.top = 8; sc.bottom = -8; sc.near = 1; sc.far = 40;
  key.shadow.bias = -0.0005;
  key.shadow.normalBias = 0.02;
  scene.add(key);
  const fill = new T.DirectionalLight(0x9fb4d0, 0.55);
  fill.position.set(-8, 4, -6);
  scene.add(fill);

  const groundMat = new T.MeshStandardMaterial({ color: 0x22272d, roughness: 1 });
  const ground = new T.Mesh(new T.CircleGeometry(18, 96), groundMat);
  ground.rotation.x = -Math.PI / 2;
  ground.receiveShadow = true;
  scene.add(ground);
  const ringMat = new T.MeshBasicMaterial({ color: 0x353b43 });
  const ring = new T.Mesh(new T.RingGeometry(6.9, 6.94, 128), ringMat);
  ring.rotation.x = -Math.PI / 2; ring.position.y = 0.002;
  scene.add(ring);

      const std = (c, r, m, extra) => new T.MeshStandardMaterial(Object.assign({ color: c, roughness: r, metalness: m || 0 }, extra || {}));
      const mats = {
        hull: std(0x6e5b3e, 0.78, 0.15),
        track: std(0x3b3631, 0.8, 0.55),
        black: std(0x1b1c1e, 0.5, 0.6),
        metal: std(0x7d7a74, 0.4, 0.75),
        wood: std(0x6b4a2b, 0.75, 0),
        dark: std(0x0c0c0d, 0.9, 0, { side: T.DoubleSide })
      };
  
      const add = (parent, geo, mat) => {
        const m = new T.Mesh(geo, mat);
        m.castShadow = true; m.receiveShadow = true;
        parent.add(m);
        return m;
      };
      const rod = (parent, a, b, r, mat) => {
        const A = new T.Vector3(a[0], a[1], a[2]);
        const B = new T.Vector3(b[0], b[1], b[2]);
        const d = B.clone().sub(A);
        const m = add(parent, new T.CylinderGeometry(r, r, d.length(), 12), mat);
        m.position.copy(A).add(B).multiplyScalar(0.5);
        m.quaternion.setFromUnitVectors(new T.Vector3(0, 1, 0), d.normalize());
        return m;
      };
  
      const tank = new T.Group();
  
      // Rautenprofil der Seitenrahmen (x: vorn +, y: oben), Gesamtlänge 8,05 m
      const outline = new T.Shape();
      outline.moveTo(1.4, 0);
      outline.lineTo(-1.9, 0);
      outline.lineTo(-3.5, 0.75);
      outline.quadraticCurveTo(-4.0, 1.0, -3.95, 1.5);
      outline.quadraticCurveTo(-3.9, 2.22, -3.3, 2.3);
      outline.lineTo(3.0, 2.42);
      outline.quadraticCurveTo(4.05, 2.44, 4.0, 1.75);
      outline.quadraticCurveTo(3.95, 1.3, 3.6, 1.1);
      outline.lineTo(1.4, 0);
  
      // Polylinie für Kettenglieder und Nietreihen
      const raw = outline.getSpacedPoints(700);
      const pts = raw.map((p) => [p.x, p.y]);
      if (Math.hypot(pts[0][0] - pts[pts.length - 1][0], pts[0][1] - pts[pts.length - 1][1]) > 1e-4) pts.push(pts[0].slice());
      const cum = [0];
      for (let i = 1; i < pts.length; i++) cum.push(cum[i - 1] + Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]));
      const L = cum[cum.length - 1];
      const at = (d) => {
        d = ((d % L) + L) % L;
        let lo = 0, hi = cum.length - 1;
        while (hi - lo > 1) { const mid = (lo + hi) >> 1; if (cum[mid] <= d) lo = mid; else hi = mid; }
        const a = pts[lo], b = pts[hi];
        const seg = cum[hi] - cum[lo] || 1;
        const f = (d - cum[lo]) / seg;
        const tx = (b[0] - a[0]) / seg, ty = (b[1] - a[1]) / seg;
        return { x: a[0] + (b[0] - a[0]) * f, y: a[1] + (b[1] - a[1]) * f, tx, ty, nx: -ty, ny: tx };
      };
  
      // Seitenrahmen (rechts/links)
      const FZ0 = 1.06, FZ1 = 1.54, TZ = 1.3;
      const frameG = new T.ExtrudeGeometry(outline, { depth: FZ1 - FZ0, bevelEnabled: false, curveSegments: 24 });
      [1, -1].forEach((s) => {
        const m = add(tank, frameG, mats.hull);
        m.position.z = s > 0 ? FZ0 : -FZ1;
      });
  
      // Nietreihen an den Außenflächen
      const rivG = new T.SphereGeometry(0.02, 6, 4);
      const rivPos = [];
      for (let d = 0; d < L; d += 0.2) { const p = at(d); rivPos.push([p.x - p.nx * 0.13, p.y - p.ny * 0.13]); }
      [-3.0, -1.6, 0.0, 1.6, 2.4].forEach((x) => { for (let y = 0.65; y < 2.2; y += 0.2) rivPos.push([x, y]); });
      const rivets = new T.InstancedMesh(rivG, mats.hull, rivPos.length * 2);
      const dm = new T.Object3D();
      let ri = 0;
      [1, -1].forEach((s) => {
        rivPos.forEach((p) => {
          dm.position.set(p[0], p[1], s * (FZ1 + 0.004));
          dm.rotation.set(0, 0, 0);
          dm.updateMatrix();
          rivets.setMatrixAt(ri++, dm.matrix);
        });
      });
      rivets.castShadow = true;
      tank.add(rivets);
  
      // Ketten: umlaufende Glieder, animierbar
      const NP = 90;
      const plateG = new T.BoxGeometry(L / NP * 0.86, 0.06, 0.54);
      const trackL = new T.InstancedMesh(plateG, mats.track, NP);
      const trackR = new T.InstancedMesh(plateG, mats.track, NP);
      trackL.castShadow = trackR.castShadow = true;
      trackL.receiveShadow = trackR.receiveShadow = true;
      tank.add(trackL); tank.add(trackR);
      const placeTracks = (off) => {
        for (let i = 0; i < NP; i++) {
          const p = at(off + i * L / NP);
          dm.rotation.set(0, 0, Math.atan2(p.ty, p.tx));
          [[trackR, TZ], [trackL, -TZ]].forEach((e) => {
            dm.position.set(p.x + p.nx * 0.03, p.y + p.ny * 0.03, e[1]);
            dm.updateMatrix();
            e[0].setMatrixAt(i, dm.matrix);
          });
        }
        trackL.instanceMatrix.needsUpdate = true;
        trackR.instanceMatrix.needsUpdate = true;
      };
      let trackOff = 0;
      placeTracks(trackOff);
  
      // Mittelrumpf zwischen den Rahmen
      const body = add(tank, new T.BoxGeometry(5.7, 1.66, FZ0 * 2), mats.hull);
      body.position.set(-0.35, 1.53, 0);
  
      // Fahrerhaus vorn mit Bugplatte
      {
        const sh = new T.Shape();
        sh.moveTo(2.3, 0.7);
        sh.lineTo(2.75, 0.95);
        sh.lineTo(3.3, 1.45);
        sh.lineTo(3.3, 2.05);
        sh.lineTo(3.15, 2.52);
        sh.lineTo(2.3, 2.52);
        sh.closePath();
        const g = new T.ExtrudeGeometry(sh, { depth: 1.7, bevelEnabled: false });
        g.translate(0, 0, -0.85);
        add(tank, g, mats.hull);
        [-0.45, -0.18, 0.18, 0.45].forEach((z) => {
          const sl = add(tank, new T.BoxGeometry(0.02, 0.04, 0.16), mats.dark);
          sl.position.set(3.305, 1.88, z);
        });
        const hatch = add(tank, new T.BoxGeometry(0.5, 0.06, 0.6), mats.hull);
        hatch.position.set(2.7, 2.55, 0);
        const ball = add(tank, new T.SphereGeometry(0.1, 16, 12), mats.black);
        ball.position.set(3.3, 1.62, 0);
        const mg = add(tank, new T.CylinderGeometry(0.04, 0.04, 0.45, 14), mats.black);
        mg.rotation.z = Math.PI / 2;
        mg.position.set(3.5, 1.62, 0);
      }
  
      // Offener Auspuff auf dem Dach (ohne Schalldämpfer, angenähert)
      [0.3, -0.3].forEach((z) => {
        rod(tank, [-0.6, 2.36, z], [-0.6, 2.62, z], 0.05, mats.black);
        rod(tank, [-0.6, 2.62, z], [-1.3, 2.62, z], 0.05, mats.black);
      });
      // Lüftungshaube auf dem Dach
      const vent = add(tank, new T.BoxGeometry(0.7, 0.12, 0.9), mats.hull);
      vent.position.set(-2.2, 2.42, 0);
  
      // Sponsons
      const sponson = (plan, y0, y1) => {
        const sh = new T.Shape();
        sh.moveTo(plan[0][0], plan[0][1]);
        for (let i = 1; i < plan.length; i++) sh.lineTo(plan[i][0], plan[i][1]);
        sh.closePath();
        const g = new T.ExtrudeGeometry(sh, { depth: y1 - y0, bevelEnabled: false });
        g.rotateX(Math.PI / 2);
        g.translate(0, y1, 0);
        return g;
      };
      const faceMount = (grp, a, b, y) => {
        const mx = (a[0] + b[0]) / 2, mz = (a[1] + b[1]) / 2;
        let nx = b[1] - a[1], nz = -(b[0] - a[0]);
        const len = Math.hypot(nx, nz); nx /= len; nz /= len;
        if (nx * mx < 0 && Math.abs(mx) > 0.01) { nx = -nx; nz = -nz; }
        if (nz < 0) { nx = -nx; nz = -nz; }
        const g = new T.Group();
        g.position.set(mx, y, mz);
        g.rotation.y = -Math.atan2(nz, nx);
        grp.add(g);
        return g;
      };
      const lewis = (g) => {
        add(g, new T.SphereGeometry(0.1, 16, 12), mats.black);
        const jacket = add(g, new T.CylinderGeometry(0.045, 0.045, 0.45, 14), mats.black);
        jacket.rotation.z = -Math.PI / 2;
        jacket.position.x = 0.26;
        const muzzle = add(g, new T.CylinderGeometry(0.015, 0.015, 0.08, 8), mats.metal);
        muzzle.rotation.z = -Math.PI / 2;
        muzzle.position.x = 0.52;
      };
  
      const vickers = (g) => {
        add(g, new T.SphereGeometry(0.1, 16, 12), mats.black);
        const jacket = add(g, new T.CylinderGeometry(0.065, 0.065, 0.5, 16), mats.metal);
        jacket.rotation.z = -Math.PI / 2;
        jacket.position.x = 0.3;
        const muzzle = add(g, new T.CylinderGeometry(0.025, 0.03, 0.1, 10), mats.black);
        muzzle.rotation.z = -Math.PI / 2;
        muzzle.position.x = 0.6;
      };
  
      const spMale = new T.Group();
      const spFemale = new T.Group();
      [1, -1].forEach((s) => {
        // Male: 6-Pfünder vorn, MG hinten
        const mg = new T.Group();
        const pm = [[-0.95, 0], [1.05, 0], [0.72, 0.47], [-0.6, 0.47]];
        add(mg, sponson(pm, 0.55, 1.68), mats.hull);
        const gun = faceMount(mg, pm[1], pm[2], 1.12);
        const mant = add(gun, new T.CylinderGeometry(0.17, 0.17, 0.22, 20), mats.hull);
        mant.rotation.z = -Math.PI / 2;
        mant.position.x = 0.06;
        const shield = add(gun, new T.BoxGeometry(0.06, 0.5, 0.42), mats.hull);
        shield.position.x = 0.0;
        const barrel = add(gun, new T.CylinderGeometry(0.045, 0.055, 2.28, 18), mats.black);
        barrel.rotation.z = -Math.PI / 2;
        barrel.position.x = 1.28;
        const rear = faceMount(mg, pm[3], pm[0], 1.12);
        lewis(rear);
        const door = add(mg, new T.BoxGeometry(0.5, 0.75, 0.02), mats.hull);
        door.position.set(0.1, 1.1, 0.475);
        mg.position.z = s * FZ1;
        mg.scale.z = s;
        spMale.add(mg);
  
        // Female: größere Erker mit zwei MGs
        const fg = new T.Group();
        const pf = [[-0.9, 0], [0.9, 0], [0.62, 0.33], [-0.62, 0.33]];
        add(fg, sponson(pf, 0.45, 1.8), mats.hull);
        const f1 = faceMount(fg, pf[1], pf[2], 1.25);
        vickers(f1);
        const f2 = faceMount(fg, pf[3], pf[0], 1.25);
        vickers(f2);
        const fd = add(fg, new T.BoxGeometry(0.5, 0.8, 0.02), mats.hull);
        fd.position.set(0, 1.0, 0.335);
        fg.position.z = s * FZ1;
        fg.scale.z = s;
        spFemale.add(fg);
      });
      tank.add(spMale); tank.add(spFemale);
  
      spMale.visible = state.version === "male";
      spFemale.visible = state.version === "female";
  
      tank.position.y = 0.06;
      tank.scale.x = 7.92 / 8.05;
      scene.add(tank);

  const target = new T.Vector3(0, 1.25, 0);

  /* Farben aus dem Seitenschema (hell/dunkel) übernehmen */
  function applyTheme() {
    const cs = getComputedStyle(box);
    const bg = (cs.getPropertyValue("--mk2-bg") || "#181d1a").trim();
    const gr = (cs.getPropertyValue("--mk2-ground") || "#22272d").trim();
    const rl = (cs.getPropertyValue("--mk2-ring") || "#353b43").trim();
    const dark = (cs.getPropertyValue("--mk2-dark") || "1").trim() === "1";
    scene.background.set(bg);
    scene.fog.color.set(bg);
    groundMat.color.set(gr);
    ringMat.color.set(rl);
    hemi.intensity = dark ? 0.9 : 1.15;
    renderer.toneMappingExposure = dark ? 1.05 : 0.95;
    dirty = true;
  }
  let dirty = true;
  applyTheme();
  new MutationObserver(applyTheme).observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme", "class"] });
  if (window.matchMedia) {
    const mq = window.matchMedia("(prefers-color-scheme: dark)");
    (mq.addEventListener ? mq.addEventListener("change", applyTheme) : mq.addListener(applyTheme));
  }

  /* Größe an den Kasten anpassen */
  function resize() {
    const w = cv.clientWidth, h = cv.clientHeight;
    if (!w || !h) return;
    renderer.setSize(w, h, false);
    cam.aspect = w / h;
    cam.updateProjectionMatrix();
    dirty = true;
  }
  resize();
  if (window.ResizeObserver) new ResizeObserver(resize).observe(cv); else window.addEventListener("resize", resize);

  /* Steuerung: Ziehen dreht, Strg/⌘ + Mausrad oder Schaltflächen zoomen; die Seite scrollt normal weiter */
  let drag = null;
  cv.addEventListener("pointerdown", (e) => {
    drag = { x: e.clientX, y: e.clientY };
    try { cv.setPointerCapture(e.pointerId); } catch (x) {}
    cv.classList.add("grab");
  });
  cv.addEventListener("pointermove", (e) => {
    if (!drag) return;
    const dx = e.clientX - drag.x, dy = e.clientY - drag.y;
    drag = { x: e.clientX, y: e.clientY };
    c.tTheta -= dx * 0.008; c.theta -= dx * 0.008;
    c.tPhi = Math.min(2.6, Math.max(0.05, c.tPhi - dy * 0.006));
    c.phi = c.tPhi;
    dirty = true;
  });
  const up = (e) => { drag = null; try { cv.releasePointerCapture(e.pointerId); } catch (x) {} cv.classList.remove("grab"); };
  cv.addEventListener("pointerup", up);
  cv.addEventListener("pointercancel", up);
  cv.addEventListener("wheel", (e) => {
    if (!e.ctrlKey && !e.metaKey) return;
    e.preventDefault();
    zoom(1 + e.deltaY * 0.0012);
  }, { passive: false });
  function zoom(f) { c.tDist = Math.min(34, Math.max(8, c.tDist * f)); dirty = true; }

  function setPressed(btn, on) { btn.setAttribute("aria-pressed", on ? "true" : "false"); }
  box.querySelectorAll("[data-view]").forEach((btn) => btn.addEventListener("click", () => {
    const v = VIEWS[btn.dataset.view];
    let t = v.theta;
    while (t - c.theta > Math.PI) t -= Math.PI * 2;
    while (c.theta - t > Math.PI) t += Math.PI * 2;
    c.tTheta = t; c.tPhi = v.phi; c.tDist = v.dist;
    state.spin = false;
    box.querySelectorAll("[data-view]").forEach((b) => setPressed(b, b === btn));
    syncToggles();
    dirty = true;
  }));
  box.querySelectorAll("[data-zoom]").forEach((btn) => btn.addEventListener("click", () => zoom(btn.dataset.zoom === "in" ? 0.85 : 1.18)));
  function syncToggles() {
    box.querySelectorAll("[data-toggle]").forEach((b) => setPressed(b, state[b.dataset.toggle]));
  }
  box.querySelectorAll("[data-toggle]").forEach((btn) => btn.addEventListener("click", () => {
    state[btn.dataset.toggle] = !state[btn.dataset.toggle];
    if (btn.dataset.toggle === "spin" && state.spin) box.querySelectorAll("[data-view]").forEach((b) => setPressed(b, false));
    syncToggles();
    dirty = true;
  }));
  syncToggles();

  /* Ausführung Male (Kanonen) oder Female (Maschinengewehre) */
  function setVersion(v) {
    state.version = v;
    spMale.visible = v === "male";
    spFemale.visible = v === "female";
    box.querySelectorAll("[data-version]").forEach((b) => setPressed(b, b.dataset.version === v));
    box.querySelectorAll("[data-nur]").forEach((el) => { el.hidden = el.dataset.nur !== v; });
    dirty = true;
  }
  box.querySelectorAll("[data-version]").forEach((btn) => btn.addEventListener("click", () => setVersion(btn.dataset.version)));
  setVersion(state.version);

  /* Nur zeichnen, wenn das Modell sichtbar ist */
  let visible = true;
  if (window.IntersectionObserver) new IntersectionObserver((en) => { visible = en[0].isIntersecting; if (visible) dirty = true; }).observe(cv);
  document.addEventListener("visibilitychange", () => { if (!document.hidden) dirty = true; });

  function loop() {
    requestAnimationFrame(loop);
    if (!visible || document.hidden) return;
    const moving = state.spin || state.tracks || drag ||
      Math.abs(c.tTheta - c.theta) > 1e-4 || Math.abs(c.tPhi - c.phi) > 1e-4 || Math.abs(c.tDist - c.dist) > 1e-3;
    if (!moving && !dirty) return;
    dirty = false;
    if (state.spin && !drag) { c.tTheta += 0.003; c.theta += 0.003; }
    c.theta += (c.tTheta - c.theta) * 0.08;
    c.phi += (c.tPhi - c.phi) * 0.08;
    c.dist += (c.tDist - c.dist) * 0.1;
    const sp = Math.sin(c.phi);
    /* schmale Kästen: Abstand vergrößern, damit der Panzer nicht abgeschnitten wird */
    const d = c.dist * Math.max(1, 1.45 / cam.aspect);
    cam.position.set(target.x + d * sp * Math.sin(c.theta), target.y + d * Math.cos(c.phi), target.z + d * sp * Math.cos(c.theta));
    if (cam.position.y < 0.15) cam.position.y = 0.15;
    cam.lookAt(target);
    ground.visible = c.phi < 1.62;
    ring.visible = ground.visible;
    if (state.tracks) { trackOff += 0.012; placeTracks(trackOff); }
    renderer.render(scene, cam);
  }
  loop();
  box.classList.add("ready");
})();
