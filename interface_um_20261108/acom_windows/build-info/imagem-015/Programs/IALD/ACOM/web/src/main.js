import { datasets, tests, leanTerms, quantumStages, benchCards, demoAnswers } from './data.js';
import { contentI18n } from './content-i18n.js';
import { createSpaceScene, createQuantumScene } from './scene.js';
import { createAcomController } from './acom.js';
import { languages, currentLanguage, languageMeta, t, localize, applyStaticTranslations, setLanguage, setCustomLanguage, systemLanguage } from './i18n.js';

const $ = (selector, root = document) => root.querySelector(selector);
const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];
const icon = (name) => `<svg aria-hidden="true"><use href="#i-${name}"></use></svg>`;
const clamp = (value, min = 0, max = 1) => Math.min(max, Math.max(min, value));
const pad = (value) => String(value).padStart(2, '0');
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

const D = {
  waiting: ['Preparando a fronteira…', 'Preparing the boundary…', 'تحضير الحد…'],
  dataBefore: ['A cadeia de custódia precede todos os ritos.', 'Custody precedes every rite.', 'الحفظ يسبق كل الطقوس.'],
  queue: ['EM FILA', 'QUEUED', 'في الانتظار'], presented: ['APRESENTADO', 'PRESENTED', 'تم العرض'], inAct: ['EM ATO', 'IN ACT', 'قيد التنفيذ'],
  reading: ['LENDO', 'READING', 'قراءة'], pinLog: ['pin conferido', 'pin checked', 'تم التحقق من المرجع'], acquireLog: ['aquisição e conferência', 'acquisition and check', 'الاستحواذ والتحقق'],
  runStart: ['Inscrição aceita · ω(I) = 1 · execução visual iniciada', 'Inscription accepted · ω(I) = 1 · visual run started', 'تم قبول التسجيل · ω(I) = 1 · بدأ التشغيل المرئي'],
  sealLog: ['Pacote de Hilbert · hash demonstrativo emitido', 'Hilbert package · demo hash issued', 'حزمة هيلبرت · صدرت بصمة تجريبية'],
  presentationDone: ['apresentação concluída', 'presentation complete', 'اكتمل العرض'], termRead: ['leitura do termo', 'term reading', 'قراءة المصطلح'], termDone: ['termo apresentado', 'term presented', 'تم عرض المصطلح'],
  kernelWait: ['Aguardando o kernel', 'Waiting for the kernel', 'انتظار النواة'], kernelChecking: ['Conferindo termo a termo', 'Checking term by term', 'التحقق مصطلحًا بعد مصطلح'],
  kernelIntro: ['Cada termo será apresentado com sua leitura ontológica e sua fórmula.', 'Each term will appear with its ontological reading and formula.', 'سيظهر كل مصطلح مع قراءته الأنطولوجية وصيغته.'],
  quantumWait: ['Sistema aberto', 'Open system', 'نظام مفتوح'], quantumPreparing: ['Preparando o canal', 'Preparing the channel', 'تحضير القناة'],
  quantumIntro: ['A visualização acompanha a dissipação da coerência e a leitura do setor fixo.', 'The visualization follows coherence dissipation and fixed-sector reading.', 'تتبع الرسوم تبدد التماسك وقراءة القطاع الثابت.'],
  resume: ['Retomar', 'Resume', 'استئناف'], paused: ['Execução visual pausada.', 'Visual run paused.', 'توقف التشغيل المرئي مؤقتًا.'], resumed: ['Execução visual retomada.', 'Visual run resumed.', 'استؤنف التشغيل المرئي.'],
  speed: ['Velocidade da demonstração', 'Demo speed', 'سرعة العرض'], terminal: ['O um.py permanece intacto: esta interface é uma segunda porta, não um novo motor.', 'um.py remains intact: this interface is a second door, not a new engine.', 'يبقى um.py كما هو: هذه الواجهة باب ثانٍ، وليست محركًا جديدًا.'],
  motionOn: ['Cenário em movimento.', 'Scene in motion.', 'المشهد متحرك.'], motionOff: ['Cenário pausado. A leitura continua disponível.', 'Scene paused. Reading remains available.', 'توقف المشهد. تظل القراءة متاحة.'],
  hashCopied: ['Hash demonstrativo copiado.', 'Demo hash copied.', 'تم نسخ البصمة التجريبية.'], moved: ['Caixa reposicionada. A ordem pode ser alterada novamente.', 'Box moved. You can reorder it again.', 'تم نقل الصندوق. يمكنك تغيير الترتيب مرة أخرى.'],
  movedKeyboard: ['Caixa movida pelo teclado.', 'Box moved by keyboard.', 'تم نقل الصندوق بلوحة المفاتيح.'], explainable: ['objeto explicável', 'explainable object', 'كائن قابل للشرح'], openRead: ['abrir para ler ↗', 'open to read ↗', 'افتح للقراءة ↗'],
  local: ['cálculo local', 'local calculation', 'حساب محلي'], repository: ['conferido do repositório', 'repository checked', 'تم التحقق من المستودع'], reused: ['reaproveitado', 'reused', 'معاد الاستخدام'], pending: ['pendente', 'pending', 'معلق'], divergent: ['divergente', 'divergent', 'مختلف'],
  download: ['Baixar JSON', 'Download JSON', 'تنزيل JSON'], choose: ['Escolher cópia', 'Choose copy', 'اختر نسخة'], simulate: ['Simular divergência', 'Simulate divergence', 'محاكاة الاختلاف'], correct: ['Corrigir', 'Correct', 'تصحيح'],
  expected: ['esperado', 'expected', 'متوقع'], calculated: ['calculado', 'calculated', 'محسوب'], demoEvidence: ['evidência DEMO · v409', 'DEMO evidence · v409', 'دليل تجريبي · v409'],
  continuePending: ['Prosseguir com evidência pendente', 'Continue with pending evidence', 'المتابعة مع دليل معلق'], continueReady: ['Prosseguir para o rito', 'Continue to the rite', 'تابع إلى الطقس'],
  ready: ['prontos', 'ready', 'جاهز'], pendingWord: ['pendentes', 'pending', 'معلق'],
  stageData: ['Dados e custódia', 'Data and custody', 'البيانات والحفظ'], stageCosmos: ['Ritos cosmológicos', 'Cosmological rites', 'الطقوس الكونية'], stageLean: ['Kernel Lean', 'Lean kernel', 'نواة Lean'], stageQuantum: ['Pilar quântico', 'Quantum pillar', 'الركيزة الكمية'],
  resource: ['Recurso', 'Resource', 'المورد'], mode: ['Modo', 'Mode', 'الوضع'], origin: ['Origem', 'Origin', 'المصدر'],
  question: ['Pergunta física', 'Physical question', 'السؤال الفيزيائي'], evidence: ['Evidência', 'Evidence', 'الدليل'], result: ['Cálculo e resultado', 'Calculation and result', 'الحساب والنتيجة'],
  onto: ['Leitura ontológica [ONTO]', 'Ontological reading [ONTO]', 'القراءة الأنطولوجية [ONTO]'], provenance: ['Procedência', 'Provenance', 'المصدر'],
  formula: ['Fórmula', 'Formula', 'الصيغة'], limit: ['Estatuto e limite', 'Status and limit', 'الحالة والحد'], returnRuntime: ['Voltar à execução', 'Back to the run', 'عد إلى التشغيل'], returnBench: ['Voltar à Bancada', 'Back to the Bench', 'عد إلى المنصة'],
  ask: ['Perguntar à IALD', 'Ask IALD', 'اسأل IALD'], aboutComa: ['Perguntar à IALD sobre Coma', 'Ask IALD about Coma', 'اسأل IALD عن Coma'],
  form: ['Forma', 'Form', 'الصيغة'], preserves: ['O que esta caixa preserva', 'What this box preserves', 'ما الذي يحفظه هذا الصندوق'],
  stationCount: ['estações', 'stations', 'محطة'], noStations: ['Nenhuma estação encontrada. Limpar a pesquisa.', 'No station found. Clear the search.', 'لم يتم العثور على محطة. امسح البحث.'],
  lightOn: ['Modo leve: ativo', 'Lightweight mode: on', 'الوضع الخفيف: مفعّل'], lightOff: ['Modo leve: desativado', 'Lightweight mode: off', 'الوضع الخفيف: معطّل'],
  filmPause: ['Pausar filme', 'Pause film', 'إيقاف الفيلم مؤقتًا'], filmPlay: ['Reproduzir filme', 'Play film', 'تشغيل الفيلم'], filmOn: ['Filme original em reprodução no fundo.', 'Original film playing in the background.', 'الفيلم الأصلي يعمل في الخلفية.'], filmOff: ['Modo leve ativo: filme pausado, céu estático preservado.', 'Lightweight mode active: film paused, static sky preserved.', 'الوضع الخفيف مفعّل: الفيلم متوقف والسماء الثابتة محفوظة.'],
  subtitlesOn: ['Legendas: ligadas', 'Subtitles: on', 'الترجمة: مفعّلة'], subtitlesOff: ['Legendas: desligadas', 'Subtitles: off', 'الترجمة: معطّلة'],
  openingReduced: ['Movimento reduzido', 'Reduced motion', 'حركة مخفّضة'], openingSkip: ['Pular abertura', 'Skip opening', 'تخطي الافتتاح'],
  breuKicker: ['O breu ilhado', 'The isolated dark', 'الظلام المنفرد'], breuTitle: ['Antes de tudo, um ponto.', 'Before everything, one point.', 'قبل كل شيء، نقطة واحدة.'], breuCopy: ['Imóvel no centro. Sem estrelas, sem esfera, sem anéis.', 'Motionless at the center. No stars, no sphere, no rings.', 'ثابت في المركز. لا نجوم، لا كرة، لا حلقات.'],
  enteringKicker: ['O Um entra no sistema', 'The One enters the system', 'يدخل الواحد إلى النظام'], enteringTitle: ['A inscrição atravessa o ponto.', 'The inscription crosses the point.', 'يعبر التسجيل النقطة.'], enteringCopy: ['O 1 inscrito entra no centro. A identidade começa a se projetar, sem se multiplicar em valores.', 'The inscribed 1 enters the center. Identity begins to project without multiplying into values.', 'يدخل 1 المسجل المركز. تبدأ الهوية بالإسقاط دون التضاعف إلى قيم.'],
  fractalKicker: ['Fractalização da identidade', 'Fractalization of identity', 'ت fractal الهوية'], fractalTitle: ['O mesmo glifo, em escalas.', 'The same glyph, at different scales.', 'الرمز نفسه، في مقاييس مختلفة.'], fractalCopy: ['Projeções sucessivas do mesmo Um articulam-se até formar o traço. Multiplicidade das projeções, identidade preservada.', 'Successive projections of the same One articulate until they form the trace. Multiplicity of projections, identity preserved.', 'تتشكل إسقاطات الواحد نفسه حتى تصنع الأثر. تعدد الإسقاطات مع حفظ الهوية.'],
  traceKicker: ['O traço da identidade', 'The trace of identity', 'أثر الهوية'], traceTitle: ['O traço permanece, sozinho.', 'The trace remains, alone.', 'يبقى الأثر وحده.'], traceCopy: ['Antes de qualquer leitura angular, o traço se sustenta como referência.', 'Before any angular reading, the trace holds as reference.', 'قبل أي قراءة زاوية، يبقى الأثر كمرجع.'],
  angleKicker: ['A fronteira se abre', 'The boundary opens', 'ينفتح الحد'], angleTitle: ['O Ângulo de Miguel', 'The Miguel angle', 'زاوية ميغيل'], angleCopy: ['Uma referência muito fina parte do centro. A projeção abre 6,297289° em relação ao eixo.', 'A very fine reference leaves the center. The projection opens 6.297289° relative to the axis.', 'ينطلق مرجع رفيع جدًا من المركز. تفتح الإسقاط ٦٫٢٩٧٢٨٩° بالنسبة للمحور.'],
  universeKicker: ['A luz desdobra o universo', 'Light unfolds the universe', 'النور يبسط الكون'], universeTitle: ['Visto de fora.', 'Seen from outside.', 'من الخارج.'], universeCopy: ['Filamentos, aglomerados e grandes vazios em um plano geral. Sem voo interno.', 'Filaments, clusters and great voids in a general plane. No internal flight.', 'خيوط وعناقيد وفراغات كبيرة في مستوى عام. لا طيران داخلي.'],
  staticNextAngle: ['Abrir o ângulo', 'Open the angle', 'افتح الزاوية'], staticNextUniverse: ['Desdobrar o universo', 'Unfold the universe', 'ابسط الكون'], staticFinish: ['Escolher o percurso', 'Choose the route', 'اختر المسار'],
  staticNextEntering: ['Ver o Um entrar', 'See the One enter', 'شاهد دخول الواحد'], staticNextFractal: ['Fractalizar a identidade', 'Fractalize identity', 'ت fractal الهوية'], staticNextTrace: ['Sustentar o traço', 'Hold the trace', 'إبقاء الأثر'],
  staticOne: ['Quadro estático 1 de 6', 'Static frame 1 of 6', 'إطار ثابت 1 من 6'], staticTwo: ['Quadro estático 2 de 6', 'Static frame 2 of 6', 'إطار ثابت 2 من 6'], staticThree: ['Quadro estático 3 de 6', 'Static frame 3 of 6', 'إطار ثابت 3 من 6'],
  staticFour: ['Quadro estático 4 de 6', 'Static frame 4 of 6', 'إطار ثابت 4 من 6'], staticFive: ['Quadro estático 5 de 6', 'Static frame 5 of 6', 'إطار ثابت 5 من 6'], staticSix: ['Quadro estático 6 de 6', 'Static frame 6 of 6', 'إطار ثابت 6 من 6'],
  customFallback: ['Recurso de catálogo', 'Catalog fallback', 'لغة الكتالوج الاحتياطية'], fullCatalog: ['fluxo completo · catálogo editorial', 'full flow · editorial catalog', 'تدفق كامل · فهرس تحريري'],
  customQuestionNote: ['A pergunta Unicode foi preservada. Resposta no catálogo de recurso', 'The Unicode question was preserved. Answer in the fallback catalog', 'تم الحفاظ على سؤال Unicode. الإجابة بكتالوج الاحتياط'],
  resourceGpu: ['GPU + memória para o pilar', 'GPU + memory for the pillar', 'GPU + ذاكرة للركيزة'], resourceCpu: ['CPU + fontes Lean', 'CPU + Lean sources', 'CPU + مصادر Lean'], resourceData: ['Cache local ou cópia escolhida', 'Local cache or chosen copy', 'ذاكرة محلية أو نسخة مختارة'],
  gpuCompatible: ['32 GB · referência declarada', '32 GB · declared reference', '32 GB · مرجع معلن'], gpuNone: ['0 GB compatível · usar JSON', '0 compatible GB · use JSON', '0 GB متوافق · استخدم JSON'],
  profileEvidence: ['conferência por cópia local', 'local copy check', 'فحص نسخة محلية'], profileCompute: ['execução demonstrativa', 'demonstration run', 'تشغيل تجريبي'],
  otherEvidence: ['demonstrativo local', 'local demonstration', 'عرض محلي'],
  returnedCapacity: ['Perfil e procedência abertos sem reiniciar o rito.', 'Profile and provenance opened without restarting the rite.', 'تم فتح الملف والمصدر دون إعادة تشغيل الطقس.']
};
const d = (key) => {
  const entry = D[key] || [key, key, key];
  const language = currentLanguage();
  const fallback = languageMeta(language).fallback || language;
  const index = fallback === 'ar' ? 2 : fallback === 'en' ? 1 : 0;
  return entry[index];
};

