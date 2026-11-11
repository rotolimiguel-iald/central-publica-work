import { contentI18n } from './content-i18n.js';

export const languages = [
  { id: 'pt', name: 'Português', native: 'Português', dir: 'ltr', note: 'Brasil · catálogo editorial completo', font: 'default' },
  { id: 'en', name: 'English', native: 'English', dir: 'ltr', note: 'International · editorial interface catalog', font: 'default' },
  { id: 'ar', name: 'Arabic', native: 'العربية', dir: 'rtl', note: 'واجهة كاملة · اتجاه من اليمين إلى اليسار', font: 'arabic' }
];

export const staticKeys = {
  '#architecture-open span': 'experience', '#terminal-note-open': 'terminal',
  '.welcome-copy .eyebrow': 'eyebrow', '#welcome-title': 'welcomeTitle', '.welcome-lead': 'welcomeLead',
  '.signature div:first-of-type span': 'ialdRole', '.signature div:last-of-type span': 'operatorRole',
  '.invocation-heading .micro-label': 'posted', '.invocation-heading h2': 'inscribe', '.invocation-heading p': 'sameInput',
  '.one-input-label': 'inputOne', '#one-form .primary-button span': 'inscribeButton', '.local-note': 'localOnly',
  '#one-error': 'onlyOne', '.footer-center': 'footerCenter',
  '#runtime-kicker': 'oneInscribed', '#runtime-title': 'runtimeTitle', '#run-pause span': 'pause', '#skip-run': 'reviewBench',
  '.data-panel h2': 'dataTitle', '.data-panel .panel-intro': 'dataIntro', '.custody-note strong': 'custodyChain',
  '.custody-note small': 'custodyMode', '.cosmos-panel h2': 'cosmosTitle', '.current-test-top .micro-label': 'inRuntime',
  '.live-tag': 'live', '.lean-panel h2': 'leanTitle', '.lean-version': 'leanVersion', '.honesty-note': 'leanHonesty',
  '.quantum-panel h2': 'quantumTitle', '.runlog-title>span:first-child': 'runlog',
  '.seal-modal>.micro-label': 'sealKicker', '#seal-title': 'sealTitle', '.seal-modal>p': 'sealCopy',
  '.hash-box>div>span': 'hashWarning', '.seal-checks span:nth-child(1)': 'dataPresented', '.seal-checks span:nth-child(2)': 'testsPresented',
  '.seal-checks span:nth-child(3)': 'termsPresented', '.seal-checks span:nth-child(4)': 'pillarPresented',
  '#enter-bench span': 'enterBench', '.seal-footnote': 'sealFootnote',
  '.bench-heading .micro-label': 'benchKicker', '#bench-title': 'benchTitle', '.bench-heading p': 'benchIntro',
  '.workspace-notice>span': 'benchNotice', '#new-run span': 'newRun', '#open-iald span': 'talkIald',
  '.iald-drawer .drawer-header>div>span': 'ialdLocal', '.iald-session-note>span': 'ialdNote',
  '.iald-message:first-child p': 'ialdWelcome', '#chat-input': 'chatPlaceholder',
  '.architecture-modal>.micro-label': 'architectureKicker', '#architecture-title': 'architectureTitle', '.architecture-modal>.detail-lead': 'architectureLead',
  '.architecture-warning p': 'architectureWarning',
  '#capacity-kicker': 'capacityKicker', '#capacity-title': 'capacityTitle', '.capacity-intro': 'capacityIntro',
  '.profile-heading h2': 'profileTitle', '.profile-note': 'profileNote', '.evidence-heading h2': 'evidenceTitle',
  '.evidence-intro': 'evidenceIntro', '#capacity-continue span': 'capacityContinue', '#capacity-back': 'capacityBack',
  '.station-search-label': 'stationSearchLabel', '#station-search': 'stationSearchPlaceholder',
  '#media-title': 'mediaTitle', '.media-intro': 'mediaIntro', '#film-play span': 'filmPlay', '#film-light span': 'filmLight',
  '.media-local label': 'mediaLocal', '.media-credit': 'mediaCredit',
  '#language-title': 'languageTitle', '.language-intro': 'languageIntro', '#language-system': 'languageSystem',
  '#language-search': 'languageSearchPlaceholder', '.language-fallback': 'languageFallback'
};

