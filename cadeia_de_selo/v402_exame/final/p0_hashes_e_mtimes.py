import hashlib, os, sys, json, time
B = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'v402'))
NOS = os.path.join('C:'+os.sep, 'IALD', 'Artigo', 'Haja_Luz', 'A Ponte e o Um', 'Nós')
def h(p):
    d = hashlib.sha256()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''): d.update(c)
    return d.hexdigest()
tag = sys.argv[1]
out = {}
# Nós mtimes (whole tree, top+recursive except lake build dirs? do all but .lake)
mt = []
for root, dirs, files in os.walk(NOS):
    dirs[:] = [d for d in dirs if d not in ('.lake',)]
    for fn in files:
        p = os.path.join(root, fn)
        try:
            st = os.stat(p); mt.append(f"{os.path.relpath(p, NOS)}\t{st.st_size}\t{st.st_mtime_ns}")
        except OSError as e:
            mt.append(f"{os.path.relpath(p, NOS)}\tERR {e}")
mt.sort()
open(f'nos_mtimes_{tag}.txt', 'w', encoding='utf-8').write('\n'.join(mt) + '\n')
out['nos_n_arquivos'] = len(mt)
out['nos_um_py_sha16'] = h(os.path.join(NOS, 'um.py'))[:16]
if tag == 'antes':
    lista = """um_v402_candidato.py CANDIDATO_v402.json ESPERADOS_v402.json ensaio_a_seco_v402.json PINOS_BN_v402.json PINO_RECIBO_PRE_SELO_v402.json PINO_MEMORIA_PY_v402.json PROVA_PRODUCAO_INTACTA_v402_pre_selo.json PRECONDICOES_v402.json COMPARACAO_V401_v402.json GUARDAS_ESTATICAS_BANCADA_v402.json kernel/KERNEL_RECIBO_v402.json kernel/FLAGS_v402.json kernel/KH_N1_v402.json DIFF_KERNEL_v402.txt conferencia_rito_v402_CONTROLE_NEGATIVO_PRE_RITO.json conferencia_rito_v402_POSITIVO_FALSO_NOS.json conferir_citacoes_v402.json registros_v402.py runtime_v402.py delta_v402.py gerar_candidato_v402.py gerar_esperados_v402.py instalar_v402.py reverter_v402.py rito_v402.sh conferir_rito_v402.py regras_v402.py registro_mapa_v402_prep.json gerar_registro_mapa_prep_v402.py pedra/PonteDaEscalaDual.lean pedra/QuedaSemGeometria.lean pedra/EsperancaCondicional.lean pos_rito/chain_pos_rito_v402.sh pos_rito/textos_v402.py pos_rito/leitura_v402.py pos_rito/registrar_mapa_v402.py pos_rito/fechar_v402.py bateria_pre_selo/NOTAS_PRE_SELO_v402.txt bancada_B3_servico/CONFERENCIA_EXIGENCIAS_SERVICO_v402.json ESTADO_V402.md""".split()
    decl = {}
    for line in open(os.path.join(B, 'ESTADO_V402.md'), encoding='utf-8'):
        line = line.strip()
        if line.startswith('- `') and line.count('`') >= 4:
            parts = line.split('`'); decl[parts[1]] = parts[3]
    res = {}
    for f in lista:
        p = os.path.join(B, *f.split('/'))
        s = h(p)[:16]; res[f] = {'sha16': s, 'bytes': os.path.getsize(p), 'declarado': decl.get(f), 'bate': (decl.get(f) == s) if f in decl else None}
    out['secao9'] = res
    out['nao_batem'] = [k for k, v in res.items() if v['bate'] is False]
json.dump(out, open(f'P0_{tag}.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in out.items() if k != 'secao9'}, ensure_ascii=False, indent=1))