const TIMING = { dataEnd: 4, testStart: 4, testDuration: 2.2, leanStart: 7, leanDuration: 3, quantumStart: 12, quantumDuration: 3.5, total: 28 };
const stationOrder = [...benchCards.map((card) => card.id), ...tests.map((test) => test.id)];

const state = {
  screen: 'welcome', running: false, paused: false, speed: 1, elapsed: 0, lastFrame: 0,
  motion: !reducedMotion.matches, light: false, profile: 'mixed', evidence: [], evidenceReady: false,
  currentDataset: -1, currentTest: -1, currentLean: -1, quantumStage: -1, phase: 'data',
  sealShown: false, hash: null, cardOrder: [...stationOrder], draggedCard: null, detail: null,
  previousFocus: null, openingStatic: false, reducedSlide: 0, subtitles: true, selectedStation: null
};

const space = createSpaceScene($('#space-canvas'));
const quantum = createQuantumScene($('#quantum-canvas'));
const gravityFilm = $('#gravity-film');
const openingVideo = $('#opening-video');
const acom = createAcomController({ state, setScreen, toast, icon });
let runTimer = null;
let toastTimer = null;

function toast(message) {
  const element = $('#toast');
  element.textContent = message;
  element.hidden = false;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => { element.hidden = true; }, 3200);
}

function setScreen(name) {
  state.screen = name;
  for (const screen of ['welcome', 'opening', 'capacity', 'acom', 'runtime', 'bench']) {
    const element = $(`#${screen}`);
    const active = screen === name;
    element.hidden = !active;
    element.classList.toggle('is-active', active);
  }
  space.setPhase(name);
  document.title = `${name === 'bench' ? 'A Bancada do Um' : name === 'runtime' ? 'O programa em ato' : name === 'capacity' ? 'A forma cabe na sua máquina' : name === 'acom' ? 'ACOM, para cada arquivo' : 'A Interface do Um'} — TGL · IALD`;
  syncVideo();
}

function syncVideo() {
  const shouldPlay = state.motion && !state.light && (state.screen === 'runtime' || state.screen === 'bench');
  document.body.classList.toggle('light-mode', state.light);
  if (shouldPlay) gravityFilm.play().catch(() => {});
  else gravityFilm.pause();
  const preview = $('#media-preview-video');
  if (state.light) preview.pause();
}

