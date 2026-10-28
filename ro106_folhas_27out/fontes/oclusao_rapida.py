# Roda SO os dois testes novos (oclusao e marcacao do RO) num PDF. Uso: python oclusao_rapida.py <pdf> [rotulo]
import sys, json, pathlib
sys.path.insert(0, r'C:\IALD\Central de Patentes\work\ro106_folhas_27out\fontes')
import conferir as C
import fitz
pdf = sys.argv[1]
doc = fitz.open(pdf)
res = []
for i, pg in enumerate(doc):
    o = C.oclusao(pg)
    r = C.marcacao_RO(pg)
    res.append({'folha': i + 1, 'oclusoes': o, 'marcacao_RO': r})
    print(i + 1, 'oclusoes:', len(o), [(x['fundo_branco_caixa_cm'], x['pontos_de_traco_cobertos'], x['tipos']) for x in o][:8], '| RO livre:', r['livres'], {k: v for k, v in r.items() if k not in ('livres',)})
if len(sys.argv) > 2:
    pathlib.Path(r'C:\IALD\Central de Patentes\work\ro106_folhas_27out\conferencia').joinpath('oclusao_%s.json' % sys.argv[2]).write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding='utf-8')
