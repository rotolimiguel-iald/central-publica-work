# -*- coding: utf-8 -*-
"""_fork_b_varredura_v411.py -- (claude-construtor-v411, retomada, fork B, 12/11/2026) adapta varredura_fock_omega_v411.py a v411: os textos do ensaio vem do dry da rodada (DL.DRY_DIR, fora de work; no ensaio do topo
proposto, a pasta de ensaio); o relatorio, o plano e a saida em DL.SAIDA; as fontes autorais da v411 (delta, registros, registros_h0dn, runtime_h0dn, quadro, gerador, guarda das frases); o recorte do texto NOVO
nos artigos rendidos e' o que nao existe no artigo rendido da v410 (dry_v410, depois de desfazer so' a mudanca do A2 no conversor para TXT), em vez da faixa de datas; «v411» deixa de contar como passagem
futura (v412 em diante). Nada roda. uso: python -B -X utf8 _fork_b_varredura_v411.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _fork_b_lib_v411 as L  # noqa: E402

V = "varredura_fock_omega_v411.py"
_nh = L.linha(V, "# [ADAPTADO v410, 06/11/2026, claude-construtor-v410]")
L.aplicar(V, [
    ("HERE = os.path.dirname(os.path.abspath(__file__))\n",
     'HERE = os.path.dirname(os.path.abspath(__file__))\n'
     'import importlib.util as _ilu\n'
     '_sp_dl = _ilu.spec_from_file_location("delta_v411_varredura", os.path.join(HERE, "delta_v411.py")); DL = _ilu.module_from_spec(_sp_dl); _sp_dl.loader.exec_module(DL)   # (v411) o dry e a saida da rodada vem do delta\n'),
    ('ARQ = [os.path.join(HERE, "dry_v411", n_) for n_ in ("core_ensaio.json", "selo_ensaio.json", "um_absoluto_forma_canonica.md", "dry_v411_pt.txt", "dry_v411_en.txt")]',
     'ARQ = [os.path.join(DL.DRY_DIR, n_) for n_ in ("core_ensaio.json", "selo_ensaio.json", "um_absoluto_forma_canonica.md", "dry_v411_pt.txt", "dry_v411_en.txt")]   # (v411) o dry da rodada, fora de work (D135)'),
    ('ARQ += [os.path.join(HERE, "pos_rito", "CUSTODIA_v411_RASCUNHO.txt"), os.path.join(HERE, "RELATORIO_PREPARACAO_v411.md"), os.path.join(HERE, "PLANO_v411.md"), os.path.join(HERE, "DEPOSITO_CONSTRUTOR_v411.md")]\n'
     'ARQ += [os.path.join(HERE, n_) for n_ in ("delta_v411.py", "registros_v411.py", "runtime_v411.py", "artigo_pt_v411.pysnip", "artigo_en_v411.pysnip", "gerar_candidato_v411.py", "gerar_relatorio_v411.py", "depositar_construtor_v411.py",\n'
     '                                          "fechar_preparacao_v411.py", "acom_inscrever_prep_v411.py", "guarda_frases_v411.py")]',
     'ARQ += [os.path.join(HERE, "pos_rito", "CUSTODIA_v411_RASCUNHO.txt"), DL.saida("RELATORIO_PREPARACAO_v411.md"), DL.saida("PLANO_v411.md"), os.path.join(HERE, "DEPOSITO_CONSTRUTOR_v411.md")]\n'
     'ARQ += [os.path.join(HERE, n_) for n_ in ("delta_v411.py", "registros_v411.py", "registros_h0dn_v411.py", "runtime_h0dn_v411.py", "quadro_v411.py", "gerar_candidato_v411.py", "gerar_relatorio_v411.py", "depositar_construtor_v411.py",\n'
     '                                          "fechar_preparacao_v411.py", "acom_inscrever_prep_v411.py", "guarda_frases_v411.py")]   # (v411: as fontes autorais; nao ha runtime_v411 nem artigo_*_v411.pysnip)'),
    ('|\\bv41[1-9]\\b|\\bopen\\b|\\bpending\\b|not\\s+yet", re.I)   # (v411: a versao corrente, v411, nao conta como passagem futura)',
     '|\\bv41[2-9]\\b|\\bopen\\b|\\bpending\\b|not\\s+yet", re.I)   # (v411: a versao corrente, v411, nao conta como passagem futura; v412 em diante conta)'),
    ('CHAVES_V411 = ("traducao_turing_v409", "cunhagens_v409", "kh_n1_cobertura_v409")',
     'CHAVES_V411 = ("iald2_v410", "a_escala_v410", "h0dn_bg1_v410", "h0dn_fontes_hms13_v410", "cunhagens_v410", "kh_n1_cobertura_v410")   # (v411) os registros da v410, herdados e selados (registro)'),
    ('''        i0_ = next((i_ for i_ in idx_ if "06/11/2026" in linhas_[i_]), None)   # (a secao da v411 comeca na data dela e vai ate a da v410)
        i1_ = next((i_ for i_ in idx_ if i0_ is not None and i_ > i0_ and "05/11/2026" in linhas_[i_]), len(linhas_))
        idx_ = list(range(max(0, i0_ - 3), i1_)) if i0_ is not None else []''',
     '''        # (v411) o texto NOVO do artigo e' o que nao existe no artigo rendido da v410 (dry_v410), depois de desfazer SO' a mudanca do A2 no conversor para TXT (^(X) -> ^X):
        # o topo novo (o quadro, o resumo, as trocas, a frase do estatuto) e a secao da v411 entram; o texto herdado da v410 fica fora (a faixa de datas da v410 nao cobria o topo)
        _lg_ = "en" if b_.endswith("_en.txt") else "pt"
        _base_txt_ = os.path.join(os.path.dirname(HERE), "v410", "dry_v410", "dry_v410_%s.txt" % _lg_)
        _velhas_ = set(open(_base_txt_, encoding="utf-8", errors="replace").read().split(chr(10))) if os.path.isfile(_base_txt_) else set()
        idx_ = [i_ for i_ in idx_ if re.sub(r"\\^\\(([^()]{2,})\\)", r"^\\1", linhas_[i_]) not in _velhas_] if _velhas_ else idx_'''),
    ('open(os.path.join(HERE, "VARREDURA_FOCK_OMEGA_v411.json"), "w", encoding="utf-8").write(json.dumps(R, ensure_ascii=False, indent=1))',
     'R.update(DL.MARCA_ENSAIO)\n_out_ = DL.saida("VARREDURA_FOCK_OMEGA_v411.json"); open(_out_ + ".tmp", "w", encoding="utf-8").write(json.dumps(R, ensure_ascii=False, indent=1)); os.replace(_out_ + ".tmp", _out_)'),
    (_nh, "# [ADAPTADO v410, 06/11/2026, claude-construtor-v410] (historico) a varredura da v409 reaproveitada na v410; a D64 segue proibindo o par na face de Fock dito em aberto"),
], "a varredura da v410 reaproveitada: os textos do ensaio do dry da rodada (DL.DRY_DIR, fora de work), o relatorio e o plano e a saida em DL.SAIDA; as fontes autorais da v411; o texto NOVO do artigo e' o que nao existe no artigo rendido da v410 (o A2 desfeito); v412 em diante conta como passagem futura")
