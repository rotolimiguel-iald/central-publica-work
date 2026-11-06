"use strict";
// Bancada Um — interface. Toda conta é feita no motor (GPU); aqui só se pede, se desenha e se mostra o estatuto.
const $ = (s) => document.querySelector(s);
const COR = { ouro: "#e8b34b", azul: "#5aa9ff", lilas: "#b38cff", cinza: "#9aa6bb", verde: "#5fd39a", verm: "#ff6b6b", grade: "#1c2333", texto: "#8792a6" };
const PARAM = [
  { k: "H0", nome: "H₀", min: 60, max: 76, passo: 0.01, v: 67.95, fmt: 2 },
  { k: "ombh2", nome: "ω_b", min: 0.0205, max: 0.0245, passo: 0.00001, v: 0.022362, fmt: 5 },
  { k: "omch2", nome: "ω_c", min: 0.105, max: 0.135, passo: 0.0001, v: 0.11900, fmt: 4 },
  { k: "beta", nome: "β", min: -0.05, max: 0.05, passo: 0.0001, v: 0.0, fmt: 5 },
  { k: "c", nome: "c (normalização)", min: -0.02, max: 0.02, passo: 0.0001, v: 0.0, fmt: 4 },
];
const CONJ = [
  { k: "planck_comp", nome: "Planck 2018 comprimido", on: true },
  { k: "desi_dr1", nome: "DESI DR1 BAO", on: true },
  { k: "desi_dr2", nome: "DESI DR2 BAO (com cov)", on: false },
  { k: "sh0es", nome: "SH0ES H₀", on: false },
  { k: "sh0es_local", nome: "SH0ES H₀ como H₀_local = H₀(1+z*)^β (lei D1a; dois setores)", on: false },
  { k: "cc_moresco", nome: "Cronômetros H(z) Moresco+2022 (32; lei acumulada z*→z; Fase 4)", on: false },
  { k: "pantheon", nome: "Pantheon+ SNe (cov completa; z>0,01; M profilado)", on: false },
  { k: "pantheon_sh0es", nome: "Pantheon+SH0ES (1657: cosmologia + 77 calibradores Cefeida; M profilado)", on: false },
];
let DADOS = null, ESTADO = null, ULTIMA = null, BETA_TGL = null;

async function api(caminho, corpo) {
  const op = corpo ? { method: "POST", headers: { "Content-Type": "application/json", "X-Cliente": "interface" }, body: JSON.stringify(corpo) } : {};
  const r = await fetch(caminho, op);
  const j = await r.json();
  if (!r.ok) throw new Error(j.erro || r.status);
  return j;
}