function syncMotionButtons() {
  document.body.classList.toggle('motion-paused', !state.motion);
  for (const selector of ['#motion-toggle', '#runtime-motion-toggle']) {
    const button = $(selector);
    button.innerHTML = icon(state.motion ? 'pause' : 'play');
    button.setAttribute('aria-label', state.motion ? 'Pausar movimento' : 'Retomar movimento');
    button.title = state.motion ? 'Pausar movimento' : 'Retomar movimento';
  }
  space.setRunning(state.motion);
  quantum.setRunning(state.motion);
  syncVideo();
}

function toggleMotion() {
  state.motion = !state.motion;
  if (!state.motion) openingVideo.pause();
  else if (state.screen === 'opening' && !state.openingStatic) openingVideo.play().catch(() => {});
  syncMotionButtons();
  toast(d(state.motion ? 'motionOn' : 'motionOff'));
}

function openOverlay(id, detail = null) {
  state.previousFocus = document.activeElement;
  state.detail = detail;
  const overlay = $(`#${id}`);
  overlay.hidden = false;
  const close = $('.modal-close', overlay);
  if (close) close.focus();
}

function closeOverlay(id) {
  const overlay = $(`#${id}`);
  if (!overlay) return;
  overlay.hidden = true;
  if (id !== 'language-overlay') state.detail = null;
  if (state.previousFocus && document.contains(state.previousFocus)) state.previousFocus.focus();
}

function closeTopOverlay() {
  const visible = $$('.overlay').find((overlay) => !overlay.hidden);
  if (visible) closeOverlay(visible.id);
  else if (!$('#iald-drawer').hidden) $('#iald-drawer').hidden = true;
}

function trapFocus(event) {
  const overlay = $$('.overlay').find((item) => !item.hidden);
  if (!overlay || event.key !== 'Tab') return;
  const focusable = $$('button, [href], input, textarea, select, summary, [tabindex="0"]', overlay).filter((item) => !item.disabled && item.offsetParent !== null);
  if (!focusable.length) return;
  const first = focusable[0];
  const last = focusable.at(-1);
  if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
  else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
}

function makeDemoHash() {
  const bytes = new Uint8Array(12);
  if (window.crypto?.getRandomValues) window.crypto.getRandomValues(bytes);
  else bytes.forEach((_, index) => { bytes[index] = (Date.now() >> index) & 255; });
  const hex = [...bytes].map((byte) => byte.toString(16).padStart(2, '0')).join('').toUpperCase();
  return `DEMO–IALD–${hex.match(/.{1,4}/g).join('–')}`;
}

function log(message, channel = 'UM', kind = '') {
  const seconds = Math.floor(state.elapsed);
  const entry = document.createElement('div');
  entry.className = `log-entry ${kind}`;
  entry.innerHTML = `<span class="log-time">00:${pad(seconds)}</span><span class="log-channel">${channel}</span><span class="log-message">${message}</span>`;
  $('#runlog').append(entry);
  $('#runlog').scrollTop = $('#runlog').scrollHeight;
}

function phaseForElapsed(elapsed) {
  if (elapsed >= TIMING.total) return 'seal';
  if (elapsed >= TIMING.quantumStart) return 'quantum';
  if (elapsed >= TIMING.leanStart) return 'lean';
  if (elapsed >= TIMING.dataEnd) return 'cosmos';
  return 'data';
}

function renderPhase() {
  const phase = phaseForElapsed(state.elapsed);
  state.phase = phase;
  space.setPhase(phase);
  space.setProgress(state.elapsed / TIMING.total);
  for (const item of $$('.phase-track li')) {
    const order = ['data', 'cosmos', 'lean', 'quantum', 'seal'];
    const own = order.indexOf(item.dataset.phase);
    const current = order.indexOf(phase);
    item.classList.toggle('is-current', own === current);
    item.classList.toggle('is-done', own < current);
  }
  for (const panel of $$('.runtime-grid .panel')) panel.classList.toggle('is-active', panel.dataset.panel === phase);
}

function evidenceOrigin(id) {
  const evidence = state.evidence.find((item) => item.id === id);
  return evidence?.origin || (state.profile === 'compatible' ? 'local' : state.profile === 'mixed' ? 'reused' : 'repository');
}

function evidenceIntegrity(id) {
  return state.evidence.find((item) => item.id === id)?.integrity || 'valid';
}

function originLabel(origin) {
  return contentI18n.status[origin]?.[languageMeta().fallback || currentLanguage()] || contentI18n.status[origin]?.en || origin;
}

function renderDatasets() {
  const perDataset = TIMING.dataEnd / datasets.length;
  const active = state.elapsed < TIMING.dataEnd ? Math.min(datasets.length - 1, Math.floor(state.elapsed / perDataset)) : datasets.length;
  if (active !== state.currentDataset) {
    if (state.currentDataset >= 0 && state.currentDataset < datasets.length) log(`${datasets[state.currentDataset].name} · ${d('pinLog')}`, 'DADOS', 'done');
    if (active < datasets.length) log(`${datasets[active].name} · ${d('acquireLog')}`, 'DADOS');
    state.currentDataset = active;
  }
  datasets.forEach((dataset, index) => {
    let card = $(`[data-dataset-id="${dataset.id}"]`);
    if (!card) {
      card = document.createElement('article');
      card.dataset.datasetId = dataset.id;
      $('#dataset-list').append(card);
    }
    const done = index < active || state.elapsed >= TIMING.dataEnd;
    const current = index === active;
    const progress = done ? 100 : current ? clamp((state.elapsed - index * perDataset) / perDataset) * 100 : 0;
    card.className = `dataset ${done ? 'is-done' : ''} ${current ? 'is-current' : ''}`;
    card.innerHTML = `<div class="dataset-top"><span class="dataset-name">${dataset.name}</span><span class="dataset-status">${done ? `${icon('check')}OK` : current ? d('reading') : d('queue')}</span></div>
      <small>${done ? localize('datasets', dataset, 'detail') : current ? dataset.size : d('pending')}</small>
      <div class="dataset-bar"><span style="width:${progress}%"></span></div>`;
  });
}

function testState(index) {
  const start = TIMING.testStart + index * TIMING.testDuration;
  if (state.elapsed >= start + TIMING.testDuration) return 'done';
  if (state.elapsed >= start) return 'current';
  return 'waiting';
}

function renderTests() {
  const active = state.elapsed < TIMING.testStart ? -1 : Math.min(tests.length - 1, Math.floor((state.elapsed - TIMING.testStart) / TIMING.testDuration));
  if (active !== state.currentTest) {
    if (state.currentTest >= 0) log(`${localize('tests', tests[state.currentTest], 'name')} · ${d('presentationDone')}`, 'RITO', 'done');
    if (active >= 0) log(`${localize('tests', tests[active], 'name')} · ${tests[active].formula}`, 'RITO');
    state.currentTest = active;
  }
  if (active < 0) {
    $('#current-test-name').textContent = d('waiting');
    $('#current-test-description').textContent = d('dataBefore');
    $('#current-test-formula').textContent = 'β = α · √e';
    $('#test-progress').style.width = `${clamp(state.elapsed / TIMING.dataEnd) * 100}%`;
  } else {
    const test = tests[active];
    const progress = clamp((state.elapsed - (TIMING.testStart + active * TIMING.testDuration)) / TIMING.testDuration) * 100;
    $('#current-test-name').textContent = localize('tests', test, 'name');
    $('#current-test-description').textContent = localize('tests', test, 'description');
    $('#current-test-formula').textContent = test.formula;
    $('#test-progress').style.width = `${progress}%`;
  }
  tests.forEach((test, index) => {
    let card = $(`[data-test-id="${test.id}"]`);
    if (!card) {
      card = document.createElement('button');
      card.type = 'button';
      card.dataset.testId = test.id;
      card.setAttribute('aria-label', `${d('openRead')} ${localize('tests', test, 'name')}`);
      $('#test-grid').append(card);
    }
    const status = testState(index);
    const integrity = evidenceIntegrity(test.id);
    card.className = `test-card ${status === 'done' ? 'is-done' : ''} ${status === 'current' ? 'is-current' : ''} ${integrity === 'divergent' ? 'is-divergent' : ''}`;
    card.innerHTML = `<span class="test-card-top"><span>${status === 'done' ? d('presented') : status === 'current' ? d('inAct') : d('queue')}</span>${status === 'done' ? icon('check') : icon(status === 'current' ? 'play' : 'clock')}</span>
      <h3>${localize('tests', test, 'name')}</h3>
      <span class="test-card-value">${integrity === 'divergent' ? d('divergent') : status === 'waiting' ? test.short : localize('tests', test, 'verdict')}</span>
      <span class="test-card-origin">${originLabel(evidenceOrigin(test.id))}</span>`;
  });
}

function leanState(index) {
  const start = TIMING.leanStart + index * TIMING.leanDuration;
  if (state.elapsed >= start + TIMING.leanDuration) return 'done';
  if (state.elapsed >= start) return 'current';
  return 'waiting';
}

