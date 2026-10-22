# -*- coding: utf-8 -*-
"""editar_artigo_errata_d19c.py -- DELTA 19/10 (rodada d19c): acrescenta UMA frase de ERRATA AO LADO sobre a palavra «teoremas» ao artigo PT e EN da v394 (artigo_pt_v394.pysnip / artigo_en_v394.pysnip), no paragrafo
«O que entra» / «What enters» da secao da v394, logo depois da frase que da' a escada do kernel e a cobertura do axiom_report (a primeira ocorrencia da palavra). A frase vem de delta19_v394 (uma fonte so'); nenhum numero digitado.
Backup de BYTES antes (.bak_<STAMP>_c1d19c), temporario -> conferir tamanho -> substituir, idempotente. Os dois .pysnip sao insumos do candidato: mudar um muda o sha16 do candidato (regenerar com gerar_candidato_v394.py)."""
import hashlib, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); V = os.path.dirname(HERE); sys.path.insert(0, V)
import delta19_v394 as DL  # noqa: E402
sha = lambda b: hashlib.sha256(b).hexdigest()
FIM_FRASE = r'$\{\texttt{propext},\texttt{Classical.choice},\texttt{Quot.sound}\}$.")'
PLANO = (("artigo_pt_v394.pysnip", r'r" teoremas, nenhuma fora do trio ' + FIM_FRASE, r" \textit{Errata ao lado (em nome próprio da gerência c1):} " + DL.ERRATA_TEOREMAS_TEX_PT + "."),
         ("artigo_en_v394.pysnip", r'r" theorems, none outside the trio ' + FIM_FRASE, r" \textit{Side erratum (in the management's own name, c1):} " + DL.ERRATA_TEOREMAS_TEX_EN + "."))
stamp = time.strftime("%Y%m%d_%H%M%S")
for nome, ancora, frase in PLANO:
    p = os.path.join(V, nome); raw = open(p, "rb").read(); txt = raw.decode("utf-8")
    if frase in txt:
        print("JA APLICADO (idempotente):", nome); continue
    assert txt.count(ancora) == 1, (nome, "ancora nao unica", txt.count(ancora))
    assert '"' not in frase, "a frase nao pode ter aspas duplas (esta' dentro de r\"...\")"
    novo = txt.replace(ancora, ancora[:-len('")')] + frase + '")', 1)
    assert novo.count(frase) == 1 and len(novo) > len(txt)
    bak = p + ".bak_%s_c1d19c" % stamp; assert not os.path.exists(bak)
    open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
    tmp = p + ".tmp_c1d19c"; open(tmp, "wb").write(novo.encode("utf-8")); assert os.path.getsize(tmp) == len(novo.encode("utf-8")) > len(raw)
    os.replace(tmp, p)
    print("OK: %s %d B -> %d B (sha16 %s -> %s); backup %s" % (nome, len(raw), os.path.getsize(p), sha(raw)[:16], sha(open(p, "rb").read())[:16], os.path.basename(bak)))
