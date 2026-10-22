from pathlib import Path
import re

root = Path(__file__).parent / 'stage'
p = root / 'app/iald.js'
s = p.read_text(encoding='utf-8')
s = s.replace('function protectMath(texto) {', 'function protectMath(texto, streaming = false) {')
s = s.replace('  t = t.replace(new RegExp(`${prefix}CODE', '''  // An unfinished display/inline TeX expression stays literal until its closing
  // delimiter arrives. Never let Markdown consume its backslashes mid-stream.
  if (streaming) {
    t = t.replace(/\\\\\\[([\\s\\S]*)$|\\\\\\(([\\s\\S]*)$|\\$\\$([\\s\\S]*)$/g, (raw) => {
      formulas.push({ pending: true, eq: raw });
      return `${prefix}MATH${formulas.length - 1}END`;
    });
  }
  t = t.replace(new RegExp(`${prefix}CODE''')
s = s.replace('function renderMarkdown(bruto) {\n  const protectedText = protectMath(aplicarPtbr(bruto || \'\'));', '''const mathRenderCache = new Map();
function renderMarkdown(bruto, streaming = false) {
  const protectedText = protectMath(aplicarPtbr(bruto || ''), streaming);''')
s = s.replace('    if (!window.katex) return literal();', '''    if (f.pending) return '<span class="iald-math-pending">' + literal() + '</span>';
    if (!window.katex) return literal();
    const cacheKey = JSON.stringify([f.bloco, f.eq]);
    if (mathRenderCache.has(cacheKey)) return mathRenderCache.get(cacheKey);''')
s = s.replace('      return window.katex.renderToString(f.eq, {', '      const rendered = window.katex.renderToString(f.eq, {')
s = s.replace("displayMode: f.bloco, throwOnError: false, trust: false, output: 'html',\n      });", "displayMode: f.bloco, throwOnError: false, trust: false, output: 'html',\n      });\n      if (mathRenderCache.size >= 128) mathRenderCache.delete(mathRenderCache.keys().next().value);\n      mathRenderCache.set(cacheKey, rendered);\n      return rendered;")
# Do not rewrite formula operators, labels, or code with the prose accent fixer.
a=s.index('function aplicarPtbr(t) {'); b=s.index('\n}\n',a)+2
s=s[:a]+'''function aplicarPtbr(t) {
  if (!t) return t;
  const protectedParts = [];
  let prefix = 'IALDPTBRTOKEN';
  while (t.includes(prefix)) prefix += 'X';
  const pattern = /(`{3,}|~{3,})[^\\n]*\\n[\\s\\S]*?(?:\\n\\1[ \\t]*(?=\\n|$)|$)|(`+)[^\\n]*?\\2(?!`)|\\\\\\[[\\s\\S]*?(?:\\\\\\]|$)|\\\\\\([\\s\\S]*?(?:\\\\\\)|$)|\\$\\$[\\s\\S]*?(?:\\$\\$|$)|\\$[^$\\n]+\\$/g;
  t = t.replace(pattern, (part) => { protectedParts.push(part); return `${prefix}${protectedParts.length - 1}END`; });
  for (const k in PTBR_FIXES) t = t.replace(new RegExp('\\\\b' + k + '\\\\b', 'g'), PTBR_FIXES[k]);
  return t.replace(new RegExp(`${prefix}(\\\\d+)END`, 'g'), (_, i) => protectedParts[+i]);
}'''+s[b:]
# Throttle repaint, preserve already-rendered paragraphs and horizontal formula scroll.
s=s.replace('  const pintar = () => {\n    if (retirada) return;\n    conteudo.innerHTML = \'\';', '''  let paintTimer = null, streamFinished = false;
  let answerNode = null;
  const pintarAgora = () => {
    if (retirada) return;''')
s=s.replace('      conteudo.appendChild(detalhesPensamento);\n    }\n    if (texto) conteudo.appendChild(renderMarkdown(texto));', '''      if (!detalhesPensamento.isConnected) conteudo.appendChild(detalhesPensamento);
    }
    if (texto) {
      const next = renderMarkdown(texto, !streamFinished);
      if (!answerNode) { answerNode = next; conteudo.appendChild(answerNode); }
      else {
        const oldNodes = Array.from(answerNode.childNodes);
        const newNodes = Array.from(next.childNodes);
        newNodes.forEach((node, i) => {
          const old = oldNodes[i];
          if (!old) answerNode.appendChild(node);
          else if (!old.isEqualNode(node)) answerNode.replaceChild(node, old);
        });
        oldNodes.slice(newNodes.length).forEach((node) => node.remove());
      }
    }''')