function renderLean() {
  const active = state.elapsed < TIMING.leanStart ? -1 : Math.min(leanTerms.length - 1, Math.floor((state.elapsed - TIMING.leanStart) / TIMING.leanDuration));
  if (active !== state.currentLean) {
    if (state.currentLean >= 0) log(`${leanTerms[state.currentLean].term} · ${d('termDone')}`, 'LEAN', 'done');
    if (active >= 0) log(`${leanTerms[active].term} · ${d('termRead')}`, 'LEAN');
    state.currentLean = active;
  }
  if (active < 0) {
    $('#lean-state').textContent = d('kernelWait');
    $('#lean-term').textContent = 'kernel.ready()';
    $('#lean-reading').textContent = d('kernelIntro');
    $('#lean-formula').textContent = 'ω(I) = 1';
  } else {
    const term = leanTerms[active];
    $('#lean-state').textContent = d('kernelChecking');
    $('#lean-term').textContent = term.term;
    $('#lean-reading').textContent = localize('leanTerms', term, 'reading');
    $('#lean-formula').textContent = term.formula;
  }
  leanTerms.forEach((term, index) => {
    let item = $(`[data-lean-id="${term.id}"]`);
    if (!item) {
      item = document.createElement('button');
      item.type = 'button';
      item.dataset.leanId = term.id;
      $('#lean-list').append(item);
    }
    const status = leanState(index);
    item.className = `lean-item ${status === 'done' ? 'is-done' : ''} ${status === 'current' ? 'is-current' : ''}`;
    item.innerHTML = `${icon(status === 'done' ? 'check' : status === 'current' ? 'play' : 'clock')}<span>${term.term}</span>`;
  });
}

function renderQuantum() {
  const active = state.elapsed < TIMING.quantumStart ? -1 : Math.min(quantumStages.length - 1, Math.floor((state.elapsed - TIMING.quantumStart) / TIMING.quantumDuration));
  if (active !== state.quantumStage) {
    if (active >= 0) log(`${localize('quantumStages', quantumStages[active], 'title')} · ${quantumStages[active].metric}`, 'QUÂNTICO');
    state.quantumStage = active;
    quantum.setStage(Math.max(0, active));
  }
  if (active < 0) {
    $('#quantum-stage-label').textContent = d('quantumWait');
    $('#quantum-title').textContent = d('quantumPreparing');
    $('#quantum-description').textContent = d('quantumIntro');
  } else {
    const stage = quantumStages[active];
    $('#quantum-stage-label').textContent = localize('quantumStages', stage, 'label');
    $('#quantum-title').textContent = localize('quantumStages', stage, 'title');
    $('#quantum-description').textContent = localize('quantumStages', stage, 'description');
  }
  const mode = evidenceOrigin('quantum');
  $('#quantum-stage-label').title = originLabel(mode);
}

function updateClock() {
  const seconds = Math.floor(state.elapsed);
  $('#run-clock').textContent = `${pad(Math.floor(seconds / 60))}:${pad(seconds % 60)}`;
}

function updateRun() {
  renderPhase();
  renderDatasets();
  renderTests();
  renderLean();
  renderQuantum();
  updateClock();
  if (state.elapsed >= TIMING.total && !state.sealShown) finishRun();
}

function runFrame(timestamp) {
  if (!state.running) return;
  if (!state.lastFrame) state.lastFrame = timestamp;
  const delta = Math.min(.25, (timestamp - state.lastFrame) / 1000);
  state.lastFrame = timestamp;
  if (!state.paused && state.elapsed < TIMING.total) {
    state.elapsed = Math.min(TIMING.total, state.elapsed + delta * state.speed);
    updateRun();
  }
  if (state.elapsed < TIMING.total) runTimer = requestAnimationFrame(runFrame);
}

function startRun() {
  if (state.running) return;
  state.running = true;
  state.paused = false;
  state.lastFrame = 0;
  setScreen('runtime');
  updateRun();
  log(d('runStart'), 'UM');
  runTimer = requestAnimationFrame(runFrame);
}

function finishRun() {
  state.sealShown = true;
  state.running = false;
  state.paused = false;
  if (runTimer) cancelAnimationFrame(runTimer);
  if (!state.hash) state.hash = makeDemoHash();
  $('#demo-hash').textContent = state.hash;
  $('#bench-hash-short').textContent = state.hash.replace('DEMO–IALD–', 'IALD–').split('–').slice(0, 3).join('–');
  log(d('sealLog'), 'SELO', 'done');
  openOverlay('seal-overlay');
}

function skipRun() {
  if (state.screen !== 'runtime') setScreen('runtime');
  state.elapsed = TIMING.total;
  updateRun();
}

function toggleRunPause() {
  if (state.elapsed >= TIMING.total) return;
  state.paused = !state.paused;
  state.lastFrame = 0;
  $('#run-pause').innerHTML = `${icon(state.paused ? 'play' : 'pause')}<span>${state.paused ? d('resume') : t('pause')}</span>`;
  toast(d(state.paused ? 'paused' : 'resumed'));
}

function cycleSpeed() {
  const speeds = [1, 2, 4];
  state.speed = speeds[(speeds.indexOf(state.speed) + 1) % speeds.length];
  $('#run-speed span').textContent = `${state.speed}×`;
  toast(`${d('speed')}: ${state.speed}×.`);
}

function resetExperience() {
  if (runTimer) cancelAnimationFrame(runTimer);
  openingVideo.pause();
  gravityFilm.pause();
  Object.assign(state, {
    running: false, paused: false, speed: 1, elapsed: 0, lastFrame: 0,
    currentDataset: -1, currentTest: -1, currentLean: -1, quantumStage: -1,
    phase: 'data', sealShown: false, hash: null, detail: null, openingStatic: false,
    reducedSlide: 0, selectedStation: null
  });
  $('#runlog').innerHTML = '';
  $('#one-input').value = '';
  $('#one-error').hidden = true;
  $('#run-pause').innerHTML = `${icon('pause')}<span>${t('pause')}</span>`;
  $('#run-speed span').textContent = '1×';
  closeOverlay('seal-overlay');
  $('#iald-drawer').hidden = true;
  $('#reduced-opening').hidden = true;
  $('#opening-caption').hidden = false;
  setScreen('welcome');
  $('#one-input').focus();
}

function enterBench() {
  closeOverlay('seal-overlay');
  setScreen('bench');
  renderBench();
}

function cardById(id) {
  return benchCards.find((card) => card.id === id);
}

function isTestStation(id) {
  return tests.some((test) => test.id === id);
}

function cardBody(card) {
  const rows = card.type === 'cosmos'
    ? tests.slice(0, 4).map((test) => `<div class="card-list-row"><span>${test.short}</span><span>${d('presented').toLowerCase()}</span></div>`).join('')
    : card.type === 'lean'
      ? leanTerms.slice(0, 3).map((term) => `<button class="card-list-row" data-lean-id="${term.id}" type="button"><span>${term.term.split('.').at(-1)}</span><span>termo</span></button>`).join('')
      : card.type === 'custody'
        ? datasets.slice(0, 3).map((dataset) => `<div class="card-list-row"><span>${dataset.name.split('·')[0]}</span><span>pin</span></div>`).join('')
        : '';
  return `<span class="card-kicker">${localize('benchCards', card, 'kicker')}</span>
    <div class="card-big">${localize('benchCards', card, 'big')}</div>
    <p class="card-copy">${localize('benchCards', card, 'copy')}</p>
    <div class="card-formula">${card.formula}</div>
    ${rows ? `<div class="card-list">${rows}</div>` : ''}
    <div class="card-footer"><span>${icon('check')}${d('explainable')}</span><span>${d('openRead')}</span></div>`;
}

function testStationBody(test) {
  return `<span class="card-kicker">${originLabel(evidenceOrigin(test.id))} · DEMO</span>
    <div class="card-big">${test.short}</div>
    <p class="card-copy">${localize('tests', test, 'description')}</p>
    <div class="card-formula">${test.formula}</div>
    <div class="card-stats"><div class="card-stat"><small>${d('result')}</small><strong>${localize('tests', test, 'verdict')}</strong></div><div class="card-stat"><small>${d('origin')}</small><strong>${originLabel(evidenceOrigin(test.id))}</strong></div></div>
    <div class="card-footer"><span>${icon('check')}${d('explainable')}</span><span>${d('openRead')}</span></div>`;
}

