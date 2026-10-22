# ENSAIO SINTETICO (nao e' a cadeia): V falso + copias; prova a logica das superficies (append, MEMORY.md, compactacao) sem o Nos v393.
import sys, os, json, runpy
HERE = os.path.dirname(os.path.abspath(__file__)); POS = os.path.dirname(HERE); PK = os.path.dirname(POS)
sys.path.insert(0, POS); sys.path.insert(0, PK)
import leitura_v393, textos_v393
E = json.load(open(os.path.join(PK, "ESPERADOS_v393.json"), encoding="utf-8"))
V = {'data':'14/10/2026','s16':'0123456789abcdef','teor':'7045/7045','escada_antes':6901,'n_pedras':3,'pedras':[{'modulo':'TGLExt.'+m} for m in ('RuleTruthContract','TheRuleAndTheFigureOfTruth','TheRuleInTheContinuousMotor')],
 'n_flags':144,'n_flags_de':144,'n_decl':144,'n_decl_de':144,'axiom_report_n':25157,'pedras_verdict':'PV','registros_novos':['a','b'],'reg_todos':['a'],'troca_dita':E['troca_dita'],
 'verbatins':{k:{'sha16':v['sha256'][:16],'bytes':v['bytes']} for k,v in E['cunhagens'].items()},
 'cons':{'verdict':'CV','pontos':241,'verificacoes':78,'tol':1e-10,'replica_hash_igual':True,'dimfix':8},'cora':{'verdict':'CO','prev':False,'G':False,'espectral_hoje':'AUSENTE'},'kh':{'decl':25161,'thm':19901,'fora':0},'cunh_verdict':'CU',
 'base16':'b590c0aa80055e2a','n_patches':2,'patches':'p1, p2','instalado_em':'x','compl':'COMPLETA','horarios':['a'],'rc':'0','selo_ts':'t','conf16':'c','conf_dm':'1/1','conf_np':'2/2','n_ver_mudaram':0,
 'pilar':{'mode':'REUSE','result16':'r'},'servidor':'s','h_um_absoluto.json':'h1','h_um_absoluto_selo.json':'h2','h_um_absoluto_forma_canonica.md':'h3','h_um_absoluto_manifest.md':'h4','artigos':{'a.pdf':'x'},'umb':35605380}
leitura_v393.ler = lambda: (V, [])
textos_v393._kernel_tem = lambda nomes: None
sys.argv = [os.path.join(POS, "superficies_v393.py"), "--copias", os.path.join(HERE, "copias")]
runpy.run_path(sys.argv[0], run_name="__main__")