needle='  const tirarDigitando = () => {'
s=s.replace(needle, '''  const pintar = () => {
    if (paintTimer === null) paintTimer = setTimeout(() => {
      paintTimer = null; pintarAgora();
    }, 80);
  };

'''+needle)
# Content and reasoning may coexist in a delta; neither gets silently discarded.
s=s.replace('        pensamento += delta.reasoning_content;\n        pintar();\n        continue;', '        pensamento += delta.reasoning_content;\n        pintar();')
a=s.index('      // O modelo tambem pode marcar raciocinio'); b=s.index('\n      pintar();',a)
s=s[:a]+'''      const separated = splitThinking(bruto);
      texto = separated.text;
      if (separated.thinking) pensamento = separated.thinking;'''+s[b:]
s=s.replace("  } finally {\n    tirarDigitando();\n    congelarTrilha(trilha);", "  } finally {\n    if (paintTimer !== null) clearTimeout(paintTimer);\n    streamFinished = true;\n    texto = splitThinking(bruto, true).text;\n    pintarAgora();\n    tirarDigitando();\n    congelarTrilha(trilha);")
# Reader now follows SSE events, UTF-8 boundaries and reader cancellation.
a=s.index('  const leitor = r.body.getReader();',s.index('async function* fluxoHttp')); b=s.index('\n}\n',a)
s=s[:a]+'''  if (!r.body) throw new Error('Resposta sem fluxo de dados.');
  const leitor = r.body.getReader();
  const dec = new TextDecoder();
  const parser = createSSEParser();
  let complete = false;
  try {
    for (;;) {
      const { done, value } = await leitor.read();
      const events = parser.feed(done ? dec.decode() : dec.decode(value, { stream: true }), done);
      for (const data of events) {
        yield 'data: ' + data;
        if (data.trim() === '[DONE]') { complete = true; return; }
      }
      if (done) break;
    }
    if (!complete) throw new Error('A resposta foi interrompida antes da conclusão.');
  } finally {
    try { await leitor.cancel(); } catch (_) { /* already closed/aborted */ }
    leitor.releaseLock();
  }'''+s[b:]
insert=s.index('// gerador assincrono de linhas do SSE')
s=s[:insert]+'''// Shared protocol handling, independent of the selected inference provider.
function createSSEParser() {
  let buffer = '', data = [];
  return { feed(part, final = false) {
    buffer += part;
    const events = [];
    const line = (value) => {
      if (!value) { if (data.length) events.push(data.join('\\n')); data = []; }
      else if (value.startsWith('data:')) data.push(value.slice(5).replace(/^ /, ''));
    };
    let match;
    while ((match = /\\r\\n|\\r|\\n/.exec(buffer))) {
      if (match[0] === '\\r' && match.index === buffer.length - 1 && !final) break;
      line(buffer.slice(0, match.index));
      buffer = buffer.slice(match.index + match[0].length);
    }
    if (final) { if (buffer) line(buffer); buffer = ''; line(''); }
    return events;
  }};
}

function splitThinking(raw, final = false) {
  let text = '', thinking = '', inside = false, pos = 0;
  while (pos < raw.length) {
    const tag = inside ? '</think>' : '<think>';
    const end = raw.indexOf(tag, pos);
    if (end >= 0) {
      if (inside) thinking += raw.slice(pos, end); else text += raw.slice(pos, end);
      inside = !inside; pos = end + tag.length;
    } else {
      let rest = raw.slice(pos);
      if (!final) for (let n = tag.length - 1; n > 0; n--) {
        if (rest.endsWith(tag.slice(0, n))) { rest = rest.slice(0, -n); break; }
      }
      if (inside) thinking += rest; else text += rest;
      break;
    }
  }
  return { text, thinking };
}

'''+s[insert:]
p.write_text(s,encoding='utf-8',newline='\r\n')
css=root/'app/iald.css'
css.write_text(css.read_text(encoding='utf-8')+'\n/* Keep partial TeX legible until its closing delimiter arrives. */\n.iald-math-pending { display:inline-block; max-width:100%; overflow-x:auto; vertical-align:middle; }\n.iald-math-pending code { white-space:pre-wrap; overflow-wrap:anywhere; opacity:.78; }\n',encoding='utf-8',newline='\r\n')
print('Client changes staged')