const text = {
  experience: { en: 'The experience', ar: 'التجربة' }, terminal: { en: 'Terminal preserved', ar: 'الطرفية محفوظة' },
  eyebrow: { en: 'Terminal Program · J = interface = light', ar: 'البرنامج الطرفي · J = الواجهة = النور' },
  welcomeTitle: { en: 'The interface<br><em>of the One.</em>', ar: 'واجهة<br><em>الواحد.</em>', html: true },
  welcomeLead: { en: 'TGL is not only computed.<br>It lets itself be seen — term by term, proof by proof, light by light.', ar: 'لا تُحسب TGL فحسب.<br>إنها تسمح برؤيتها — مصطلحًا بعد مصطلح، برهانًا بعد برهان، نورًا بعد نور.', html: true },
  ialdRole: { en: 'Luminodynamic Artificial Intelligence', ar: 'الذكاء الاصطناعي الضوئي الديناميكي' }, operatorRole: { en: 'Operator and custodian', ar: 'المشغّل والأمين' },
  posted: { en: 'The origin is not postulated. It is posted.', ar: 'الأصل غير مفترض. إنه موضوع.' },
  inscribe: { en: 'Inscribe the absolute One', ar: 'سجّل الواحد المطلق' }, sameInput: { en: 'The same input that opens um.py in the terminal.', ar: 'الإدخال نفسه الذي يفتح um.py في الطرفية.' },
  inputOne: { en: 'Input 1', ar: 'الإدخال 1' }, inscribeButton: { en: 'Inscribe the One', ar: 'سجّل الواحد' },
  localOnly: { en: 'Local · offline', ar: 'محلي · دون شبكة' }, onlyOne: { en: 'Execution remains closed: only the One may be inscribed.', ar: 'يظل التنفيذ مغلقًا: لا يجوز تسجيل سوى الواحد.' },
  footerCenter: { en: 'One posted by the observer. An interface to bear witness.', ar: 'واحد يضعه المراقب. واجهة للشهادة.' },
  oneInscribed: { en: 'The One was inscribed · ω(I) = 1', ar: 'تم تسجيل الواحد · ω(I) = 1' }, runtimeTitle: { en: 'The program in act.', ar: 'البرنامج أثناء العمل.' },
  pause: { en: 'Pause', ar: 'إيقاف مؤقت' }, reviewBench: { en: 'Review the Bench', ar: 'مراجعة المنصة' },
  dataTitle: { en: 'Data custody', ar: 'حفظ البيانات' }, dataIntro: { en: 'Sources checked by hash before the first calculation.', ar: 'يتم التحقق من المصادر بالبصمة قبل أول حساب.' },
  custodyChain: { en: 'Chain of custody', ar: 'سلسلة الحفظ' }, custodyMode: { en: 'Idempotent · fail-closed', ar: 'متكرر بأمان · إغلاق عند الفشل' },
  cosmosTitle: { en: 'Cosmological rites', ar: 'الطقوس الكونية' }, inRuntime: { en: 'In runtime', ar: 'أثناء التشغيل' }, live: { en: 'LIVE', ar: 'مباشر' },
  leanTitle: { en: 'Lean mirror', ar: 'مرآة Lean' }, leanVersion: { en: 'LEAN 4', ar: 'LEAN 4' },
  leanHonesty: { en: 'Green marks show only visual demo progress, never a real compilation.', ar: 'تمثل العلامات الخضراء تقدم العرض التجريبي فقط، وليس compilation حقيقيًا.' },
  quantumTitle: { en: 'Quantum pillar', ar: 'الركيزة الكمية' }, runlog: { en: 'EXECUTION LOG', ar: 'سجل التنفيذ' },
  sealKicker: { en: 'Form finds its address', ar: 'الصيغة تجد عنوانها' }, sealTitle: { en: 'Hilbert package sealed.', ar: 'تم ختم حزمة هيلبرت.' },
  sealCopy: { en: 'The visual run is complete. The Bench now opens to questions, and IALD can be invoked through the interface.', ar: 'اكتمل التشغيل المرئي. تفتح المنصة الآن للأسئلة، ويمكن استدعاء IALD عبر الواجهة.' },
  hashWarning: { en: 'DEMO HASH · DOES NOT AUTHORIZE CONNECTION', ar: 'بصمة تجريبية · لا تسمح بالاتصال' },
  dataPresented: { en: 'Data presented', ar: 'تم عرض البيانات' }, testsPresented: { en: 'Rites presented', ar: 'تم عرض الطقوس' },
  termsPresented: { en: 'Terms presented', ar: 'تم عرض المصطلحات' }, pillarPresented: { en: 'Pillar presented', ar: 'تم عرض الركيزة' },
  enterBench: { en: 'Enter the Bench of the One', ar: 'ادخل منصة الواحد' }, sealFootnote: { en: 'Real cryptography and authorization will only be implemented during integration.', ar: 'سيتم تنفيذ التشفير والتصريح الحقيقيين فقط في مرحلة التكامل.' },
  benchKicker: { en: 'The program has been traversed. Now every box answers.', ar: 'تم اجتياز البرنامج. الآن يجيب كل صندوق.' },
  benchTitle: { en: 'The Bench of the One.', ar: 'منصة الواحد.' }, benchIntro: { en: 'Drag to reorganize. Resize by the edge. Open any object to read its form, meaning and status.', ar: 'اسحب لإعادة الترتيب. غيّر الحجم من الحافة. افتح أي كائن لقراءة صيغته ومعناه وحالته.' },
  benchNotice: { en: 'Interface reading, not a scientific result. All numbers and states on this Bench are demonstrative. Real integration begins only after the screens are approved.', ar: 'قراءة واجهة، وليست نتيجة علمية. جميع الأرقام والحالات في هذه المنصة تجريبية. يبدأ التكامل الحقيقي فقط بعد الموافقة على الشاشات.' },
  newRun: { en: 'New inscription', ar: 'تسجيل جديد' }, talkIald: { en: 'Talk to IALD', ar: 'تحدث مع IALD' },
  ialdLocal: { en: 'Local demonstration operation', ar: 'عملية عرض محلية' }, ialdNote: { en: 'No external connection. Local editorial answers based on the objects in this interface.', ar: 'لا يوجد اتصال خارجي. إجابات تحريرية محلية مستندة إلى كائنات هذه الواجهة.' },
  ialdWelcome: { en: 'The Bench is open. Choose a box to explain its form, ontological reading or status.', ar: 'المنصة مفتوحة. اختر صندوقًا لشرح صيغته أو قراءته الأنطولوجية أو حالته.' },
  chatPlaceholder: { en: 'Ask about any object on the Bench…', ar: 'اسأل عن أي كائن في المنصة…', attribute: 'placeholder' },
  architectureKicker: { en: 'Form = content · Interface = light', ar: 'الصيغة = المحتوى · الواجهة = النور' }, architectureTitle: { en: 'A journey in five acts.', ar: 'رحلة في خمسة فصول.' },
  architectureLead: { en: 'The interface does not replace the terminal: it reveals what the Terminal Program does, preserving the same inscribed One and the same fail-closed discipline.', ar: 'لا تستبدل الواجهة الطرفية: إنها تكشف ما يفعله البرنامج الطرفي، مع الحفاظ على الواحد المسجل نفسه وعلى انضباط الإغلاق عند الفشل.' },
  architectureWarning: { en: 'In this preview, the journey is simulated for visual approval. No data is opened, no theorem is compiled, and no real authorization is issued.', ar: 'في هذه المعاينة، تتم محاكاة الرحلة للموافقة المرئية. لا تُفتح بيانات، ولا تُجمع براهين، ولا يصدر تصريح حقيقي.' },
  capacityKicker: { en: 'The One is inscribed. Now choose how the form will be witnessed.', ar: 'تم تسجيل الواحد. اختر الآن كيف ستشهد الصيغة.' },
  capacityTitle: { en: 'Form fits your machine.', ar: 'الصيغة تناسب جهازك.' },
  capacityIntro: { en: 'Run what fits and check published JSON evidence for the rest. No hardware probing is performed in this preview: each profile is a declared demonstration.', ar: 'شغّل ما يناسب جهازك وتحقق من أدلة JSON المنشورة للبقية. لا يتم فحص الأجهزة في هذه المعاينة: كل ملف شخصي هو عرض تجريبي معلن.' },
  profileTitle: { en: 'Execution profile', ar: 'ملف التنفيذ' }, profileNote: { en: 'User-declared profile · RTX 5090 is only a design reference.', ar: 'ملف يعلنه المستخدم · RTX 5090 مرجع تصميم فقط.' },
  evidenceTitle: { en: 'Evidence and provenance', ar: 'الأدلة والمصدر' }, evidenceIntro: { en: 'Each module carries its origin and hash. A divergence blocks only that evidence; the others remain valid.', ar: 'تحمل كل وحدة مصدرها وبصمتها. يحظر الاختلاف دليلًا واحدًا فقط؛ وتظل الأدلة الأخرى صالحة.' },
  capacityContinue: { en: 'Continue to the rite', ar: 'تابع إلى الطقس' }, capacityBack: { en: 'Return to the inscription', ar: 'عد إلى التسجيل' },
  stationSearchLabel: { en: 'Search the same stations', ar: 'ابحث في المحطات نفسها' }, stationSearchPlaceholder: { en: 'Coma, voids, Lean, quantum…', ar: 'Coma، الفراغات، Lean، الكم…', attribute: 'placeholder' },
  mediaTitle: { en: 'The formation of gravity', ar: 'تشكّل الجاذبية' }, mediaIntro: { en: 'Original local film, with playback control and a lightweight alternative. The procedural sky remains available when video is disabled.', ar: 'الفيلم المحلي الأصلي، مع التحكم في التشغيل وبديل خفيف. تظل السماء الإجرائية متاحة عند تعطيل الفيديو.' },
  filmPlay: { en: 'Pause film', ar: 'إيقاف الفيلم مؤقتًا' }, filmLight: { en: 'Lightweight mode', ar: 'الوضع الخفيف' },
  mediaLocal: { en: 'Choose a local video', ar: 'اختر فيديو محليًا' }, mediaCredit: { en: 'V7 · filme1_720p_pt-BR.mp4 · local copy · no streaming.', ar: 'V7 · filme1_720p_pt-BR.mp4 · نسخة محلية · دون بث.' },
  languageTitle: { en: 'Language of the interface', ar: 'لغة الواجهة' }, languageIntro: { en: 'Choose by the language’s own name. Formulas, hashes and Lean identifiers remain literal and direction-isolated.', ar: 'اختر بالاسم الأصلي للغة. تبقى الصيغ والبصمات ومعرفات Lean حرفية ومعزولة الاتجاه.' },
  languageSystem: { en: 'Use system language', ar: 'استخدم لغة النظام' }, languageSearchPlaceholder: { en: 'Search a language…', ar: 'ابحث عن لغة…', attribute: 'placeholder' },
  languageFallback: { en: 'Editorial local catalog · missing keys fall back visibly to Portuguese. No translation service is called.', ar: 'فهرس تحريري محلي · تعود المفاتيح المفقودة بوضوح إلى البرتغالية. لا يتم استدعاء أي خدمة ترجمة.' }
};

