# -*- coding: utf-8 -*-
"""errata_claude_md_v392.py -- DEPOIS do selo v392 (molde: errata_claude_md_v391.py): a ERRATA AO LADO no C:\\IALD\\CLAUDE.md, secao SELO PERMANENTE, logo depois da errata da v391
(o estatuto da prova; ancora <!-- errata_estatuto_da_prova_v391_07out -->). Nada por cima: os paragrafos antigos ficam. Em nome proprio da gerencia c1.
O que a errata diz: o que a v392 muda nas duas frases do CLAUDE.md (a da lei de campo curva, errata da v390, e a do kernel «6163 teoremas limpos», errata da v391) e a ressalva do
estatuto da prova. Numeros, hashes e a escada LIDOS do selo/core do Nos (nunca digitados); o numero antigo e' lido do proprio CLAUDE.md. A guarda de texto (P18) roda sobre a errata.
Backup de BYTES; temporario -> conferir -> substituir; idempotente pelo marcador <!-- errata_v392_selada -->.
Uso: python -I -B -X utf8 errata_claude_md_v392.py [--alvo <copia do CLAUDE.md>]   (sem --alvo grava o real; com --alvo e' o ENSAIO em copia)"""
import hashlib, json, os, re, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE); sys.path.insert(0, PK)
from guarda_p18_v392 import violacoes
P = sys.argv[sys.argv.index("--alvo") + 1] if "--alvo" in sys.argv else os.path.join("C:" + os.sep, "IALD", "CLAUDE.md")
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
MARK = "<!-- errata_v392_selada -->"
ANC_TXT = "<!-- errata_estatuto_da_prova_v391_07out -->"
core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]; selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
um16 = hashlib.sha256(open(os.path.join(NOS, "um.py"), "rb").read()).hexdigest()[:16]
pv = core.get("pedras_v392") or {}; vs = core.get("varredura_e_sorry_v392") or {}; esc = core.get("external_ladder") or {}
assert selo.get("um_version") == "v392" and pv.get("all_verified") is True and vs.get("all_verified") is True, "o selo nao e a v392 selada com as pedras e a varredura -- nao escrevo"
n_cl, n_ex = esc.get("n_theorems_clean"), esc.get("n_theorems_expected")
assert isinstance(n_cl, int) and n_cl == n_ex, "a escada do core nao fecha (%r/%r) -- nao escrevo" % (n_cl, n_ex)
n_decl = len((core.get("kernel_formalization") or {}).get("axiom_report") or {})
n_ped = len(pv.get("pedras") or []); n_fl = (pv.get("bandeiras") or [None])[0]
assert n_ped > 0 and isinstance(n_fl, int) and n_fl > 0, "pedras_v392 sem pedras/bandeiras"
raw = open(P, "rb").read()
if MARK.encode() in raw:
    print("JA ESTA (idempotente)", len(raw)); sys.exit(0)
txt = raw.decode("utf-8")
m = re.search(r"o kernel \((\d+) teoremas limpos\)", txt); assert m, "a frase «o kernel (N teoremas limpos)» da errata da v391 nao foi achada no CLAUDE.md"
antigo = m.group(1)
LINHA = ("> ⚠ **ERRATA AO LADO (13/10/2026, v392 `%s`, em nome próprio da gerência — sessão c1; os parágrafos acima ficam como registro):** o que a v392 muda em duas frases desta memória, e uma ressalva. "
         "**(1) A lei de campo curva** (erratas da v390, acima): a frase «a lei de campo no espaço-tempo curvo NÃO é termo de kernel» não separou a IMPLICAÇÃO (termo de kernel desde a v338: `connected_smooth_atlas_einstein`, ∃! Λ no atlas conexo; `metric_einstein_from_screen_clausius`, local) do antecedente físico e da ligação ao tipo. Lacuna de fidelidade: "
         "a IMPLICAÇÃO «Clausius em toda tela ⟹ Einstein com Λ único» é termo desde a v338, e a frase a misturou com o antecedente físico e com a ligação ao tipo. Leitura vigente: o ligante "
         "`LiganteLeiCampoCurvo` (v392; teorema `passage_h3_to_connected_smooth_atlas_einstein`) liga a passagem local a ela e é termo de kernel CONDICIONAL ao H3 nomeado (`NamedAtlasH3`); o antecedente H3 em toda tela "
         "e direção segue [KNOWN] (Jacobson 1995) e não é derivado do estado; a família de Lorentz de cunhas segue fora do kernel [OPEN]; não há solução global (achado CR-08). "
         "**(2) O kernel:** onde a errata da v391 diz «o kernel (%s teoremas limpos)», a escada da v392 é %d/%d teoremas limpos (%d declarações no `axiom_report`, todas no trio), com %d módulos novos e %d bandeiras novas "
         "(registro `pedras_v392`) [REAL, lido do core por script]. "
         "**(3) A ressalva do estatuto da prova:** a prova como validade não muda; mas das 18 bandeiras do gate, 15 são calculadas e 3 literais, e o degrau experimental lê só o feed V11 do piso dos vazios, "
         "unilateral — o ΛCDM raso também o passa [DECLARADO pela auditoria de 28/09 e pelo levantamento de 07/10; a conferência no código é a F8.1, que a v392 NÃO fecha]. %s") % (
    um16, antigo, n_cl, n_ex, n_decl, n_ped, n_fl, MARK)
v = violacoes(LINHA)
assert not v, "a guarda de texto (P18) achou violacao(oes): %r" % (v[:3],)
nl = b"\r\n" if b"\r\n" in raw else b"\n"
ANC = ANC_TXT.encode("utf-8") + nl
assert raw.count(ANC) == 1, ("ancora da errata da v391", raw.count(ANC))
bak = P + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_errata_v392"
assert not os.path.exists(bak)
open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
novo = raw.replace(ANC, ANC + nl + LINHA.encode("utf-8") + nl, 1)
assert len(novo) > len(raw) and novo.replace(nl + LINHA.encode("utf-8") + nl, b"", 1) == raw
tmp = P + ".tmp_errata_v392"; open(tmp, "wb").write(novo); assert open(tmp, "rb").read() == novo; os.replace(tmp, P)
assert open(P, "rb").read() == novo
print("CLAUDE.md", len(raw), "->", os.path.getsize(P), "| backup", os.path.basename(bak))