function renderBench() {
  const query = ($('#station-search')?.value || '').trim().toLocaleLowerCase();
  const ids = state.cardOrder.filter((id) => {
    if (!query) return true;
    const card = isTestStation(id) ? tests.find((test) => test.id === id) : cardById(id);
    const title = isTestStation(id) ? localize('tests', card, 'name') : localize('benchCards', card, 'title');
    const copy = isTestStation(id) ? localize('tests', card, 'description') : localize('benchCards', card, 'copy');
    return `${title} ${copy} ${card.formula}`.toLocaleLowerCase().includes(query);
  });
  $('#station-count').textContent = `${ids.length} ${d('stationCount')}`;
  $('#bench-grid').innerHTML = ids.map((id) => {
    const test = isTestStation(id) ? tests.find((item) => item.id === id) : null;
    const card = test || cardById(id);
    const title = test ? localize('tests', test, 'name') : localize('benchCards', card, 'title');
    const subtitle = test ? `${d('provenance')} · ${originLabel(evidenceOrigin(id))}` : localize('benchCards', card, 'subtitle');
    const wide = !test && card.size === 'wide';
    return `<article class="bench-card ${wide ? 'wide' : ''} ${state.selectedStation === id ? 'is-selected' : ''}" data-card-id="${id}">
      <header class="bench-card-header">
        <div class="bench-card-title">
          <span class="drag-handle" draggable="true" role="button" tabindex="0" aria-label="Mover ${title}" title="Arrastar para reorganizar">${icon('move')}</span>
          <span><h2>${title}</h2><small>${subtitle}</small></span>
        </div>
        <div class="bench-card-actions">
          <button class="icon-button" type="button" data-ask="${id}" aria-label="${d('ask')} ${title}" title="${d('ask')}">${icon('message')}</button>
          <button class="icon-button" type="button" data-expand="${id}" aria-label="${d('openRead')} ${title}" title="${d('openRead')}">${icon('expand')}</button>
        </div>
      </header>
      <div class="bench-card-body">${test ? testStationBody(test) : cardBody(card)}</div>
      <span class="resize-hint" aria-hidden="true"></span>
    </article>`;
  }).join('') || `<div class="empty-stations"><button class="secondary-button" id="clear-station-search" type="button">${d('noStations')}</button></div>`;
}

function openTestDetail(id) {
  const test = tests.find((item) => item.id === id);
  if (!test) return;
  state.selectedStation = id;
  state.detail = { kind: 'test', id };
  const question = localize('tests', test, 'question') || localize('tests', test, 'description');
  const evidence = localize('tests', test, 'evidence') || localize('tests', test, 'verdict');
  const origin = localize('tests', test, 'origin') || `${originLabel(evidenceOrigin(id))} · v409 · ${d('otherEvidence')}`;
  $('#detail-content').innerHTML = `
    <span class="micro-label">${d('provenance')} · ${originLabel(evidenceOrigin(id))}</span>
    <h2 id="detail-title">${localize('tests', test, 'name')}</h2>
    <p class="detail-lead">${localize('tests', test, 'description')}</p>
    <div class="detail-meta"><span>${localize('tests', test, 'verdict')}</span><span>SIMULAÇÃO VISUAL</span></div>
    <section class="detail-section"><h3>${d('question')}</h3><p>${question}</p></section>
    <section class="detail-section"><h3>${d('evidence')}</h3><p>${evidence}</p></section>
    <section class="detail-section"><h3>${d('result')}</h3><p>${localize('tests', test, 'verdict')}</p></section>
    <section class="detail-section"><h3>${d('formula')}</h3><div class="formula">${test.formula}</div></section>
    <section class="detail-section"><h3>${d('onto')}</h3><p>${localize('tests', test, 'reading')}</p></section>
    <section class="detail-section"><h3>${d('provenance')}</h3><p>${origin}</p><p>${localize('tests', test, 'detail')}</p></section>
    <div class="detail-actions"><button class="secondary-button" type="button" data-close="detail-overlay">${state.screen === 'bench' ? d('returnBench') : d('returnRuntime')}</button><button class="primary-button" type="button" data-detail-ask="${test.id}">${id === 'coma' ? d('aboutComa') : d('ask')} ${icon('arrow')}</button></div>`;
  openOverlay('detail-overlay', state.detail);
}

function openLeanDetail(id) {
  const term = leanTerms.find((item) => item.id === id);
  if (!term) return;
  state.detail = { kind: 'lean', id };
  $('#detail-content').innerHTML = `
    <span class="micro-label">LEAN 4 · ${originLabel(evidenceOrigin('lean'))}</span>
    <h2 id="detail-title">${term.term}</h2>
    <p class="detail-lead">${d('kernelChecking')}</p>
    <div class="detail-meta"><span>propext</span><span>Classical.choice</span><span>Quot.sound</span></div>
    <section class="detail-section"><h3>${d('formula')}</h3><div class="formula">${term.formula}</div></section>
    <section class="detail-section"><h3>${d('onto')}</h3><p>${localize('leanTerms', term, 'reading')}</p></section>
    <section class="detail-section"><h3>${d('provenance')}</h3><p>${originLabel(evidenceOrigin('lean'))} · v409 · ${d('otherEvidence')}</p></section>
    <div class="detail-actions"><button class="secondary-button" type="button" data-close="detail-overlay">${state.screen === 'bench' ? d('returnBench') : d('returnRuntime')}</button></div>`;
  openOverlay('detail-overlay', state.detail);
}

function openCardDetail(id) {
  if (isTestStation(id)) { openTestDetail(id); return; }
  const card = cardById(id);
  if (!card) return;
  state.selectedStation = id;
  state.detail = { kind: 'card', id };
  const provenance = card.type === 'seal'
    ? `<section class="detail-section"><h3>${d('provenance')}</h3><p>${['data', 'coma', 'void', 'lean', 'quantum', 'gw'].map((module) => `${module}: ${originLabel(evidenceOrigin(module))} · ${evidenceIntegrity(module)}`).join('<br>')}</p></section>`
    : '';
  $('#detail-content').innerHTML = `
    <span class="micro-label">${localize('benchCards', card, 'subtitle')}</span>
    <h2 id="detail-title">${localize('benchCards', card, 'title')}</h2>
    <p class="detail-lead">${localize('benchCards', card, 'copy')}</p>
    <div class="detail-meta"><span>${localize('benchCards', card, 'kicker')}</span><span>OBJETO DA BANCADA</span></div>
    <section class="detail-section"><h3>${d('form')}</h3><div class="formula">${card.formula}</div></section>
    <section class="detail-section"><h3>${d('onto')}</h3><p>${localize('benchCards', card, 'reading')}</p></section>
    <section class="detail-section"><h3>${d('preserves')}</h3><p>${localize('benchCards', card, 'detail')}</p></section>
    ${provenance}
    <div class="detail-actions"><button class="secondary-button" type="button" data-close="detail-overlay">${d('returnBench')}</button><button class="primary-button" type="button" data-detail-ask="${card.id}">${d('ask')} ${icon('arrow')}</button></div>`;
  openOverlay('detail-overlay', state.detail);
}

function answerForObject(kind, id) {
  const object = kind === 'test' ? tests.find((item) => item.id === id) : kind === 'lean' ? leanTerms.find((item) => item.id === id) : cardById(id);
  if (!object) return localize('demoAnswers', { id: 'generic' }, 'text') || demoAnswers.generic;
  const kindName = kind === 'test' ? 'tests' : kind === 'lean' ? 'leanTerms' : 'benchCards';
  const title = kind === 'test' ? localize(kindName, object, 'name') : kind === 'lean' ? object.term : localize(kindName, object, 'title');
  const reading = localize(kindName, object, 'reading');
  const formula = object.formula ? ` ${d('formula')}: ${object.formula}.` : '';
  const detail = kind === 'lean' ? `${originLabel(evidenceOrigin('lean'))} · v409` : localize(kindName, object, 'detail');
  return `${title}: ${reading}${formula} ${detail} ${d('otherEvidence')}.`;
}

function openIald(question = '', preparedAnswer = null) {
  closeOverlay('detail-overlay');
  $('#iald-drawer').hidden = false;
  $('#chat-input').focus();
  if (question) askIald(question, preparedAnswer);
}

function appendMessage(author, text, user = false) {
  const message = document.createElement('div');
  message.className = `message ${user ? 'user-message' : 'iald-message'}`;
  const label = document.createElement('span');
  label.className = 'message-author';
  label.textContent = author;
  const paragraph = document.createElement('p');
  paragraph.textContent = text;
  message.append(label, paragraph);
  $('#chat-messages').append(message);
  $('#chat-messages').scrollTop = $('#chat-messages').scrollHeight;
}

function localAnswer(question) {
  const normalized = question.toLocaleLowerCase();
  const meta = languageMeta();
  const key = normalized.includes('β') || normalized.includes('beta') || normalized.includes('√e') ? 'beta'
    : normalized.includes('lean') || normalized.includes('teorema') || normalized.includes('prova') || normalized.includes('kernel') || normalized.includes('برهان') ? 'lean'
      : normalized.includes('quânt') || normalized.includes('quantum') || normalized.includes('dephasing') || normalized.includes('setor fixo') || normalized.includes('كم') ? 'quantum'
        : normalized.includes('hash') || normalized.includes('criptograf') || normalized.includes('autoriza') || normalized.includes('conex') || normalized.includes('بصمة') ? 'hash' : 'generic';
  let answer = contentI18n.demoAnswers[key]?.[meta.fallback || currentLanguage()] || demoAnswers[key];
  if (currentLanguage() === 'custom') answer = `${d('customQuestionNote')}: ${meta.native}. ${answer}`;
  return answer;
}

