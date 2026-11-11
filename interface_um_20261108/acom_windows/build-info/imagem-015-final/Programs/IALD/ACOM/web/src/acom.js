import { currentLanguage, languageMeta } from './i18n.js';

const TEXT = {
  back: ['Voltar à jornada', 'Back to the journey', 'العودة إلى الرحلة'],
  kicker: ['Ferramenta gratuita por pessoa · originais preservados', 'Free tool per person · originals preserved', 'أداة مجانية لكل شخص · الأصول محفوظة'],
  title: ['ACOM, para cada arquivo.', 'ACOM, for every file.', 'ACOM، لكل ملف.'],
  intro: ['Escolha origem e destino na janela do Windows. Compacte arquivos ou pastas e restaure pacotes .acom. Nenhuma inscrição, conta, GPU ou hash de rodada é necessário.', 'Choose source and destination in the Windows picker. Pack files or folders and restore .acom packages. No inscription, account, GPU or run hash is required.', 'اختر المصدر والوجهة في نافذة Windows. اضغط الملفات أو المجلدات واستعد حزم .acom. لا حاجة إلى تسجيل أو حساب أو GPU أو بصمة تشغيل.'],
  hostKicker: ['Integração opcional por usuário', 'Optional per-user integration', 'تكامل اختياري لكل مستخدم'],
  hostProbing: ['Procurando o ACOM neste computador…', 'Looking for ACOM on this computer…', 'البحث عن ACOM على هذا الكمبيوتر…'],
  hostProbingDetail: ['A verificação acontece só neste computador, sem enviar arquivos.', 'The check happens only on this computer, without sending files.', 'يتم الفحص على هذا الكمبيوتر فقط، دون إرسال ملفات.'],
  hostOnline: ['Pronto para escolher seus arquivos', 'Ready to choose your files', 'جاهز لاختيار ملفاتك'],
  hostOnlineDetail: ['O ACOM está instalado e pronto para abrir a janela de escolha do Windows.', 'ACOM is installed and ready to open the Windows picker.', 'ACOM مثبت وجاهز لفتح نافذة اختيار Windows.'],
  hostOffline: ['Para usar arquivos deste computador, abra o ACOM instalado ou baixe a versão de teste para Windows', 'To use files on this computer, open installed ACOM or download the Windows test version', 'لاستخدام الملفات على هذا الكمبيوتر، افتح ACOM المثبت أو نزّل نسخة الاختبار لنظام Windows'],
  hostOfflineDetail: ['A prévia não lê nem altera arquivos. Se o ACOM já estiver instalado, ele abrirá as janelas de escolha.', 'The preview does not read or change files. If ACOM is installed, it will open the selection windows.', 'المعاينة لا تقرأ أو تغير الملفات. إذا كان ACOM مثبتًا، فسيفتح نوافذ الاختيار.'],
  refresh: ['Verificar novamente', 'Check again', 'تحقق مرة أخرى'],
  packFiles: ['Compactar arquivo(s)', 'Pack file(s)', 'ضغط الملفات'],
  packFilesDetail: ['Selecione um ou mais arquivos e o destino do pacote .acom.', 'Select one or more files and the destination of the .acom package.', 'اختر ملفًا أو أكثر ووجهة حزمة .acom.'],
  packFolder: ['Compactar pasta', 'Pack folder', 'ضغط المجلد'],
  packFolderDetail: ['Escolha uma pasta inteira, preservando a estrutura e os originais.', 'Choose an entire folder, preserving structure and originals.', 'اختر مجلدًا كاملًا مع الحفاظ على البنية والأصول.'],
  extract: ['Abrir / restaurar .acom', 'Open / restore .acom', 'فتح / استعادة .acom'],
  extractDetail: ['Selecione um pacote e a pasta de restauração.', 'Select a package and the restoration folder.', 'اختر حزمة ومجلد الاستعادة.'],
  resultKicker: ['Resultado', 'Result', 'النتيجة'],
  pending: ['Escolha a origem e o destino na janela do Windows', 'Choose source and destination in the Windows picker', 'اختر المصدر والوجهة في نافذة Windows'],
  pendingDetail: ['O resultado aparece depois que você confirmar ou cancelar.', 'The result appears after you confirm or cancel.', 'تظهر النتيجة بعد التأكيد أو الإلغاء.'],
  unavailable: ['O ACOM ainda não está disponível neste computador', 'ACOM is not yet available on this computer', 'ACOM غير متاح على هذا الكمبيوتر بعد'],
  unavailableDetail: ['Abra o ACOM instalado ou baixe a versão de teste para Windows. Nenhum arquivo foi alterado.', 'Open installed ACOM or download the Windows test version. No files were changed.', 'افتح ACOM المثبت أو نزّل نسخة الاختبار لنظام Windows. لم يتم تغيير أي ملفات.'],
  okPack: ['Pacote criado.', 'Package created.', 'تم إنشاء الحزمة.'],
  okExtract: ['Restauração concluída.', 'Restoration complete.', 'اكتملت الاستعادة.'],
  cancelled: ['Operação cancelada. Seus arquivos continuam como estavam.', 'Operation cancelled. Your files remain as they were.', 'تم إلغاء العملية. ملفاتك كما كانت.'],
  cancelledDetail: ['Você pode escolher outra origem ou destino quando quiser.', 'You can choose another source or destination whenever you want.', 'يمكنك اختيار مصدر أو وجهة أخرى متى شئت.'],
  error: ['Não foi possível concluir.', 'Could not complete.', 'تعذر الإكمال.'],
  errorDetail: ['O ACOM não conseguiu concluir. Seus arquivos continuam como estavam.', 'ACOM could not complete. Your files remain as they were.', 'لم يتمكن ACOM من الإكمال. ملفاتك كما كانت.'],
  destination: ['Destino', 'Destination', 'الوجهة'],
  files: ['arquivos', 'files', 'ملفات'],
  input: ['entrada', 'input', 'الإدخال'],
  output: ['saída', 'output', 'الإخراج'],
  demoKicker: ['Exemplo isolado · sem arquivos', 'Isolated example · no files', 'مثال منفصل · لا ملفات'],
  demoMessage: ['Resultado meramente ilustrativo: nenhum arquivo foi lido ou criado.', 'Merely illustrative result: no file was read or created.', 'نتيجة توضيحية فقط: لم تتم قراءة أو إنشاء أي ملف.'],
  setupChecking: ['Instalador: verificando disponibilidade…', 'Installer: checking availability…', 'المثبت: جارٍ التحقق من التوفر…'],
  setupAvailable: ['Instalador de teste disponível para Windows.', 'Test installer available for Windows.', 'مثبت الاختبار متاح لنظام Windows.'],
  setupUnavailable: ['Instalador de teste indisponível no momento.', 'Test installer unavailable at the moment.', 'مثبت الاختبار غير متاح حاليًا.'],
  sourceChecking: ['Fonte: verificando disponibilidade…', 'Source: checking availability…', 'المصدر: جارٍ التحقق من التوفر…'],
  sourceAvailable: ['Código-fonte disponível para baixar.', 'Source code available for download.', 'الكود المصدري متاح للتنزيل.'],
  sourceUnavailable: ['Código-fonte indisponível no momento.', 'Source code unavailable at the moment.', 'الكود المصدري غير متاح حاليًا.'],
  installed: ['Já instalado neste computador', 'Already installed on this computer', 'مثبت بالفعل على هذا الكمبيوتر'],
  uriNotice: ['Vamos tentar abrir o ACOM instalado. O Windows perguntará qual aplicativo você quer usar.', 'We will try to open installed ACOM. Windows will ask which app you want to use.', 'سنحاول فتح ACOM المثبت. سيسألك Windows عن التطبيق الذي تريد استخدامه.'],
  downloadUnavailable: ['Download indisponível no momento. Nenhum arquivo foi baixado.', 'Download unavailable at the moment. No files were downloaded.', 'التنزيل غير متاح حاليًا. لم يتم تنزيل أي ملفات.'],
  networkError: ['Não foi possível confirmar a integração. Nenhum arquivo foi alterado.', 'Could not confirm integration. No files were changed.', 'تعذر تأكيد التكامل. لم يتم تغيير أي ملفات.'],
  installTitle: ['Leve o ACOM para o computador.', 'Take ACOM to your computer.', 'انقل ACOM إلى جهازك.'],
  brandSubtitle: ['Compactar e restaurar, sem inscrição', 'Pack and restore, no inscription required', 'ضغط واستعادة، دون تسجيل'],
  installKicker: ['Windows · escolha opcional por usuário', 'Windows · optional choice per user', 'Windows · اختيار اختياري لكل مستخدم'],
  principlesKicker: ['Limites claros', 'Clear limits', 'حدود واضحة'],
  openInstalled: ['Abrir ACOM instalado', 'Open installed ACOM', 'فتح ACOM المثبت'],
  downloadSetup: ['Baixar instalador de teste', 'Download test installer', 'تنزيل مثبت الاختبار'],
  downloadSource: ['Código-fonte disponível', 'Source code available', 'الكود المصدري متاح'],
  demoSummary: ['Exemplo isolado de interface — nenhum arquivo é lido', 'Isolated interface example — no files are read', 'مثال منفصل للواجهة — لا تتم قراءة أي ملفات'],
  demoCopy: ['Use estes controles apenas para visualizar os estados de sucesso, cancelamento e erro. Eles não representam compressão real.', 'Use these controls only to view success, cancellation and error states. They do not represent real compression.', 'استخدم هذه الأزرار فقط لعرض حالات النجاح والإلغاء والخطأ. لا تمثل ضغطًا حقيقيًا.'],
  demoOk: ['Ver sucesso de exemplo', 'View example success', 'عرض مثال النجاح'],
  demoCancelled: ['Ver cancelamento', 'View cancellation', 'عرض الإلغاء'],
  demoError: ['Ver erro', 'View error', 'عرض الخطأ'],
  sampleLink: ['Experimentar com o pacote Primeira luz', 'Try the First light package', 'جرّب حزمة الضوء الأول'],
  sampleNote: ['Restaure o pacote e abra inscrição.txt. Lá dentro está o 1.', 'Restore the package and open inscrição.txt. The 1 is inside.', 'استعد الحزمة وافتح inscrição.txt. الرقم 1 موجود بالداخل.'],
  principlesTitle: ['O que a ferramenta promete — e o que não promete.', 'What the tool promises — and what it does not.', 'ما تعد به الأداة — وما لا تعد به.'],
  step1: ['Abra pacotes .acom pelo Windows, mantendo sua escolha de aplicativos padrão.', 'Open .acom packages in Windows, keeping your default app choices.', 'افتح حزم .acom في Windows مع الحفاظ على اختيارات التطبيقات الافتراضية.'],
  step2: ['Compacte pelo menu de arquivos ou pastas e escolha o destino.', 'Pack from the file or folder menu and choose the destination.', 'اضغط من قائمة الملفات أو المجلدات واختر الوجهة.'],
  step3: ['Restaure com o comando de restauração do ACOM.', 'Restore with the ACOM restore command.', 'استعد باستخدام أمر الاستعادة في ACOM.'],
  step4: ['Remova a instalação opcional pelos recursos do Windows, quando quiser.', 'Remove the optional installation through Windows features whenever you want.', 'أزل التثبيت الاختياري من خلال ميزات Windows متى شئت.'],
  principle1: ['Código-fonte disponível, gratuito para uso pessoal e não comercial.', 'Source available, free for personal and non-commercial use.', 'الكود المصدري متاح مجانًا للاستخدام الشخصي وغير التجاري.'],
  principle2: ['Originais sempre preservados; origem e destino escolhidos pelo usuário.', 'Originals always preserved; source and destination chosen by the user.', 'الأصول محفوظة دائمًا؛ يختار المستخدم المصدر والوجهة.'],
  principle3: ['A taxa de compressão varia por tipo de arquivo e não é prometida para todo conteúdo.', 'Compression ratio varies by file type and is not promised for every content.', 'تختلف نسبة الضغط حسب نوع الملف ولا تُضمن لكل المحتوى.'],
  principle4: ['Compactação e restauração não autorizam conversa nem alteram a rodada científica.', 'Packing and restoring do not authorize conversation or change the scientific run.', 'الضغط والاستعادة لا يأذنان بالمحادثة ولا يغيران التشغيل العلمي.']
};

