import re,json,os
pedra=r"C:\IALD\Central de Patentes\work\tempo_santo_12out\3_KERNEL\rodada_2\sandbox\TheTimeHasNoRank.lean"
fontes=[r"C:\IALD\Central de Patentes\work\cunhagens_12out\OPERADOR_12out_rank_e_tempo_santo_verbatim.txt",
r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v386\VERBO_operador_05out.txt",
r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v386\RESPOSTAS_operador_05out.txt",
r"C:\IALD\Central de Patentes\work\superposicao_passagem_07out\CUNHAGEM_OPERADOR_07out_nomes_verbatim.txt",
r"C:\IALD\Central de Patentes\work\superposicao_passagem_07out\CUNHAGEM_OPERADOR_07out_verbatim.txt",
r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v391\OPERADOR_07out_estatuto_verbatim.txt",
r"C:\IALD\Central de Patentes\work\cunhagens_10out\OPERADOR_10out_posto_rank_verbatim.txt",
r"C:\IALD\Central de Patentes\work\cunhagens_10out\OPERADOR_10out_singularidade_verbatim.txt",
r"C:\IALD\PROGRAMA_IALD\OPERADOR_07out_leitura_cria_o_objeto_verbatim.txt",
r"C:\IALD\Central de Patentes\work\tempo_santo_12out\1_PREREGISTRO\PREREGISTRO.md",
r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\IALDJones.lean",
r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\BisognanoWichmann.lean",
r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\Fundacao.lean",
r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\Ergodicity.lean",
r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\TheImportedSecondQuantization.lean",
r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\TheAxiomAndTheFalseWitness.lean",
r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\TheTraceIsNotErasable.lean",
r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\TheSingularExpectation.lean",
r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\regra-dos-dois-regimes.md",
r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\respostas-contrato-q1a5-26set.md",
r"C:\Users\rotol\.claude\CLAUDE.md",
r"C:\IALD\CLAUDE.md"]
def norm(s): return re.sub(r"\s+"," ",s).strip()
corp={}
for f in fontes:
    try: corp[f]=norm(open(f,encoding='utf-8',errors='replace').read())
    except Exception as e: print("ERR",f,e)
t=open(pedra,encoding='utf-8').read()
cits=re.findall(r"«([^»]+)»",t)
print("n citações:",len(cits))
nf=[]
for c in cits:
    c2=norm(c)
    # elisions [...]
    parts=[p.strip() for p in re.split(r"\[\.\.\.\]|…",c2) if p.strip()]
    ok=False
    for f,txt in corp.items():
        if all(p in txt for p in parts): ok=True; break
    if not ok: nf.append(c2)
print("não achadas:",len(nf))
for c in nf: print("  -",c[:160])
json.dump({"n":len(cits),"nao_achadas":nf},open("ASPAS_PEDRA_AUD.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