// ---------------- desenho ----------------
function preparar(cv) {
  const dpr = window.devicePixelRatio || 1, w = cv.clientWidth, h = cv.clientHeight;
  cv.width = Math.round(w * dpr); cv.height = Math.round(h * dpr);
  const g = cv.getContext("2d"); g.setTransform(dpr, 0, 0, dpr, 0, 0); g.clearRect(0, 0, w, h);
  return { g, w, h };
}
function ticks(a, b, n) {
  const span = b - a, pass = Math.pow(10, Math.floor(Math.log10(span / n))), m = [1, 2, 5, 10].find((x) => span / (x * pass) <= n) * pass;
  const out = []; for (let t = Math.ceil(a / m) * m; t <= b + 1e-12; t += m) out.push(+t.toPrecision(12)); return out;
}
function grafico(cv, cfg) {
  const { g, w, h } = preparar(cv), M = { l: 46, r: 10, t: 10, b: 26 };
  let xs = [], ys = [];
  (cfg.series || []).forEach((s) => { xs.push(...s.x); ys.push(...s.y); });
  (cfg.pontos || []).forEach((p) => { xs.push(p.x); ys.push(p.y - (p.e || 0), p.y + (p.e || 0)); });
  let [x0, x1] = cfg.xlim || [Math.min(...xs), Math.max(...xs)], [y0, y1] = cfg.ylim || [Math.min(...ys), Math.max(...ys)];
  if (!cfg.ylim) { const p = (y1 - y0) * 0.08 || 1; y0 -= p; y1 += p; }
  const X = (x) => M.l + (x - x0) / (x1 - x0) * (w - M.l - M.r), Y = (y) => h - M.b - (y - y0) / (y1 - y0) * (h - M.t - M.b);
  g.font = "11px Segoe UI"; g.fillStyle = COR.texto; g.strokeStyle = COR.grade; g.lineWidth = 1;
  ticks(x0, x1, 6).forEach((t) => { g.beginPath(); g.moveTo(X(t), M.t); g.lineTo(X(t), h - M.b); g.stroke(); g.fillText(fmtT(t), X(t) - 10, h - 8); });
  ticks(y0, y1, 5).forEach((t) => { g.beginPath(); g.moveTo(M.l, Y(t)); g.lineTo(w - M.r, Y(t)); g.stroke(); g.fillText(fmtT(t), 4, Y(t) + 4); });
  (cfg.hlinhas || []).forEach((l) => { g.strokeStyle = l.cor; g.setLineDash(l.dash || []); g.beginPath(); g.moveTo(M.l, Y(l.y)); g.lineTo(w - M.r, Y(l.y)); g.stroke(); g.setLineDash([]); });
  (cfg.vlinhas || []).forEach((l) => { g.strokeStyle = l.cor; g.lineWidth = 1.5; g.setLineDash(l.dash || []); g.beginPath(); g.moveTo(X(l.x), M.t); g.lineTo(X(l.x), h - M.b); g.stroke(); g.setLineDash([]); if (l.rot) { g.fillStyle = l.cor; g.fillText(l.rot, X(l.x) + 4, M.t + 12); } });
  (cfg.barras || []).forEach((b) => { g.fillStyle = b.cor; const yb = Y(0), yt = Y(b.y); g.fillRect(X(b.x) - b.w / 2, Math.min(yb, yt), b.w, Math.abs(yb - yt)); });
  (cfg.series || []).forEach((s) => {
    g.strokeStyle = s.cor; g.lineWidth = s.larg || 2; g.setLineDash(s.dash || []); g.beginPath();
    s.x.forEach((x, i) => { const px = X(x), py = Y(s.y[i]); i ? g.lineTo(px, py) : g.moveTo(px, py); }); g.stroke(); g.setLineDash([]);
  });
  (cfg.pontos || []).forEach((p) => {
    g.strokeStyle = p.cor; g.fillStyle = p.cor; g.lineWidth = 1.3;
    if (p.e) { g.beginPath(); g.moveTo(X(p.x), Y(p.y - p.e)); g.lineTo(X(p.x), Y(p.y + p.e)); g.stroke(); }
    g.beginPath(); if (p.forma === "q") g.rect(X(p.x) - 3.5, Y(p.y) - 3.5, 7, 7); else g.arc(X(p.x), Y(p.y), 3.6, 0, 7); g.fill();
  });
  if (cfg.xrot) { g.fillStyle = COR.texto; g.fillText(cfg.xrot, w - M.r - g.measureText(cfg.xrot).width, h - 8); }
}
function fmtT(t) { const a = Math.abs(t); return a !== 0 && (a < 0.01 || a >= 1e4) ? t.toExponential(1) : +t.toPrecision(4) + ""; }
function mapa(cv, H, bx, by, cfg) {
  const { g, w, h } = preparar(cv), M = { l: 46, r: 10, t: 10, b: 26 };
  const nx = H.length, ny = H[0].length; let mx = 0; H.forEach((r) => r.forEach((v) => (mx = Math.max(mx, v))));
  const x0 = bx[0], x1 = bx[nx], y0 = by[0], y1 = by[ny];
  const X = (x) => M.l + (x - x0) / (x1 - x0) * (w - M.l - M.r), Y = (y) => h - M.b - (y - y0) / (y1 - y0) * (h - M.t - M.b);
  for (let i = 0; i < nx; i++) for (let j = 0; j < ny; j++) {
    const v = H[i][j] / mx; if (v <= 0) continue;
    g.fillStyle = `rgba(${Math.round(90 + 150 * v)},${Math.round(120 + 60 * v)},${Math.round(255 - 180 * v)},${0.15 + 0.85 * Math.sqrt(v)})`;
    g.fillRect(X(bx[i]), Y(by[j + 1]), X(bx[i + 1]) - X(bx[i]) + 0.6, Y(by[j]) - Y(by[j + 1]) + 0.6);
  }
  g.font = "11px Segoe UI"; g.fillStyle = COR.texto;
  ticks(x0, x1, 5).forEach((t) => g.fillText(fmtT(t), X(t) - 12, h - 8)); ticks(y0, y1, 5).forEach((t) => g.fillText(fmtT(t), 4, Y(t) + 4));
  (cfg.vlinhas || []).forEach((l) => { if (l.x < x0 || l.x > x1) return; g.strokeStyle = l.cor; g.lineWidth = 1.5; g.setLineDash(l.dash || []); g.beginPath(); g.moveTo(X(l.x), M.t); g.lineTo(X(l.x), h - M.b); g.stroke(); g.setLineDash([]); });
  g.fillText(cfg.xrot || "", w - 60, h - 8); g.fillText(cfg.yrot || "", M.l + 4, M.t + 12);
}