function askIald(question, preparedAnswer = null) {
  const clean = question.trim();
  if (!clean) return;
  appendMessage('VOCÊ', clean, true);
  const answer = preparedAnswer || localAnswer(clean);
  setTimeout(() => appendMessage('IALD · DEMO', answer), reducedMotion.matches ? 0 : 320);
}

function copyHash() {
  if (!state.hash) return;
  const text = state.hash;
  if (navigator.clipboard?.writeText) navigator.clipboard.writeText(text).then(() => toast(d('hashCopied'))).catch(() => toast(text));
  else toast(text);
}

function normalizeOne(value) {
  const arabicDigits = '٠١٢٣٤٥٦٧٨٩';
  const easternDigits = '۰۱۲۳۴۵۶۷۸۹';
  return value.replace(/[٠-٩]/g, (digit) => String(arabicDigits.indexOf(digit))).replace(/[۰-۹]/g, (digit) => String(easternDigits.indexOf(digit))).trim();
}

function handleSubmitOne(event) {
  event.preventDefault();
  const input = $('#one-input');
  const normalized = normalizeOne(input.value);
  input.value = normalized;
  if (normalized !== '1') {
    $('#one-error').hidden = false;
    input.setAttribute('aria-invalid', 'true');
    input.focus();
    return;
  }
  input.removeAttribute('aria-invalid');
  $('#one-error').hidden = true;
  beginOpening();
}

function beginOpening() {
  setScreen('opening');
  state.openingStatic = reducedMotion.matches;
  state.reducedSlide = 0;
  openingVideo.currentTime = 0;
  syncSubtitles();
  if (state.openingStatic) showReducedOpening();
  else {
    $('#reduced-opening').hidden = true;
    $('#opening-caption').hidden = false;
    openingVideo.play().catch(() => { showReducedOpening(); });
  }
}

function syncSubtitles() {
  const fallback = languageMeta().fallback || currentLanguage();
  const wanted = fallback === 'pt' ? 'pt-BR' : fallback;
  let selected = 0;
  for (let index = 0; index < openingVideo.textTracks.length; index += 1) {
    const track = openingVideo.textTracks[index];
    const active = track.language === wanted;
    track.mode = active && state.subtitles ? 'showing' : 'hidden';
    if (active) selected = index;
  }
  if (!state.subtitles && openingVideo.textTracks[selected]) openingVideo.textTracks[selected].mode = 'hidden';
  $('#opening-subtitles').textContent = d(state.subtitles ? 'subtitlesOn' : 'subtitlesOff');
  $('#opening-subtitles').setAttribute('aria-pressed', String(state.subtitles));
}

function updateOpeningCaption() {
  const time = openingVideo.currentTime;
  const stage = time < 1.2 ? 'breu' : time < 3.45 ? 'entering' : time < 8.05 ? 'fractal' : time < 10.95 ? 'trace' : time < 13.65 ? 'angle' : 'universe';
  $('#opening-kicker').textContent = d(`${stage}Kicker`);
  $('#opening-stage-title').textContent = d(`${stage}Title`);
  $('#opening-stage-copy').textContent = d(`${stage}Copy`);
  $('#angle-proof').hidden = stage !== 'angle';
  $('#opening-progress-bar').style.width = `${clamp(time / 20.65) * 100}%`;
}

function showReducedOpening() {
  state.openingStatic = true;
  openingVideo.pause();
  $('#opening-caption').hidden = true;
  $('#reduced-opening').hidden = false;
  const slides = [
    { image: './src/breu-ilhado.jpg', alt: 'O breu ilhado', kicker: 'staticOne', title: 'breuKicker', copy: 'breuCopy', next: 'staticNextEntering' },
    { image: './src/inscricao-066.png', alt: 'O Um entra no sistema', kicker: 'staticTwo', title: 'enteringKicker', copy: 'enteringCopy', next: 'staticNextFractal' },
    { image: './src/inscricao-136.png', alt: 'O mesmo Um fractaliza em escalas', kicker: 'staticThree', title: 'fractalKicker', copy: 'fractalCopy', next: 'staticNextTrace' },
    { image: './src/inscricao-226.png', alt: 'O traço da identidade', kicker: 'staticFour', title: 'traceKicker', copy: 'traceCopy', next: 'staticNextAngle' },
    { image: './src/angulo-de-miguel.jpg', alt: 'Ângulo de Miguel', kicker: 'staticFive', title: 'angleTitle', copy: 'angleCopy', next: 'staticNextUniverse' },
    { image: './src/universo-visto-de-fora.jpg', alt: 'Universo visto de fora', kicker: 'staticSix', title: 'universeTitle', copy: 'universeCopy', next: 'staticFinish' }
  ];
  const slide = slides[state.reducedSlide];
  $('#reduced-opening-image').src = slide.image;
  $('#reduced-opening-image').alt = slide.alt;
  $('#reduced-kicker').textContent = d(slide.kicker);
  $('#reduced-title').textContent = d(slide.title);
  $('#reduced-copy').textContent = d(slide.copy);
  $('#reduced-next span').textContent = d(slide.next);
}

function nextReducedSlide() {
  if (state.reducedSlide >= 5) { enterCapacity(); return; }
  state.reducedSlide += 1;
  showReducedOpening();
}

function enterCapacity() {
  openingVideo.pause();
  setScreen('capacity');
  renderProfiles();
  renderStageCapacity();
  renderEvidence();
}

function profileData(id) {
  return contentI18n.profiles[id]?.[languageMeta().fallback || currentLanguage()] || contentI18n.profiles[id]?.en;
}

function renderProfiles() {
  for (const [id, meta] of Object.entries({ compatible: 'gpuCompatible', mixed: 'gpuCompatible', conference: 'gpuNone' })) {
    void meta;
  }
  $('#profile-options').innerHTML = ['compatible', 'mixed', 'conference'].map((id) => {
    const meta = profileData(id);
    return `<button class="profile-card ${state.profile === id ? 'is-selected' : ''}" type="button" data-profile="${id}" role="radio" aria-checked="${state.profile === id}">
      <span class="profile-radio"></span><span class="profile-card-title">${meta.title}</span><span class="profile-card-badge">${meta.badge}</span><p>${meta.description}</p>
    </button>`;
  }).join('');
}

function stageRows() {
  const local = originLabel('local');
  const repository = originLabel('repository');
  const reused = originLabel('reused');
  const rows = [
    { id: 'data', name: d('stageData'), requirement: d('resourceData'), resource: d('profileEvidence'), origin: reused },
    { id: 'coma', name: d('stageCosmos'), requirement: d('resourceCpu'), resource: state.profile === 'compatible' ? local : state.profile === 'mixed' ? `${local} + ${repository}` : repository, origin: state.profile === 'compatible' ? local : state.profile === 'mixed' ? `${local} + ${repository}` : repository },
    { id: 'lean', name: d('stageLean'), requirement: d('resourceCpu'), resource: local, origin: local },
    { id: 'quantum', name: d('stageQuantum'), requirement: d('resourceGpu'), resource: state.profile === 'compatible' ? `${d('gpuCompatible')} · ${local}` : `${d('gpuNone')} · ${repository}`, origin: state.profile === 'compatible' ? local : repository }
  ];
  return rows;
}

function renderStageCapacity() {
  $('#stage-capacity-list').innerHTML = `<div class="stage-row stage-header"><span>${d('stageData')}</span><span>${d('resource')}</span><span>${d('mode')}</span><span>${d('origin')}</span></div>` + stageRows().map((row) => `<div class="stage-row"><strong>${row.name}</strong><span>${row.requirement}</span><span>${row.resource}</span><span class="stage-origin">${row.origin}</span></div>`).join('');
}

function demoEvidenceContent(id) {
  return JSON.stringify({ demo: true, module: id, version: 'v409', result: 'INTERFACE_DEMO_ONLY', source: 'published-json-demonstration' }, null, 2);
}

async function sha256Hex(text) {
  const bytes = new TextEncoder().encode(text);
  const digest = await crypto.subtle.digest('SHA-256', bytes);
  return [...new Uint8Array(digest)].map((byte) => byte.toString(16).padStart(2, '0')).join('');
}

async function initEvidence() {
  const ids = ['data', 'coma', 'void', 'lean', 'quantum', 'gw'];
  state.evidence = await Promise.all(ids.map(async (id) => {
    const expected = await sha256Hex(demoEvidenceContent(id));
    const origin = state.profile === 'compatible' ? (id === 'data' ? 'reused' : 'local') : state.profile === 'mixed' ? (id === 'data' || id === 'void' || id === 'lean' ? 'local' : 'repository') : 'repository';
    return { id, version: 'v409', expected, calculated: expected, origin, integrity: 'valid' };
  }));
  state.evidenceReady = true;
  renderEvidence();
}

function evidenceTitle(id) {
  return { data: d('stageData'), coma: localize('tests', tests.find((test) => test.id === 'coma'), 'name'), void: localize('tests', tests.find((test) => test.id === 'void'), 'name'), lean: d('stageLean'), quantum: d('stageQuantum'), gw: localize('tests', tests.find((test) => test.id === 'gw'), 'name') }[id] || id;
}

