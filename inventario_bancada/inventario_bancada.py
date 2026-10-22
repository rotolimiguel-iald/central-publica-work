# -*- coding: utf-8 -*-
"""inventario_bancada.py -- INVENTARIO de tudo o que a bancada do ChatGPT examinou e produziu (SO LEITURA da pasta Chatgpt\).
Ordem do operador (27/09/2026): «Precisamos fazer um inventário de tudo que foi examinado e produzido na bancada do chatgpt pra não
nos perdermos mais em serviço já executado» + «Depois de inventariar tudo, precisamos indexar ao atlas da tgl».
Varre Chatgpt\ (pula .lake, .git, node_modules, tex_environment, __pycache__, e as pastas privadas/de estado do orquestrador).
Para cada .lean: sha16 (bytes), declaracoes (tipo, nome, namespace), tokens proibidos, e se esta no kernel canonico (mesmo sha16 de
bytes, ou mesmo conteudo modulo a transformacao O16) e se os nomes estao no axiom_report do selo corrente. Para cada documento de
entrega (ENTREGA_*, PRONTO.json, *QUADRO*, RELATORIO*, MEDIDA*, P1..P9, PROGRESSO): sha16, tamanho, 1o titulo. Etiqueta por tema.
Saidas (fora da pasta Chatgpt\): inventario_bancada.json + INVENTARIO_BANCADA_CHATGPT.md no scratchpad."""
import hashlib, json, os, re, sys, time
sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'C:\IALD\Central de Patentes\Chatgpt'
NOS = r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós'
KER = os.path.join(NOS, 'tgl_kernel')
OUT = os.path.dirname(os.path.abspath(__file__))
SKIP = {'.lake', '.git', 'node_modules', 'tex_environment', '__pycache__', 'state', 'profiles', 'build', '.venv', 'venv'}
DOC_RE = re.compile(r'(ENTREGA_|PRONTO\.json$|QUADRO|RELATORIO|MEDIDA|^P[1-9]_|PROGRESSO|RECIBO|MAPA|INVENTARIO|README|LEIA)', re.I)
DECL = re.compile(r"^\s*(?:@\[[^\]]*\]\s*)*(?:(?:private|protected|noncomputable|partial|unsafe|scoped)\s+)*"
                  r"(theorem|lemma|def|structure|abbrev|instance|inductive|class)\s+([A-Za-z_\u0370-\u03ff][A-Za-z0-9_'!?\u0370-\u03ff.]*)", re.M)
NS = re.compile(r"^\s*namespace\s+(\S+)", re.M)
TEMAS = [
    ('rede_K_subespaco_padrao', r'StandardSubspace|standardSubspace|symplComp|K_mono|K_local|K_boost|K_translate|halfline|isotony|Borchers|BGL|localiza'),
    ('wigner_orbita_poincare', r'Wigner|orbital|Orbital|rapidity|Rapidity|helicit|Helicit|massShell|MassShell|littleGroup'),
    ('fock_segunda_quantizacao', r'Fock|fock|secondQuant|SecondQuant|Gamma_|Weyl|weyl|exponentialVector|coherent|Coherent'),
    ('tomita_modular', r'Tomita|tomita|modular|Modular|Delta|polar|Polar|conjugation'),
    ('kms_bw', r'KMS|kms|Bisognano|BW|Unruh|strip|Strip'),
    ('maxwell_tensor_ctt', r'Maxwell|maxwell|stress|Stress|nullEnergy|charge|Charge|CTT|Wall'),
    ('nucleo_traco_takesaki', r'Core|core|trace|Trace|crossed|Crossed|dual|Dual|Connes|Breuer'),
    ('contrato_H2_H3', r'Contrato|contrato|ContratoH|H2|H3|horizon|Horizon|Clausius|Raychaudhuri'),
    ('operadores_ilimitados', r'Unbounded|unbounded|Graph|graph|Resolvent|resolvent|BoundedTransform|closed'),
    ('ringdown_gw', r'ringdown|Ringdown|QNM|qnm|echo|Echo|GW150914|kerr|Kerr'),
    ('susy_locks', r'Susy|SUSY|susy|Lock|lock|ThreeLocks'),
]