// ---------------- modelo ao vivo ----------------
function montarControles() {
  $("#sliders").innerHTML = PARAM.map((p) => `<div class="slider"><div class="rot"><span>${p.nome}</span><b id="v-${p.k}"></b></div>
    <input type="range" id="s-${p.k}" min="${p.min}" max="${p.max}" step="${p.passo}" value="${p.v}"></div>`).join("");
  PARAM.forEach((p) => $(`#s-${p.k}`).addEventListener("input", () => { mostrarValores(); agendar(); }));
  $("#conjuntos").innerHTML = CONJ.map((c) => `<label><input type="checkbox" data-c="${c.k}" ${c.on ? "checked" : ""}> ${c.nome}</label>`).join("");
  $("#conj-ev").innerHTML = CONJ.map((c) => `<label><input type="checkbox" data-e="${c.k}" ${c.on ? "checked" : ""}> ${c.nome}</label>`).join("");
  document.querySelectorAll("#conjuntos input").forEach((i) => i.addEventListener("change", agendar));
  $("#b-tgl").onclick = () => { if (BETA_TGL !== null) { $("#s-beta").value = BETA_TGL; mostrarValores(); agendar(); } };
  $("#b-zero").onclick = () => { $("#s-beta").value = 0; $("#s-c").value = 0; mostrarValores(); agendar(); };
  $("#b-fid").onclick = () => { PARAM.forEach((p) => ($(`#s-${p.k}`).value = p.v)); mostrarValores(); agendar(); };
  mostrarValores();
}
function theta() { const t = {}; PARAM.forEach((p) => (t[p.k] = +$(`#s-${p.k}`).value)); return t; }
function mostrarValores() { PARAM.forEach((p) => ($(`#v-${p.k}`).textContent = (+$(`#s-${p.k}`).value).toFixed(p.fmt))); }
function conjuntos(sel) { return [...document.querySelectorAll(sel)].filter((i) => i.checked).map((i) => i.dataset.c || i.dataset.e); }
// as opções de modelo/verossimilhança (auditoria de 28/09): modo selado × corrigido, e o mapa de R (escolha [INPUT] não derivada)
function opcoes() { const m = $("#modo"), r = $("#mapa-r"); return { modo: m ? m.value : "tgl", mapa_R: r ? r.value : "eff" }; }
let tAg = null, emVoo = false, pendente = false;
function agendar() { clearTimeout(tAg); tAg = setTimeout(avaliar, 40); }
async function avaliar() {
  if (!ESTADO?.canone?.ok) { $("#ev-texto").textContent = "Contrato canônico indisponível: atualização necessária."; return; }
  if (emVoo) { pendente = true; return; } emVoo = true;
  try { ULTIMA = await api("/api/avaliar", { theta: theta(), conjuntos: conjuntos("#conjuntos input"), curvas: true, opcoes: opcoes() }); desenharModelo(); }
  catch (e) { $("#ev-texto").textContent = "Avaliação recusada: " + e.message; }
  emVoo = false; if (pendente) { pendente = false; avaliar(); }
}
function desenharModelo() {
  const r = ULTIMA, c = r.curvas, tipos = [["DM/rd", "g-dm", "DM_rd"], ["DH/rd", "g-dh", "DH_rd"], ["DV/rd", "g-dv", "DV_rd"]];
  tipos.forEach(([tp, id, chave]) => {
    const pts = [];
    DADOS.desi_dr1.linhas.filter((l) => l.tipo === tp).forEach((l) => pts.push({ x: l.z, y: l.valor, e: l.sigma, cor: COR.azul }));
    DADOS.desi_dr2.linhas.filter((l) => l.tipo === tp).forEach((l) => pts.push({ x: l.z + 0.012, y: l.valor, e: l.sigma, cor: COR.lilas, forma: "q" }));
    grafico($("#" + id), { series: [{ x: c.z, y: c.lcdm[chave], cor: COR.cinza, dash: [5, 4], larg: 1.4 }, { x: c.z, y: c[chave], cor: COR.ouro }], pontos: pts, xrot: "z" });
  });
  // desvios
  const barras = [], rot = []; let i = 0;
  const add = (vals, pred, sig, cor) => vals.forEach((v, k) => { barras.push({ x: i, y: (pred[k] - v) / sig[k], w: 9, cor }); i++; });
  const sets = r.conjuntos;
  if (sets.includes("planck_comp")) add(DADOS.planck_comp.valores, r.predito.planck, DADOS.planck_comp.cov.map((l, k) => Math.sqrt(l[k])), COR.verde);
  if (sets.includes("desi_dr1")) add(DADOS.desi_dr1.linhas.map((l) => l.valor), r.predito.desi_dr1, DADOS.desi_dr1.linhas.map((l) => l.sigma), COR.azul);
  if (sets.includes("desi_dr2")) add(DADOS.desi_dr2.linhas.map((l) => l.valor), r.predito.desi_dr2, DADOS.desi_dr2.linhas.map((l) => l.sigma), COR.lilas);
  if (sets.includes("sh0es")) add([DADOS.sh0es.valor], [r.predito.H0], [DADOS.sh0es.sigma], COR.verm);
  const mx = Math.max(3, ...barras.map((b) => Math.abs(b.y))) * 1.1;
  grafico($("#g-pull"), { xlim: [-1, Math.max(i, 1)], ylim: [-mx, mx], barras, hlinhas: [{ y: 0, cor: "#3a4760" }, { y: 2, cor: "#3a2f2f", dash: [3, 3] }, { y: -2, cor: "#3a2f2f", dash: [3, 3] }] });
  grafico($("#g-phi"), { series: [{ x: c.Phi.z, y: c.Phi.Phi, cor: COR.ouro }], hlinhas: [{ y: 1, cor: COR.cinza, dash: [4, 4] }], xrot: "z" });
  // tabelas
  const lin = (a, b) => `<tr><td>${a}</td><td>${b}</td></tr>`;
  $("#t-chi2").innerHTML = Object.entries(r.chi2).map(([k, v]) => lin(k, v.toFixed(3))).join("") + lin("<b>total</b>", `<b>${r.chi2_total.toFixed(3)}</b>`) + lin("n dados", r.n_dados);
  const d = r.derivados;
  $("#t-der").innerHTML = lin("Ω_Λ", d.Omega_L.toFixed(5)) + lin("r_drag (Mpc)", d.r_drag.toFixed(3)) + lin("r* (Mpc)", d.r_star.toFixed(3)) + lin("z*", d.z_star.toFixed(2)) +
    lin("E(0) − 1", d.E0_menos_1.toExponential(1)) + lin("resíduo do fecho", d.residuo_fecho.toExponential(1)) + lin("D_M ΛCDM / CAMB", d.autoverif_DM_camb.toFixed(6)) +
    lin("dentro dos limites", d.dentro_dos_limites ? "sim" : "<span style='color:#ff6b6b'>não</span>");
  const pl = r.predito.planck, obs = DADOS.planck_comp.valores, nm = ["R", "ℓ_A", "ω_b"];
  $("#t-planck").innerHTML = nm.map((n, k) => lin(n, `${pl[k].toFixed(k === 2 ? 5 : 4)} <span style="color:#8792a6">/ ${obs[k]}</span>`)).join("");
}