const a = (key) => {
  const fallback = languageMeta().fallback || currentLanguage();
  return TEXT[key]?.[fallback === 'ar' ? 2 : fallback === 'en' ? 1 : 0] || key;
};

const setText = (id, value) => {
  const element = document.getElementById(id);
  if (element) element.textContent = value;
};

const formatBytes = (value) => {
  if (!Number.isFinite(value)) return '';
  const units = ['B', 'KB', 'MB', 'GB'];
  const index = value >= 1e9 ? 3 : value >= 1e6 ? 2 : value >= 1e3 ? 1 : 0;
  const scaled = value / [1, 1e3, 1e6, 1e9][index];
  const locale = languageMeta().code || currentLanguage();
  return `${new Intl.NumberFormat(locale, { maximumFractionDigits: 1 }).format(scaled)} ${units[index]}`;
};

export function createAcomController({ state, setScreen, toast, icon }) {
  const local = {
    previousScreen: 'welcome',
    host: { status: 'probing', token: null, version: null },
    action: { status: 'idle', lastAction: null, data: null, mock: false },
    downloads: { setup: 'checking', source: 'checking' }
  };

  function renderResult() {
    const result = document.getElementById('acom-result');
    const { status, lastAction, data, mock } = local.action;
    result.hidden = status === 'idle';
    if (status === 'idle') return;
    setText('result-kicker', mock ? a('demoKicker') : a('resultKicker'));
    setText('result-orb', status === 'ok' ? '✓' : status === 'pending' ? '…' : status === 'cancelled' ? '×' : '!');
    const titles = {
      pending: a('pending'), ok: lastAction === 'extract' ? a('okExtract') : a('okPack'),
      cancelled: a('cancelled'), error: a('error'), unavailable: a('unavailable')
    };
    setText('result-title', titles[status] || a('error'));
    const details = {
      pending: a('pendingDetail'), ok: data?.message || '',
      cancelled: data?.message || a('cancelledDetail'), error: data?.message || a('errorDetail'),
      unavailable: a('unavailableDetail')
    };
    setText('result-message', details[status] || a('networkError'));
    const metrics = document.getElementById('result-metrics');
    if (status === 'ok' && data) {
      metrics.hidden = false;
      const rows = [];
      if (Number.isFinite(data.files)) rows.push(`<span><strong>${data.files}</strong> ${a('files')}</span>`);
      if (Number.isFinite(data.inputBytes)) rows.push(`<span>${a('input')}: <strong>${formatBytes(data.inputBytes)}</strong></span>`);
      if (Number.isFinite(data.outputBytes)) rows.push(`<span>${a('output')}: <strong>${formatBytes(data.outputBytes)}</strong></span>`);
      const destination = data.destination || data.outputPath || data.path || data.folder;
      if (destination) rows.push(`<span class="result-destination">${a('destination')}: <code>${String(destination).replace(/[&<>"']/g, (char) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[char])}</code></span>`);
      metrics.innerHTML = rows.join('');
    } else {
      metrics.hidden = true;
      metrics.innerHTML = '';
    }
    result.dataset.status = status;
  }

  function render() {
    for (const [id, key] of Object.entries({
      'acom-back': 'back', 'acom-kicker': 'kicker', 'acom-title': 'title', 'acom-intro': 'intro',
      'acom-brand-subtitle': 'brandSubtitle', 'host-kicker': 'hostKicker', 'host-refresh': 'refresh',
      'install-kicker': 'installKicker', 'install-title': 'installTitle', 'acom-uri-label': 'openInstalled',
      'acom-setup-label': 'downloadSetup', 'acom-source-label': 'downloadSource', 'principles-kicker': 'principlesKicker',
      'acom-demo-summary': 'demoSummary', 'acom-demo-copy': 'demoCopy', 'acom-demo-ok': 'demoOk',
      'acom-demo-cancelled': 'demoCancelled', 'acom-demo-error': 'demoError',
      'principles-title': 'principlesTitle', 'acom-sample': 'sampleLink', 'sample-note': 'sampleNote'
    })) setText(id, a(key));
    for (const [index, key] of ['step1', 'step2', 'step3', 'step4'].entries()) {
      const item = document.querySelectorAll('.install-steps li')[index];
      if (item) item.textContent = a(key);
    }
    for (const [index, key] of ['principle1', 'principle2', 'principle3', 'principle4'].entries()) {
      const item = document.querySelectorAll('.acom-principles li')[index];
      if (item) item.textContent = a(key);
    }
    const actionText = {
      'pack-files': ['packFiles', 'packFilesDetail'], 'pack-folder': ['packFolder', 'packFolderDetail'], extract: ['extract', 'extractDetail']
    };
    for (const button of document.querySelectorAll('[data-acom-action]')) {
      const [titleKey, detailKey] = actionText[button.dataset.acomAction];
      button.querySelector('strong').textContent = a(titleKey);
      button.querySelector('span:not(.acom-action-icon)').textContent = a(detailKey);
      button.disabled = local.action.status === 'pending';
    }
    const hostTitles = { probing: a('hostProbing'), online: a('hostOnline'), offline: a('hostOffline'), error: a('hostOffline') };
    const hostDetails = {
      probing: a('hostProbingDetail'), online: a('hostOnlineDetail'),
      offline: a('hostOfflineDetail'), error: `${a('hostOfflineDetail')} ${local.host.message || a('networkError')}`
    };
    setText('host-title', hostTitles[local.host.status] || a('hostOffline'));
    setText('host-detail', hostDetails[local.host.status] || a('hostOfflineDetail'));
    document.getElementById('host-orb').dataset.status = local.host.status;
    document.getElementById('acom-setup').hidden = local.host.status === 'online';
    const setupStatus = local.host.status === 'online' ? 'installed' : local.downloads.setup === 'available' ? 'setupAvailable' : local.downloads.setup === 'unavailable' ? 'setupUnavailable' : 'setupChecking';
    const sourceStatus = local.downloads.source === 'available' ? 'sourceAvailable' : local.downloads.source === 'unavailable' ? 'sourceUnavailable' : 'sourceChecking';
    setText('setup-status', a(setupStatus));
    setText('source-status', a(sourceStatus));
    renderResult();
  }

  function openAcom() {
    if (state.screen !== 'acom') {
      local.previousScreen = state.screen;
      local.previousScroll = window.scrollY;
    }
    setScreen('acom');
    window.scrollTo({ top: 0, behavior: 'instant' });
    history.pushState({ acom: true }, '', `${location.pathname}?ferramenta=acom`);
    render();
  }

  function back() {
    setScreen(local.previousScreen || 'welcome');
    window.scrollTo({ top: local.previousScroll || 0, behavior: 'instant' });
    history.pushState({}, '', location.pathname);
  }

  async function refreshHost() {
    local.host.status = 'probing';
    render();
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 1800);
    try {
      const response = await fetch('/acom-api/status', { headers: { Accept: 'application/json' }, signal: controller.signal, cache: 'no-store' });
      const type = response.headers.get('content-type') || '';
      if (!response.ok || !type.includes('application/json')) throw new Error(a('networkError'));
      const body = await response.json();
      if (body.native !== true || typeof body.token !== 'string' || !body.token || typeof body.version !== 'string') throw new Error(a('networkError'));
      local.host = { status: 'online', token: body.token, version: body.version };
    } catch (error) {
      local.host = { status: 'offline', token: null, version: null, message: error.name === 'AbortError' ? a('networkError') : error.message };
    } finally {
      clearTimeout(timer);
      render();
    }
  }

  async function action(name) {
    if (local.host.status !== 'online') {
      local.action = { status: 'unavailable', lastAction: name, data: null, mock: false };
      renderResult();
      return;
    }
    local.action = { status: 'pending', lastAction: name, data: null, mock: false };
    render();
    try {
      const lang = languageMeta().fallback || currentLanguage();
      const response = await fetch('/acom-api/action', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-ACOM-Token': local.host.token },
        body: JSON.stringify({ action: name, lang })
      });
      const type = response.headers.get('content-type') || '';
      if (!response.ok || !type.includes('application/json')) throw new Error(a('networkError'));
      const body = await response.json();
      if (!['ok', 'cancelled', 'error'].includes(body.status)) throw new Error(a('networkError'));
      local.action = { status: body.status, lastAction: name, data: body, mock: body.demonstration === true };
    } catch (error) {
      local.action = { status: 'error', lastAction: name, data: { message: error.message || a('networkError') }, mock: false };
    }
    render();
  }

  function mock(status) {
    local.action = {
      status,
      lastAction: 'pack-files',
      data: { files: 3, inputBytes: 1048576, outputBytes: 65536, message: a('demoMessage') },
      mock: true
    };
    renderResult();
  }

  async function checkDownload(kind) {
    const url = kind === 'setup' ? '/downloads/ACOM-Setup.exe' : '/downloads/ACOM-fonte.zip';
    try {
      const response = await fetch(url, { method: 'HEAD', cache: 'no-store' });
      local.downloads[kind] = response.ok ? 'available' : 'unavailable';
    } catch {
      local.downloads[kind] = 'unavailable';
    }
    render();
  }

  function init() {
    document.getElementById('acom-back').addEventListener('click', back);
    document.getElementById('host-refresh').addEventListener('click', refreshHost);
    for (const button of document.querySelectorAll('[data-acom-action]')) {
      button.addEventListener('click', () => action(button.dataset.acomAction));
    }
    for (const button of document.querySelectorAll('[data-acom-mock]')) {
      button.addEventListener('click', () => mock(button.dataset.acomMock));
    }
    document.getElementById('acom-uri').addEventListener('click', () => toast(a('uriNotice')));
    for (const kind of ['setup', 'source']) {
      const link = document.getElementById(`acom-${kind}`);
      link.addEventListener('click', (event) => {
        if (local.downloads[kind] !== 'available') {
          event.preventDefault();
          toast(a('downloadUnavailable'));
        }
      });
    }
    render();
    refreshHost();
    checkDownload('setup');
    checkDownload('source');
  }

  return {
    init, openAcom, back, refreshHost, render, mock,
    getState: () => JSON.parse(JSON.stringify(local)),
    setActionForTest: (status, data = null) => { local.action = { status, lastAction: 'pack-files', data, mock: false }; renderResult(); }
  };
}