def h16b(p):
    with open(p, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()[:16]


def reverse_o16(t):
    t = re.sub(r"^import TGLExt\.O16\.(\S+)[ \t]*$", r"import \1", t, flags=re.M)
    t = re.sub(r"^([ \t]*)local instance (?:instLocal|instModuleRealSH|instNormedSpaceRealSH)[A-Za-z0-9]* :", r"\1local instance :", t, flags=re.M)
    return t


t0 = time.time()
# o kernel canonico: sha16 de bytes e sha16 do texto revertido (O16)
ker_bytes, ker_text = {}, {}
for dp, dn, fn in os.walk(KER):
    dn[:] = [d for d in dn if d not in SKIP]
    for f in fn:
        if f.endswith('.lean'):
            p = os.path.join(dp, f); rel = os.path.relpath(p, KER).replace('\\', '/')
            b = open(p, 'rb').read()
            ker_bytes[hashlib.sha256(b).hexdigest()[:16]] = rel
            try:
                ker_text[hashlib.sha256(reverse_o16(b.decode('utf-8')).encode('utf-8')).hexdigest()[:16]] = rel
            except UnicodeDecodeError:
                pass
core = json.load(open(os.path.join(NOS, 'um_absoluto.json'), encoding='utf-8'))['core']
axr = (core.get('kernel_formalization') or {}).get('axiom_report') or {}
axr_suf = set()
for k in axr:
    parts = k.split('.')
    for i in range(len(parts)):
        axr_suf.add('.'.join(parts[i:]))

leans, docs, pastas = [], [], {}
for dp, dn, fn in os.walk(ROOT):
    dn[:] = [d for d in dn if d not in SKIP and not d.startswith('.')]
    rel_dir = os.path.relpath(dp, ROOT).replace('\\', '/')
    top = rel_dir.split('/')[0] if rel_dir != '.' else '.'
    for f in fn:
        p = os.path.join(dp, f)
        rel = os.path.relpath(p, ROOT).replace('\\', '/')
        pastas.setdefault(top, {'lean': 0, 'docs': 0, 'outros': 0})
        if f.endswith('.lean'):
            try:
                b = open(p, 'rb').read(); t = b.decode('utf-8', errors='replace')
            except OSError:
                continue
            s16 = hashlib.sha256(b).hexdigest()[:16]
            decls = [(k, n) for k, n in DECL.findall(t)]
            nss = NS.findall(t)
            no_kernel = ker_bytes.get(s16) or ker_text.get(hashlib.sha256(t.encode('utf-8')).hexdigest()[:16])
            nomes = [n for _, n in decls]
            em_axr = sum(1 for n in nomes if n in axr_suf or (nss and (nss[0] + '.' + n) in axr_suf))
            proib = [w for w in ('sorry', 'admit', 'native_decide') if re.search(r'(?<![A-Za-z_])' + w + r'(?![A-Za-z_])', re.sub(r'--.*|/-.*?-/', '', t, flags=re.S))]
            has_axiom = bool(re.search(r'^\s*axiom\s', t, re.M))
            temas = [nm for nm, rx in TEMAS if re.search(rx, rel + ' ' + ' '.join(nomes))]
            leans.append({'arquivo': rel, 'sha16': s16, 'bytes': len(b), 'n_decl': len(decls), 'namespaces': nss[:3],
                          'decls': [k + ' ' + n for k, n in decls][:400], 'no_kernel_canonico': no_kernel, 'nomes_no_axiom_report': em_axr,
                          'tokens_proibidos_fora_de_comentario': proib, 'declara_axiom': has_axiom, 'temas': temas,
                          'mtime': time.strftime('%Y-%m-%d %H:%M', time.localtime(os.path.getmtime(p)))})
            pastas[top]['lean'] += 1
        elif DOC_RE.search(f) and f.lower().endswith(('.md', '.json', '.txt')):
            try:
                t = open(p, encoding='utf-8', errors='replace').read(4000)
            except OSError:
                continue
            m = re.search(r'^#\s+(.+)$', t, re.M)
            docs.append({'arquivo': rel, 'sha16': h16b(p), 'bytes': os.path.getsize(p), 'titulo': (m.group(1).strip() if m else t.strip().splitlines()[0][:160] if t.strip() else ''),
                         'mtime': time.strftime('%Y-%m-%d %H:%M', time.localtime(os.path.getmtime(p)))})
            pastas[top]['docs'] += 1
        else:
            pastas[top]['outros'] += 1

res = {'gerado_em': time.strftime('%Y-%m-%d %H:%M:%S'), 'raiz': ROOT, 'segundos': round(time.time() - t0, 1),
       'n_lean': len(leans), 'n_docs': len(docs), 'pastas': pastas, 'lean': leans, 'docs': docs,
       'n_lean_no_kernel': sum(1 for x in leans if x['no_kernel_canonico']),
       'n_decl_total': sum(x['n_decl'] for x in leans)}
json.dump(res, open(os.path.join(OUT, 'inventario_bancada.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in res.items() if k not in ('lean', 'docs', 'pastas')}, ensure_ascii=False))
print('pastas:', json.dumps(pastas, ensure_ascii=False)[:3000])