// ---------------- evidência ----------------
function travar(v) { v = v || !ESTADO?.canone?.ok; ["#b-ajustar", "#b-comparar", "#b-amostrar"].forEach((s) => ($(s).disabled = v)); }
function sig(s) {
  if (!s) return "";
  const num = (x, f) => Number.isFinite(x) ? f(x) : "não disponível";
  return `<div class="card">Diagnóstico local: z = <b>${num(s.z_local, x => x.toFixed(2))}</b> (p = ${num(s.p_local, x => x.toExponential(2))})<br>
    Šidák exploratório, ${s.n_familias} família(s): z = ${num(s.z_sidak_exploratorio, x => x.toFixed(2))}. Significância global não calibrada.</div>`;
}
$("#b-ajustar").onclick = async () => {
  travar(true); $("#ev-texto").textContent = "ajustando…";
  try {
    const r = await api("/api/ajustar", { conjuntos: conjuntos("#conj-ev input"), beta: "livre", c_livre: $("#c-livre").checked, opcoes: opcoes() });
    const a = r.ajuste, s = a.sigma_JtJ;
    $("#ev-texto").innerHTML = `<span class="estatuto">${r.estatuto}</span>\n<span class="grande">β = ${a.theta.beta.toFixed(5)} ± ${(s.beta || 0).toFixed(5)}</span>\n` +
      `χ² = ${a.chi2.toFixed(3)} com ${a.gl} g.l. · H₀ = ${a.theta.H0.toFixed(2)} ± ${(s.H0 || 0).toFixed(2)}\nα√e = ${r.beta_tgl.toFixed(6)} está a ${(r.beta_tgl_em_sigma_JtJ || 0).toFixed(2)} σ (JᵀJ)` + sig(r.significancia);
  } catch (e) { $("#ev-texto").textContent = "falhou: " + e.message; }
  travar(false); carregarLivro();
};
$("#b-comparar").onclick = async () => {
  travar(true); $("#ev-texto").textContent = "ajustando os três modelos…";
  try {
    const r = await api("/api/comparar", { conjuntos: conjuntos("#conj-ev input"), c_livre: $("#c-livre").checked, opcoes: opcoes() });
    const d = r.delta_chi2;
    $("#ev-texto").innerHTML = `<span class="estatuto">${r.estatuto}</span>\n` +
      `ΛCDM (β = 0)        χ² = ${r.lcdm.chi2.toFixed(3)}\nTGL (β = α√e)      χ² = ${r.tgl_beta_fixo.chi2.toFixed(3)}\nβ livre            χ² = ${r.beta_livre.chi2.toFixed(3)}  (β̂ = ${r.beta_livre.theta.beta.toFixed(5)})\n\n` +
      `<span class="grande">Δχ²(TGL − ΛCDM) = ${d.tgl_menos_lcdm.toFixed(3)}</span>\n${r.leitura}` + sig(r.significancia);
  } catch (e) { $("#ev-texto").textContent = "falhou: " + e.message; }
  travar(false); carregarLivro();
};
$("#b-amostrar").onclick = async () => {
  travar(true);
  try {
    const { tarefa } = await api("/api/amostrar", { conjuntos: conjuntos("#conj-ev input"), c_livre: $("#c-livre").checked, walkers: +$("#n-w").value,
      passos: +$("#n-p").value, queima: +$("#n-q").value, semente: +$("#n-s").value, opcoes: opcoes() });
    const t0 = Date.now();
    const loop = async () => {
      const t = await api("/api/tarefas/" + tarefa);
      $("#progresso div").style.width = (100 * t.progresso).toFixed(1) + "%";
      $("#ev-texto").textContent = `${t.estado} · ${(100 * t.progresso).toFixed(0)}% · ${((Date.now() - t0) / 1000).toFixed(0)} s`;
      if (t.estado === "pronta") { mostrarPosterior(t.resultado); travar(false); carregarLivro(); return; }
      if (t.estado === "falhou") { $("#ev-texto").textContent = "falhou: " + t.erro; travar(false); return; }
      setTimeout(loop, 700);
    };
    loop();
  } catch (e) { $("#ev-texto").textContent = "falhou: " + e.message; travar(false); }
};
function mostrarPosterior(r) {
  const b = r.resumo.beta, hb = r.hist_beta;
  const xs = hb.bordas.slice(0, -1).map((v, i) => (v + hb.bordas[i + 1]) / 2), w = hb.bordas[1] - hb.bordas[0], mx = Math.max(...hb.contagens);
  const barras = xs.map((x, i) => ({ x, y: hb.contagens[i] / mx, w: 0, cor: COR.azul }));
  grafico($("#g-post"), {
    series: [{ x: xs, y: hb.contagens.map((c) => c / mx), cor: COR.azul, larg: 2 }], ylim: [0, 1.08], xlim: [Math.min(hb.bordas[0], -0.001), Math.max(hb.bordas.at(-1), r.beta_tgl * 1.15)],
    vlinhas: [{ x: 0, cor: COR.cinza, dash: [4, 4], rot: "0" }, { x: r.beta_tgl, cor: COR.ouro, rot: "α√e" }, { x: b.median, cor: COR.azul, dash: [2, 3] }], xrot: "β",
  });
  const h2 = r.hist_beta_H0;
  mapa($("#g-2d"), h2.contagens, h2.bordas_beta, h2.bordas_H0, { vlinhas: [{ x: 0, cor: COR.cinza, dash: [4, 4] }, { x: r.beta_tgl, cor: COR.ouro }], xrot: "β", yrot: "H₀" });
  $("#ev-texto").innerHTML = `<span class="estatuto">${r.estatuto}</span>\n<span class="grande">β = ${b.median.toFixed(5)} (+${b.sigma_upper.toFixed(5)} / −${b.sigma_lower.toFixed(5)})</span>\n` +
    `H₀ = ${r.resumo.H0.median.toFixed(2)} · ${r.walkers} walkers × ${r.passos} passos em ${r.segundos} s · aceitação ${r.aceitacao_media.toFixed(2)} · amostras efetivas ≈ ${Math.round(r.amostras_efetivas)}\n` +
    `fração do posterior com β ≥ α√e: ${(100 * r.fracao_beta_acima_de_beta_tgl).toFixed(3)}% · com β ≥ 0: ${(100 * r.fracao_beta_acima_de_zero).toFixed(1)}%` + sig(r.significancia);
}