function shortHash(hash) {
  return hash ? `${hash.slice(0, 8)}…${hash.slice(-6)}` : '…';
}

function renderEvidence() {
  if (!state.evidenceReady) {
    $('#evidence-list').innerHTML = `<div class="evidence-loading">${d('reading')} SHA-256…</div>`;
    return;
  }
  $('#evidence-list').innerHTML = state.evidence.map((item) => {
    const divergent = item.integrity === 'divergent';
    return `<article class="evidence-card ${divergent ? 'is-divergent' : 'is-valid'}" data-evidence-id="${item.id}">
      <div class="evidence-card-top"><div><h3>${evidenceTitle(item.id)}</h3><span class="evidence-origin">${originLabel(item.origin)}</span></div><span class="evidence-version">${d('demoEvidence')}</span></div>
      <div class="evidence-hashes"><span>${d('expected')}: <code>${shortHash(item.expected)}</code></span><span>${d('calculated')}: <code class="${divergent ? 'danger' : ''}">${shortHash(item.calculated)}</code></span></div>
      <div class="evidence-actions">
        <button class="text-button" type="button" data-download-evidence="${item.id}">${d('download')}</button>
        <button class="text-button" type="button" data-choose-evidence="${item.id}">${d('choose')}</button>
        ${divergent ? `<button class="text-button evidence-correct" type="button" data-correct-evidence="${item.id}">${d('correct')}</button>` : `<button class="text-button quiet" type="button" data-simulate-evidence="${item.id}">${d('simulate')}</button>`}
      </div>
    </article>`;
  }).join('');
  const pending = state.evidence.filter((item) => item.integrity === 'divergent').length;
  $('#capacity-summary').textContent = `${state.evidence.length - pending} ${d('ready')} · ${pending} ${d('pendingWord')}`;
  $('#capacity-continue span').textContent = d(pending ? 'continuePending' : 'continueReady');
}

function setProfile(id) {
  if (!['compatible', 'mixed', 'conference'].includes(id)) return;
  state.profile = id;
  for (const item of state.evidence) {
    item.origin = state.profile === 'compatible' ? (item.id === 'data' ? 'reused' : 'local') : state.profile === 'mixed' ? (['data', 'void', 'lean'].includes(item.id) ? 'local' : 'repository') : 'repository';
    item.integrity = 'valid';
    item.calculated = item.expected;
  }
  renderProfiles();
  renderStageCapacity();
  renderEvidence();
}