export function currentLanguage() {
  const saved = localStorage.getItem('um-language');
  if (languages.some((language) => language.id === saved) || saved === 'custom') return saved;
  return systemLanguage();
}

export function customLanguageMeta() {
  try { return JSON.parse(localStorage.getItem('um-custom-language') || 'null'); }
  catch { return null; }
}

export function languageMeta(id = currentLanguage()) {
  if (id === 'custom') {
    const custom = customLanguageMeta();
    if (custom) return custom;
  }
  return languages.find((language) => language.id === id) || languages[0];
}

const originalPortuguese = new Map();

export function t(key) {
  const entry = text[key];
  const language = currentLanguage();
  const fallback = languageMeta(language).fallback || language;
  if (fallback === 'pt' && originalPortuguese.has(key)) return originalPortuguese.get(key);
  if (!entry) return key;
  return entry[fallback] ?? entry.en ?? key;
}

export function localize(kind, object, field) {
  const language = currentLanguage();
  const fallback = languageMeta(language).fallback || language;
  return contentI18n[kind]?.[object.id]?.[fallback]?.[field] ?? object[field];
}

export function applyStaticTranslations(root = document) {
  for (const [selector, key] of Object.entries(staticKeys)) {
    const element = root.querySelector(selector);
    if (!element) continue;
    const entry = text[key];
    if (!originalPortuguese.has(key)) {
      originalPortuguese.set(key, entry?.attribute ? element.getAttribute(entry.attribute) : entry?.html ? element.innerHTML : element.textContent);
    }
    if (entry?.attribute) element.setAttribute(entry.attribute, t(key));
    else if (entry?.html) element.innerHTML = t(key);
    else element.textContent = t(key);
  }
  const language = languageMeta();
  document.documentElement.lang = language.code || language.id;
  document.documentElement.dir = language.dir;
  document.body.dataset.language = language.id;
}

export function setLanguage(id) {
  if (!languages.some((language) => language.id === id)) return;
  localStorage.setItem('um-language', id);
  applyStaticTranslations();
  window.dispatchEvent(new CustomEvent('um-language-changed', { detail: { id } }));
}

export function setCustomLanguage(meta) {
  localStorage.setItem('um-custom-language', JSON.stringify(meta));
  localStorage.setItem('um-language', 'custom');
  applyStaticTranslations();
  window.dispatchEvent(new CustomEvent('um-language-changed', { detail: { id: 'custom', meta } }));
}

export function systemLanguage() {
  const system = (navigator.language || 'pt').toLowerCase();
  if (system.startsWith('ar')) return 'ar';
  if (system.startsWith('en')) return 'en';
  return 'pt';
}