// ---------------- estado, lago, gw, livro, validação ----------------
async function carregarEstado() {
  try {
    ESTADO = await api("/api/estado");
    const e = ESTADO, ch = [];
    ch.push(`<span class="chip ${e.pronta ? "ok" : "ruim"}">motor <b>${e.pronta ? "pronto" : e.erro ? "erro" : "carregando"}</b></span>`);
    ch.push(`<span class="chip ${e.canone?.ok ? "ok" : "ruim"}">cânone <b>${e.canone?.ok ? escapaHtml(e.canone.canonical_version) + " · " + e.canone.um_py_sha256.slice(0, 12) : "revalidação necessária"}</b></span>`);
    travar(!e.pronta);
    if (e.gpu) ch.push(`<span class="chip">${e.gpu.nome.replace("NVIDIA GeForce ", "")} · VRAM livre <b>${e.gpu.vram_livre_gib} GiB</b></span>`);
    if (e.ram) ch.push(`<span class="chip">RAM livre <b>${e.ram.livre_gib}</b> / ${e.ram.total_gib} GiB</span>`);
    if (e.motor) { BETA_TGL = e.motor.beta_tgl; ch.push(`<span class="chip">β<sub>TGL</sub> = α√e = <b>${e.motor.beta_tgl.toFixed(6)}</b></span>`); }
    if (e.livro) ch.push(`<span class="chip">livro <b>${e.livro.total}</b> · famílias de teste <b>${e.livro.familias_de_teste}</b></span>`);
    $("#chips").innerHTML = ch.join("");
    return e.pronta;
  } catch (e) { $("#chips").innerHTML = `<span class="chip ruim">sem conexão <b>${e.message}</b></span>`; return false; }
}
let tLago = null, SEL = null;
const gib = (b) => (b / 2 ** 30).toFixed(2);
async function carregarLago() {
  clearTimeout(tLago);
  const l = await api("/api/lago"), cat = l.catalogo, res = l.residente, est = res.estado;
  const ram = ESTADO && ESTADO.ram ? ESTADO.ram : null;
  const porEstado = {}; res.arquivos.forEach((a) => (porEstado[a.estado] = (porEstado[a.estado] || 0) + 1));
  let h = `<div class="card"><b>Residente na RAM: ${gib(est.bytes_residentes || 0)} GiB</b> em ${est.carregados || 0} arquivos · estado <b>${est.estado}</b>
    ${est.segundos ? `· carga completa em ${est.segundos} s` : ""} ${ram ? `· RAM livre ${ram.livre_gib} / ${ram.total_gib} GiB` : ""}
    <div class="progresso"><div style="width:${(100 * (est.progresso || 0)).toFixed(1)}%"></div></div>
    <span class="nota">${Object.entries(porEstado).map(([k, v]) => `${k}: ${v}`).join(" · ")} · ${cat && cat.bytes_total ? `catálogo total ${gib(cat.bytes_total)} GiB` : ""}</span>
    <div class="botoes"><button id="b-carregar">recarregar o lago</button></div></div>`;
  h += `<div class="grade2"><div><table>` + res.arquivos.filter((a) => a.estado !== "na_fila").sort((a, b) => b.bytes - a.bytes).map((a) => {
    const nome = a.caminho.split("\\").slice(-3).join("\\");
    const tabs = (a.tabelas || []).map((t) => `<button class="mini" data-c="${encodeURIComponent(a.caminho)}" data-h="${t.hdu}">HDU ${t.hdu} · ${t.tipo} · ${t.linhas.toLocaleString("pt-BR")}${t.n_colunas ? " × " + t.n_colunas : ""}</button>`).join(" ");
    return `<tr><td title="${a.caminho}">${nome}<br><span class="nota">${a.estado}${a.motivo ? " — " + a.motivo : ""}${a.sha256 ? " · sha256 " + a.sha256 : ""}${a.segundos ? " · " + a.segundos + " s" : ""}</span><br>${tabs}</td><td>${gib(a.bytes)} GiB</td></tr>`;
  }).join("") + `</table></div><div id="explorador" class="card">Escolha uma HDU à esquerda para explorar as colunas na GPU.</div></div>`;
  $("#lago").innerHTML = h;
  $("#b-carregar").onclick = async () => { await api("/api/lago/carregar", {}); carregarLago(); };
  document.querySelectorAll("#lago button.mini").forEach((b) => (b.onclick = () => explorar(decodeURIComponent(b.dataset.c), +b.dataset.h)));
  if (est.estado === "carregando") tLago = setTimeout(carregarLago, 2000);
}
async function explorar(caminho, hdu) {
  const t = await api(`/api/lago/colunas?caminho=${encodeURIComponent(caminho)}&hdu=${hdu}`);
  SEL = { caminho, hdu, t };
  const num = t.colunas.filter((c) => /[if]\d|float|int|uint/.test(c.dtype));
  const opc = num.map((c) => `<option>${c.nome}</option>`).join("");
  const ra = num.find((c) => /^(ra|alpha_j2000|raj2000|ra_deg)$/i.test(c.nome)), dec = num.find((c) => /^(dec|delta_j2000|dej2000|dec_deg)$/i.test(c.nome));
  $("#explorador").innerHTML = `<b>${caminho.split("\\").pop()}</b> · HDU ${hdu} · ${t.linhas.toLocaleString("pt-BR")} linhas · ${t.colunas.length} colunas
    <div class="linha">coluna <select id="x-col">${opc}</select> <label><input type="checkbox" id="x-log"> log₁₀</label> <button id="b-hist">histograma (GPU)</button></div>
    <div class="linha">X <select id="m-x">${opc}</select> Y <select id="m-y">${opc}</select> <button id="b-mapa">mapa 2D (GPU)</button></div>
    <canvas id="g-lago" style="height:300px"></canvas><div id="x-info" class="nota"></div>`;
  if (ra) $("#m-x").value = ra.nome; if (dec) $("#m-y").value = dec.nome;
  $("#b-hist").onclick = async () => {
    const r = await api("/api/lago/histograma", { caminho, hdu, coluna: $("#x-col").value, bins: 140, log: $("#x-log").checked });
    const w = (r.faixa[1] - r.faixa[0]) / r.contagens.length, xs = r.contagens.map((_, i) => r.faixa[0] + (i + 0.5) * w), mx = Math.max(...r.contagens) || 1;
    grafico($("#g-lago"), { series: [{ x: xs, y: r.contagens.map((c) => c / mx), cor: COR.azul }], ylim: [0, 1.05], xrot: (r.log10 ? "log₁₀ " : "") + r.coluna });
    $("#x-info").textContent = `${r.n_finito.toLocaleString("pt-BR")} valores finitos de ${r.n.toLocaleString("pt-BR")} · média ${r.media.toPrecision(6)} · desvio ${r.desvio.toPrecision(4)} · [${r.minimo.toPrecision(5)}, ${r.maximo.toPrecision(5)}] · ${r.dispositivo} em ${(1000 * r.segundos).toFixed(0)} ms`;
  };
  $("#b-mapa").onclick = async () => {
    const r = await api("/api/lago/mapa", { caminho, hdu, x: $("#m-x").value, y: $("#m-y").value, bins: [360, 180] });
    const bx = [...Array(r.bins[0] + 1).keys()].map((i) => r.faixa[0][0] + i * (r.faixa[0][1] - r.faixa[0][0]) / r.bins[0]);
    const by = [...Array(r.bins[1] + 1).keys()].map((i) => r.faixa[1][0] + i * (r.faixa[1][1] - r.faixa[1][0]) / r.bins[1]);
    mapa($("#g-lago"), r.contagens, bx, by, { xrot: r.x, yrot: r.y });
    $("#x-info").textContent = `${r.n.toLocaleString("pt-BR")} pontos · ${r.bins[0]}×${r.bins[1]} células · ${r.dispositivo} em ${(1000 * r.segundos).toFixed(0)} ms`;
  };
}
let tGW = null, GWR = null;
const f3 = (v, n = 3) => (v === null || v === undefined || Number.isNaN(v) ? "—" : (+v).toFixed(n));
async function carregarGW() {
  clearTimeout(tGW);
  const g = await api("/api/gw"), r = g.residente, e = r.estado, o = g.oficial;
  const arqs = Object.entries(r.arquivos).map(([k, v]) => `${k.replace("_FASE6_ECO_RADICAL_20261001", "").replace("_FASE6_ANTES_DE_ABRIR", "").replace(".json", "")} ${v.presente ? "✓ " + v.sha16 : "—"}`).join(" · ");
  let h = `<div class="card"><b>Banco residente de eco (Fase 6, «a transformada radical»)</b>: ${r.n_eventos} eventos BBH · ${Object.entries(r.por_era_src || {}).map(([k, v]) => `${k}: ${v}`).join(" · ")} ·
    ${r.n_series_ok} séries branqueadas na RAM (${r.gib_residente} GiB) · ${r.n_series_nan} com NaN · estado <b>${e.estado}</b> ${e.segundos ? `· carga em ${e.segundos} s` : ""} ${e.erro ? `· <span class="ruim">${e.erro}</span>` : ""}
    <div class="progresso"><div style="width:${e.total ? (100 * e.carregados / e.total).toFixed(1) : 0}%"></div></div>
    <span class="nota">${r.pipeline}</span><br><span class="nota">estágios: ${arqs}</span>
    <div class="linha">era <select id="gw-era"><option value="">todas</option><option>O1O2</option><option>O3</option><option>O4</option></select>
      SNR ≥ <input id="gw-snr" type="number" value="8" step="0.5" style="width:64px"> M_f(det) ≥ <input id="gw-mf" type="number" value="0" style="width:64px">
      <button id="gw-b-ev">listar eventos</button> · subamostra <select id="gw-sub"><option>todos</option><option>o4</option><option>maio</option></select>
      σ <select id="gw-sig"><option value="max">max(fora da fonte, jackknife) — a pré-registrada</option><option value="off">fora da fonte</option><option value="jack">jackknife</option></select>
      <button id="gw-b-emp">empilhar com estes filtros (consulta)</button></div></div>
    <div class="card nota">Bancada oficial (${o.fonte}): ${o.fora_do_ar ? "fora do ar" : "no ar (só leitura)"}</div>
    <div class="grade2"><div id="gw-eventos" class="card">Clique em «listar eventos».</div><div><div id="gw-serie" class="card">Escolha uma série (H1/L1) na tabela para ver o trecho branqueado em torno do merger.</div><div id="gw-emp" class="card">O empilhamento de consulta aparece aqui (não é o veredito selado).</div></div></div>`;
  $("#gw").innerHTML = h;
  $("#gw-b-ev").onclick = gwEventos; $("#gw-b-emp").onclick = gwEmpilhar;
  if (e.estado === "carregando" || e.estado === "na_fila") tGW = setTimeout(carregarGW, 3000);
}
function gwFiltros() {
  const f = {}; const era = $("#gw-era").value, snr = +$("#gw-snr").value, mf = +$("#gw-mf").value;
  if (era) f.era = era; if (snr > 0) f.snr_min = snr; if (mf > 0) f.Mf_min = mf; return f;
}
async function gwEventos() {
  const f = gwFiltros(), q = Object.entries(f).map(([k, v]) => `${k}=${encodeURIComponent(v)}`).join("&");
  const r = await api("/api/gw/eventos" + (q ? "?" + q : "")); GWR = r;
  const leis = ["MAY", "KMS"];
  $("#gw-eventos").innerHTML = `<b>${r.n} eventos</b> <span class="nota">· estágios: cego ${r.estagios.cego || "—"} · aberto ${r.estagios.aberto || "—"}</span>
    <div style="max-height:520px;overflow:auto"><table><tr><td>evento</td><td>era</td><td>SNR</td><td>M_f det</td><td>a_f</td><td>τ_MAY · τ_KMS (ms)</td><td>séries</td><td>eco (â H1 / L1 por lei)</td></tr>` +
    r.eventos.map((ev) => `<tr><td title="${ev.catalogo} v${ev.versao}">${ev.nome}</td><td>${ev.era}</td><td>${f3(ev.snr, 1)}</td><td>${f3(ev.Mf_det, 1)}</td><td>${f3(ev.a_f, 3)}</td>
      <td>${ev.tau_ms ? f3(ev.tau_ms.MAY, 2) + " · " + f3(ev.tau_ms.KMS, 2) : "—"}</td>
      <td>${["H1", "L1"].map((d) => ev.dets.includes(d) ? `<button class="mini" data-k="${ev.nome}_${d}" data-tau="${ev.tau_ms ? ev.tau_ms.KMS : 0}" data-tm="${ev.tau_ms ? ev.tau_ms.MAY : 0}">${d}</button>` : `<span class="nota">${d}${(ev.nan || []).includes(d) ? " NaN" : " —"}</span>`).join(" ")}</td>
      <td class="nota">${leis.map((l) => ev.eco && ev.eco[l] ? `${l}: ${["H1", "L1"].map((d) => ev.eco[l][d] ? (ev.eco[l][d].a === null ? "cego" : f3(ev.eco[l][d].a, 2) + "±" + f3(ev.eco[l][d].sigma, 2)) : "—").join(" / ")}` : "").filter(Boolean).join("<br>")}</td></tr>`).join("") + `</table></div>`;
  document.querySelectorAll("#gw-eventos button.mini").forEach((b) => (b.onclick = () => gwSerie(b.dataset.k, +b.dataset.tau, +b.dataset.tm)));
}
async function gwSerie(key, tauKms, tauMay) {
  const s = await api(`/api/gw/serie?key=${key}&t0=-0.25&dur=0.45&n_max=3000`), a = await api(`/api/gw/espectro?key=${key}`);
  if (s.status && s.status !== "OK") { $("#gw-serie").innerHTML = `<b>${key}</b>: ${s.status}`; return; }
  $("#gw-serie").innerHTML = `<b>${key}</b> · branqueada (passa-alta 15 Hz, Tukey, banda 20–1024 Hz) · sd fora da fonte ${f3(s.sd_off, 3)} · MAD na fonte ${f3(s.mad_on, 3)} · pico/sd ${f3(s.pico_sd, 1)} · sha256 ${s.sha256.slice(0, 16)}…
    <br><span class="nota">linhas: merger (GPS do catálogo) em 0; atraso MAY (${f3(tauMay, 2)} ms) e KMS (${f3(tauKms, 2)} ms) a partir do merger</span>
    <canvas id="g-gw-s" style="height:220px"></canvas><canvas id="g-gw-a" style="height:180px"></canvas><div class="nota">ASD √PSD (Welch), log₁₀, até 1024 Hz</div>`;
  grafico($("#g-gw-s"), { series: [{ x: s.t_rel, y: s.y, cor: COR.azul, larg: 1 }], xrot: "t − t_merger (s)",
    vlinhas: [{ x: 0, cor: COR.ouro }, { x: tauMay / 1000, cor: COR.verde, dash: [3, 3] }, { x: tauKms / 1000, cor: COR.lilas, dash: [3, 3] }] });
  const lf = a.f_hz.map((v) => Math.log10(Math.max(v, 1))), la = a.asd.map((v) => Math.log10(Math.max(v, 1e-30)));
  grafico($("#g-gw-a"), { series: [{ x: lf, y: la, cor: COR.cinza, larg: 1.2 }], xrot: "log₁₀ f (Hz)" });
}
async function gwEmpilhar() {
  const f = gwFiltros(), sub = $("#gw-sub").value, sig = $("#gw-sig").value;
  const r = await api("/api/gw/empilhar", { sub, filtros: f, sigma_regra: sig });
  if (r.erro) { $("#gw-emp").innerHTML = `<span class="ruim">${r.erro}</span>`; return; }
  const R = r.resultados, L = ["R1_peso1", "R2_peso2_2theta", "R3_quadrado"], nomes = { R1_peso1: "R1 √β", R2_peso2_2theta: "R2 sin 2θ", R3_quadrado: "R3 β" };
  $("#gw-emp").innerHTML = `<b>Empilhamento de consulta</b> · sub <b>${r.sub}</b> · filtros ${JSON.stringify(r.filtros)} · σ ${r.sigma_regra} · estágios cego ${r.estagios.cego || "—"} / aberto ${r.estagios.aberto || "—"} / pré-registro ${r.estagios.preregistro || "—"}
    <br><span class="nota">${r.aviso}</span>
    <table><tr><td>lei</td><td>n_ev</td><td>â ± σ_usado</td><td>σ_off · σ_jack · dispersão</td><td>z_det</td>${L.map((l) => `<td>${nomes[l]}: poder · sist. · z_excl · veredito</td>`).join("")}</tr>` +
    Object.entries(R).map(([law, st]) => st.n_eventos ? `<tr><td>${law}</td><td>${st.n_eventos}</td><td>${f3(st.a)} ± ${f3(st.sigma_usado)}</td><td>${f3(st.sigma_off)} · ${f3(st.sigma_jack)} · ${f3(st.fator_dispersao, 2)}</td><td>${f3(st.z_det, 2)}</td>` +
      L.map((l) => { const p = st.por_leitura[l], v = st.vereditos_de_consulta[l]; return `<td>${f3(p.poder, 2)} · ${f3(p.sistematica_relativa, 2)} · ${f3(p.z_excl, 2)} · <b>${v.veredito.replace("TGL_ECHO_RADICAL_V3__", "")}</b></td>`; }).join("") + `</tr>` :
      `<tr><td>${law}</td><td colspan="8">sem eventos</td></tr>`).join("") + `</table>
    <div class="nota">controles look-elsewhere (τ/2, 2τ): ${Object.entries(R).map(([law, st]) => st.n_eventos ? `${law}: ` + Object.entries(st.controles).map(([c, v]) => `${c} â ${f3(v.a, 2)} ± ${f3(v.sigma, 2)} (z ${f3(v.z, 1)}; diafonia ${f3(v.xtalk_from_R1, 2)})`).join(" · ") : "").filter(Boolean).join("<br>")}</div>`;
}
async function carregarLivro() {
  try {
    const l = await api("/api/livro");
    $("#livro").innerHTML = `<div class="card">${l.total} registros · <b>${l.familias_de_teste}</b> famílias de teste (a correção de significância usa este número)</div>
      <table><tr><td>quando</td><td>quem</td><td>operação</td><td>conjuntos</td><td>estatuto</td><td>p local</td></tr>` +
      l.ultimas.map((u) => `<tr><td>${u.ts}</td><td>${u.cliente}</td><td>${u.operacao}</td><td>${u.conjuntos.join(", ")}</td><td>${u.estatuto}</td><td>${u.p_local === null ? "—" : (+u.p_local).toExponential(2)}</td></tr>`).join("") + "</table>";
  } catch (e) { }
}
async function carregarValidacao() {
  try {
    const v = await api("/api/validacao");
    $("#validacao").innerHTML = Object.entries(v).map(([f, d]) => `<div class="card"><b>${f}</b><pre style="white-space:pre-wrap;font-size:12px">${JSON.stringify(d.resumo_curto || d, null, 1).slice(0, 3000)}</pre></div>`).join("") || "nenhuma validação gravada";
  } catch (e) { }
}