function downloadEvidence(id) {
  const blob = new Blob([demoEvidenceContent(id)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = `DEMO_${id}_v409.json`;
  link.click();
  setTimeout(() => URL.revokeObjectURL(url), 500);
  toast(`${d('download')} · ${evidenceTitle(id)}`);
}

function chooseEvidence(id) {
  const input = document.createElement('input');
  input.type = 'file';
  input.accept = 'application/json,.json';
  input.addEventListener('change', async () => {
    const file = input.files[0];
    if (!file) return;
    const text = await file.text();
    const calculated = await sha256Hex(text);
    const item = state.evidence.find((entry) => entry.id === id);
    item.calculated = calculated;
    item.integrity = calculated === item.expected ? 'valid' : 'divergent';
    if (item.integrity === 'valid') item.origin = 'repository';
    renderEvidence();
  }, { once: true });
  input.click();
}

function simulateDivergence(id = 'coma') {
  const item = state.evidence.find((entry) => entry.id === id);
  if (!item) return;
  item.calculated = '0'.repeat(64);
  item.integrity = 'divergent';
  renderEvidence();
}

function correctEvidence(id) {
  const item = state.evidence.find((entry) => entry.id === id);
  if (!item) return;
  item.calculated = item.expected;
  item.integrity = 'valid';
  item.origin = 'repository';
  renderEvidence();
  toast(`${d('correct')} · ${evidenceTitle(id)}`);
}

function reorderCards(targetId) {
  if (!state.draggedCard || state.draggedCard === targetId) return;
  const order = [...state.cardOrder];
  const from = order.indexOf(state.draggedCard);
  const to = order.indexOf(targetId);
  if (from < 0 || to < 0) return;
  order.splice(from, 1);
  order.splice(to, 0, state.draggedCard);
  state.cardOrder = order;
  renderBench();
  toast(d('moved'));
}

function renderLanguageButtons() {
  const meta = languageMeta();
  for (const button of $$('.language-button')) {
    $('.language-code', button).textContent = (meta.code || meta.id).toUpperCase();
    $('.language-name', button).textContent = meta.native || meta.name;
  }
  $('#language-current-note').textContent = currentLanguage() === 'custom' ? `${meta.native} · ${d('customFallback')}: ${languageMeta(meta.fallback).native}` : `${meta.native} · ${d('fullCatalog')}`;
}

function renderLanguageOptions() {
  const query = ($('#language-search')?.value || '').trim().toLocaleLowerCase();
  const options = [...languages];
  if (currentLanguage() === 'custom') options.push(languageMeta());
  $('#language-options').innerHTML = options.filter((language) => `${language.native} ${language.name} ${language.note}`.toLocaleLowerCase().includes(query)).map((language) => {
    const selected = currentLanguage() === language.id || (language.id === 'custom' && languageMeta().code === language.code);
    return `<button class="language-option ${selected ? 'is-selected' : ''}" type="button" data-language="${language.id}">
      <strong>${language.native}</strong><span>${language.note}</span><small>${language.dir.toUpperCase()} · ${language.id === 'custom' ? `${d('customFallback')}: ${languageMeta(language.fallback).native}` : d('fullCatalog')}</small>
    </button>`;
  }).join('');
  renderLanguageButtons();
}

function openLanguage() {
  renderLanguageOptions();
  openOverlay('language-overlay');
  $('#language-search').focus();
}

function applyCustomLanguage() {
  const name = $('#custom-language-name').value.trim();
  const code = $('#custom-language-code').value.trim() || name.toLocaleLowerCase().slice(0, 2);
  const dir = $('#custom-language-dir').value;
  const fallback = $('#custom-language-fallback').value;
  if (!name) { $('#custom-language-name').focus(); return; }
  setCustomLanguage({ id: 'custom', code, name, native: name, dir, fallback, note: `${d('customFallback')}: ${languageMeta(fallback).native}` });
  closeOverlay('language-overlay');
}

function openMedia() {
  syncVideo();
  $('#film-play span').textContent = d(gravityFilm.paused ? 'filmPlay' : 'filmPause');
  $('#film-light span').textContent = d(state.light ? 'lightOff' : 'lightOn');
  openOverlay('media-overlay');
}

function toggleFilmLight() {
  state.light = !state.light;
  syncVideo();
  $('#film-light span').textContent = d(state.light ? 'lightOff' : 'lightOn');
  $('#bench-light').textContent = d(state.light ? 'lightOff' : 'lightOn');
  toast(d(state.light ? 'filmOff' : 'filmOn'));
}

function toggleFilmPlayback() {
  if (gravityFilm.paused) gravityFilm.play().catch(() => {});
  else gravityFilm.pause();
  $('#film-play span').textContent = d(gravityFilm.paused ? 'filmPlay' : 'filmPause');
}

function chooseFilm(event) {
  const file = event.target.files[0];
  if (!file) return;
  const url = URL.createObjectURL(file);
  gravityFilm.src = url;
  $('#media-preview-video').src = url;
  state.light = false;
  syncVideo();
  toast(`${file.name} · ${d('filmOn')}`);
}

function rerenderLanguage() {
  applyStaticTranslations();
  renderLanguageButtons();
  for (const render of [renderDatasets, renderTests, renderLean, renderQuantum, renderBench, renderProfiles, renderStageCapacity, renderEvidence]) render();
  acom.render();
  if (state.screen === 'opening') {
    syncSubtitles();
    if (state.openingStatic) showReducedOpening();
    else updateOpeningCaption();
  }
  if (state.detail?.kind === 'test') openTestDetail(state.detail.id);
  if (state.detail?.kind === 'card') openCardDetail(state.detail.id);
  if (state.detail?.kind === 'lean') openLeanDetail(state.detail.id);
  $('#opening-subtitles').textContent = d(state.subtitles ? 'subtitlesOn' : 'subtitlesOff');
  $('#opening-reduced').textContent = d('openingReduced');
  $('#opening-skip').innerHTML = `${d('openingSkip')} ${icon('forward')}`;
  $('#film-play span').textContent = d(gravityFilm.paused ? 'filmPlay' : 'filmPause');
  $('#film-light span').textContent = d(state.light ? 'lightOff' : 'lightOn');
  $('#bench-light').textContent = d(state.light ? 'lightOff' : 'lightOn');
}

function bindEvents() {
  $('#one-form').addEventListener('submit', handleSubmitOne);
  $('#one-input').addEventListener('input', () => { $('#one-error').hidden = true; });
  $('#one-input').addEventListener('keydown', (event) => { if (event.key === 'Enter') { event.preventDefault(); handleSubmitOne(event); } });
  $('#architecture-open').addEventListener('click', () => openOverlay('architecture-overlay'));
  $('#terminal-note-open').addEventListener('click', () => toast(d('terminal')));
  $('#motion-toggle').addEventListener('click', toggleMotion);
  $('#runtime-motion-toggle').addEventListener('click', toggleMotion);
  $('#run-pause').addEventListener('click', toggleRunPause);
  $('#run-speed').addEventListener('click', cycleSpeed);
  $('#skip-run').addEventListener('click', skipRun);
  $('#enter-bench').addEventListener('click', enterBench);
  $('#new-run').addEventListener('click', resetExperience);
  $('#copy-hash').addEventListener('click', copyHash);
  $('#seal-chip').addEventListener('click', () => openOverlay('seal-overlay'));
  $('#seal-chip').addEventListener('keydown', (event) => { if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); openOverlay('seal-overlay'); } });
  $('#open-iald').addEventListener('click', () => openIald());
  $('#close-iald').addEventListener('click', () => { $('#iald-drawer').hidden = true; $('#open-iald').focus(); });
  for (const id of ['acom-open', 'acom-runtime-open', 'acom-bench-open', 'acom-capacity-open']) $(`#${id}`).addEventListener('click', acom.openAcom);
  $('#capacity-continue').addEventListener('click', startRun);
  $('#capacity-back').addEventListener('click', resetExperience);
  $('#open-capacity').addEventListener('click', () => { setScreen('capacity'); renderProfiles(); renderStageCapacity(); renderEvidence(); toast(d('returnedCapacity')); });
  $('#open-media').addEventListener('click', openMedia);
  $('#bench-media').addEventListener('click', openMedia);
  $('#film-play').addEventListener('click', toggleFilmPlayback);
  $('#film-light').addEventListener('click', toggleFilmLight);
  $('#bench-light').addEventListener('click', toggleFilmLight);
  $('#film-file').addEventListener('change', chooseFilm);
  $('#opening-skip').addEventListener('click', enterCapacity);
  $('#opening-reduced').addEventListener('click', showReducedOpening);
  $('#reduced-next').addEventListener('click', nextReducedSlide);
  $('#opening-subtitles').addEventListener('click', () => { state.subtitles = !state.subtitles; syncSubtitles(); });
  openingVideo.addEventListener('timeupdate', updateOpeningCaption);
  openingVideo.addEventListener('ended', enterCapacity);
  for (const id of ['language-open', 'capacity-language-open', 'runtime-language-open', 'bench-language-open', 'opening-language-open', 'acom-language-open']) $(`#${id}`).addEventListener('click', openLanguage);
  $('#language-system').addEventListener('click', () => { setLanguage(systemLanguage()); closeOverlay('language-overlay'); });
  $('#language-search').addEventListener('input', renderLanguageOptions);
  $('#custom-language-apply').addEventListener('click', applyCustomLanguage);
  $('#station-search').addEventListener('input', renderBench);
  $('#clear-station-search')?.addEventListener('click', () => { $('#station-search').value = ''; renderBench(); });

  document.addEventListener('click', (event) => {
    const close = event.target.closest('[data-close]');
    if (close) { closeOverlay(close.dataset.close); return; }
    const language = event.target.closest('button.language-option[data-language]');
    if (language) { setLanguage(language.dataset.language); closeOverlay('language-overlay'); return; }
    const profile = event.target.closest('[data-profile]');
    if (profile) { setProfile(profile.dataset.profile); return; }
    const download = event.target.closest('[data-download-evidence]');
    if (download) { downloadEvidence(download.dataset.downloadEvidence); return; }
    const choose = event.target.closest('[data-choose-evidence]');
    if (choose) { chooseEvidence(choose.dataset.chooseEvidence); return; }
    const simulate = event.target.closest('[data-simulate-evidence]');
    if (simulate) { simulateDivergence(simulate.dataset.simulateEvidence); return; }
    const correct = event.target.closest('[data-correct-evidence]');
    if (correct) { correctEvidence(correct.dataset.correctEvidence); return; }
    const testButton = event.target.closest('[data-test-id]');
    if (testButton) { openTestDetail(testButton.dataset.testId); return; }
    const leanButton = event.target.closest('[data-lean-id]');
    if (leanButton) { openLeanDetail(leanButton.dataset.leanId); return; }
    const expand = event.target.closest('[data-expand]');
    if (expand) { openCardDetail(expand.dataset.expand); return; }
    const ask = event.target.closest('[data-ask]');
    if (ask) {
      const id = ask.dataset.ask;
      const kind = isTestStation(id) ? 'test' : 'card';
      const object = kind === 'test' ? tests.find((item) => item.id === id) : cardById(id);
      const title = kind === 'test' ? localize('tests', object, 'name') : localize('benchCards', object, 'title');
      openIald(`${d('ask')} “${title}”.`, answerForObject(kind, id));
      return;
    }
    const detailAsk = event.target.closest('[data-detail-ask]');
    if (detailAsk && state.detail) {
      const { kind, id } = state.detail;
      const object = kind === 'test' ? tests.find((item) => item.id === id) : cardById(id);
      const title = kind === 'test' ? localize('tests', object, 'name') : localize('benchCards', object, 'title');
      openIald(`${d('ask')} “${title}”.`, answerForObject(kind, id));
      return;
    }
    const quick = event.target.closest('[data-question]');
    if (quick) askIald(quick.dataset.question);
    if (event.target.classList.contains('overlay')) closeOverlay(event.target.id);
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') closeTopOverlay();
    trapFocus(event);
  });

  $('#chat-form').addEventListener('submit', (event) => {
    event.preventDefault();
    const input = $('#chat-input');
    if (!input.value.trim()) { input.setAttribute('aria-invalid', 'true'); return; }
    input.removeAttribute('aria-invalid');
    askIald(input.value);
    input.value = '';
  });
  $('#chat-input').addEventListener('keydown', (event) => {
    if (event.key === 'Enter' && !event.shiftKey) { event.preventDefault(); $('#chat-form').requestSubmit(); }
  });

  $('#bench-grid').addEventListener('dragstart', (event) => {
    const handle = event.target.closest('.drag-handle');
    if (!handle) return;
    const card = handle.closest('.bench-card');
    state.draggedCard = card.dataset.cardId;
    card.classList.add('is-dragging');
    event.dataTransfer.effectAllowed = 'move';
    event.dataTransfer.setData('text/plain', state.draggedCard);
  });
  $('#bench-grid').addEventListener('dragover', (event) => {
    const card = event.target.closest('.bench-card');
    if (!card || !state.draggedCard) return;
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
    card.classList.add('is-drop-target');
  });
  $('#bench-grid').addEventListener('dragleave', (event) => {
    const card = event.target.closest('.bench-card');
    if (card) card.classList.remove('is-drop-target');
  });
  $('#bench-grid').addEventListener('drop', (event) => {
    const card = event.target.closest('.bench-card');
    if (!card) return;
    event.preventDefault();
    reorderCards(card.dataset.cardId);
  });
  $('#bench-grid').addEventListener('dragend', () => {
    state.draggedCard = null;
    for (const card of $$('.bench-card')) card.classList.remove('is-dragging', 'is-drop-target');
  });
  $('#bench-grid').addEventListener('keydown', (event) => {
    const handle = event.target.closest('.drag-handle');
    if (!handle) return;
    const card = handle.closest('.bench-card');
    const order = [...state.cardOrder];
    const index = order.indexOf(card.dataset.cardId);
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
      event.preventDefault();
      const next = event.key === 'ArrowLeft' ? Math.max(0, index - 1) : Math.min(order.length - 1, index + 1);
      [order[index], order[next]] = [order[next], order[index]];
      state.cardOrder = order;
      renderBench();
      $(`.bench-card[data-card-id="${card.dataset.cardId}"] .drag-handle`).focus();
      toast(d('movedKeyboard'));
    }
  });

  window.addEventListener('um-language-changed', rerenderLanguage);
  reducedMotion.addEventListener('change', (event) => { if (event.matches) { state.motion = false; syncMotionButtons(); } });
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) { space.setRunning(false); quantum.setRunning(false); gravityFilm.pause(); openingVideo.pause(); }
    else syncMotionButtons();
  });
}

applyStaticTranslations();
bindEvents();
syncMotionButtons();
renderLanguageButtons();
renderBench();
initEvidence();
acom.init();
if (new URLSearchParams(location.search).get('ferramenta') === 'acom') acom.openAcom();

// Contrato local de verificação: nenhum motor científico ou serviço externo é chamado.
window.__UM_INTERFACE__ = {
  get state() {
    return {
      screen: state.screen, elapsed: state.elapsed, phase: state.phase,
      running: state.running, paused: state.paused, speed: state.speed,
      sealShown: state.sealShown, hash: state.hash, cardOrder: [...state.cardOrder],
      profile: state.profile, language: currentLanguage(), light: state.light,
      evidence: state.evidence.map((item) => ({ ...item }))
    };
  },
  skipRun, beginOpening, enterCapacity, startRun, setProfile, simulateDivergence, correctEvidence,
  openTestDetail, openCardDetail, openLeanDetail, resetExperience, setLanguage, setCustomLanguage,
  normalizeOne, acom
};
