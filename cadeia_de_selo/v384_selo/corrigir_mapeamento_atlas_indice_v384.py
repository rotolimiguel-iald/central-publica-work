# -*- coding: utf-8 -*-
"""CORRECAO do mapeamento versao -> sha16 do atlas_indice.py (aferidor das superficies v384, defeito ALTO: a regeneracao de 04/10 18:13 gravou v382 e v383
com o hash da v381; v371-v381 deslocados uma versao desde a v371). Causa: casava o hash de cada backup um.py.bak_* com a PRIMEIRA versao citada perto dele no
diario, mas cada backup e' o um.py da versao ANTERIOR e o diario escreve «vNNN sobre a vNNN-1 `hash`». Agora: (1) PRIMARIO -- o cabecalho de selo do diario
«## dd/mm/aaaa — **vNNN SELADA (...)** `sha16`» (a ultima ocorrencia por versao); (2) SECUNDARIO -- a frase «**A vNNN** (`sha16`» (o caso da v382, selada so no
Nos); (3) so para versoes SEM nenhuma das duas fontes, a regra antiga, MARCADA com † («nao conferido») e explicada numa nota sob a tabela. A versao corrente
segue lida do disco. Backup de BYTES do gerador; count == 1; ast. NAO roda o gerador (a gerencia o roda depois)."""
import ast, hashlib, os, time
P = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "work", "cadeia_de_selo", "atlas_indice.py")
raw = open(P, "rb").read(); s = raw.decode("utf-8")
bak = P + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_mapa384"; open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
PAIRS = [
    ('''sha_de = {}
for b in baks:
    h = sha16(os.path.join(NOS, b))
    for mm in re.finditer(r'(v3\\d\\d)[^\\n]{0,200}?`%s`' % h, linh):
        sha_de.setdefault(mm.group(1), h)
sha_de[VER] = um_sha
''', '''sha_de = {}; sha_fonte = {}
# (1) PRIMARIO (04/10/2026, aferidor das superficies v384): o cabecalho de selo do diario -- a ultima ocorrencia por versao
for mm in re.finditer(r'(?m)^#{1,3} [^\\n]*?\\*\\*(v3\\d\\d) SELADA[^*\\n]*\\*\\*[^\\n`]*`([0-9a-f]{16})`', linh):
    sha_de[mm.group(1)] = mm.group(2); sha_fonte[mm.group(1)] = 'selo'
# (2) SECUNDARIO: «**A vNNN** (`sha16`» (a v382, selada so no Nos)
for mm in re.finditer(r'\\*\\*A (v3\\d\\d)\\*\\* \\(`([0-9a-f]{16})`', linh):
    if mm.group(1) not in sha_de:
        sha_de[mm.group(1)] = mm.group(2); sha_fonte[mm.group(1)] = 'frase'
# (3) so sem (1) nem (2): a regra antiga (backup <-> diario por proximidade), MARCADA † -- NAO conferida (ela deslocava uma versao: cada backup e' o um.py da ANTERIOR)
for b in baks:
    h = sha16(os.path.join(NOS, b))
    for mm in re.finditer(r'(v3\\d\\d)[^\\n]{0,200}?`%s`' % h, linh):
        if mm.group(1) not in sha_de:
            sha_de[mm.group(1)] = h; sha_fonte[mm.group(1)] = 'antiga'
sha_de[VER] = um_sha; sha_fonte[VER] = 'disco'
'''),
    ('''    L.append('| %s | `%s` | %s | %d | %s |' % (v, sha_de.get(v, '—'), stdout_count(v) if stdout_count(v) else '—', len(mods), ', '.join(proc)))''',
     '''    L.append('| %s | `%s`%s | %s | %d | %s |' % (v, sha_de.get(v, '—'), ' †' if sha_fonte.get(v) == 'antiga' else '', stdout_count(v) if stdout_count(v) else '—', len(mods), ', '.join(proc)))'''),
    ('''L += ['', '## 2. As pedras do arco, por versão (nome → teoremas; procedência)', '']''',
     '''L += ['', '> Fonte do hash (04/10/2026): o cabeçalho de selo do diário («**vNNN SELADA …** `sha16`»), ou a frase «**A vNNN** (`sha16`»; a versão corrente, do disco. '
      '**†** = sem nenhuma das duas fontes: valor da regra antiga (backup ↔ diário por proximidade), **não conferido** — essa regra deslocava uma versão '
      '(ver a errata de 04/10/2026 no §7).', '',
      '## 2. As pedras do arco, por versão (nome → teoremas; procedência)', '']'''),
]
for old, new in PAIRS:
    c = s.count(old); assert c == 1, (c, old[:120])
    s = s.replace(old, new)
ast.parse(s)
b = s.encode("utf-8"); open(P + ".tmp", "wb").write(b); assert os.path.getsize(P + ".tmp") == len(b); os.replace(P + ".tmp", P); assert open(P, "rb").read() == b
print("ok", len(PAIRS), hashlib.sha256(b).hexdigest()[:16], "| backup", os.path.basename(bak))