// Relatórios da gerência: arquivos Markdown publicados em ui/relatorios/ (índice gerado por ferramentas/publicar_relatorio.py, com sha256).
// A renderização usa o marked (jsdelivr); se não carregar, o texto aparece cru, nunca some.
let MARKED = null;
function carregarMarked() {
  if (MARKED) return Promise.resolve(MARKED);
  return new Promise((res) => {
    const s = document.createElement("script");
    s.src = "https://cdn.jsdelivr.net/npm/marked@12/marked.min.js";
    s.onload = () => { MARKED = window.marked; res(MARKED); };
    s.onerror = () => res(null);
    document.head.appendChild(s);
  });
}
function escapaHtml(t) { return t.replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c])); }
async function mostrarRelatorio(item) {
  const alvo = $("#relatorio-corpo");
  alvo.innerHTML = `<div class="nota">carregando ${item.arquivo}…</div>`;
  const r = await fetch("/ui/relatorios/" + item.arquivo);
  const md = await r.text();
  const m = await carregarMarked();
  alvo.innerHTML = `<div class="nota">${item.arquivo} · sha256 ${item.sha256.slice(0, 16)}… · ${item.bytes.toLocaleString("pt-BR")} bytes · publicado ${item.publicado}</div>` +
    (m ? `<div class="md">${m.parse(md)}</div>` : `<pre class="md-cru">${escapaHtml(md)}</pre>`);
}
async function carregarRelatorios() {
  try {
    const r = await fetch("/ui/relatorios/index.json");
    if (!r.ok) throw new Error("sem índice");
    const idx = await r.json();
    const itens = idx.relatorios || [];
    $("#relatorios").innerHTML = `<div class="linha"><label>relatório</label><select id="sel-relatorio">` +
      itens.map((it, i) => `<option value="${i}">${it.titulo}</option>`).join("") + `</select><span class="nota">${itens.length} publicado(s); a fonte canônica é a pasta de trabalho da gerência, isto é cópia com hash.</span></div><div id="relatorio-corpo"></div>`;
    const sel = $("#sel-relatorio");
    sel.addEventListener("change", () => mostrarRelatorio(itens[+sel.value]));
    if (itens.length) mostrarRelatorio(itens[0]);
  } catch (e) {
    $("#relatorios").innerHTML = `<div class="card">Nenhum relatório publicado ainda (ferramentas/publicar_relatorio.py).<br><span class="nota">${e}</span></div>`;
  }
}

document.querySelectorAll("#abas button").forEach((b) => b.addEventListener("click", () => {
  document.querySelectorAll("#abas button").forEach((x) => x.classList.toggle("ativa", x === b));
  document.querySelectorAll(".aba").forEach((a) => a.classList.toggle("ativa", a.id === "aba-" + b.dataset.aba));
  const a = b.dataset.aba;
  if (a === "lago") carregarLago(); if (a === "gw") carregarGW(); if (a === "livro") carregarLivro(); if (a === "validacao") carregarValidacao();
  if (a === "relatorios") carregarRelatorios();
  if (a === "modelo" && ULTIMA) desenharModelo();
}));
window.addEventListener("resize", () => ULTIMA && desenharModelo());
["#modo", "#mapa-r"].forEach((s) => { const el = $(s); if (el) el.addEventListener("change", () => avaliar()); });

(async function iniciar() {
  montarControles();
  while (!(await carregarEstado())) await new Promise((r) => setTimeout(r, 1500));
  DADOS = await api("/api/dados");
  $("#ev-texto").textContent = "Contrato conferido. Mova um parâmetro para avaliar; as opções TGL e mapa efetivo estão selecionadas.";
  setInterval(carregarEstado, 5000);
})();
