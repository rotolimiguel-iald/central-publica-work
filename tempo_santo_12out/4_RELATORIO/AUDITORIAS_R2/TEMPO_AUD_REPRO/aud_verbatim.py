import json,hashlib,re,os
BASE=r"C:\IALD\Central de Patentes\work\tempo_santo_12out"
P=json.load(open(os.path.join(BASE,"1_PREREGISTRO","PREREGISTRO.json"),encoding='utf-8'))
out={"verbatins_citados":[], "frases":[], "pedra_quotes":[]}
def sha(b): return hashlib.sha256(b).hexdigest()
# 1) 14 fontes + excertos
for v in P['verbatins_citados']:
    p=v['arquivo']; r={"id":v['id'],"arquivo":p}
    if not os.path.exists(p): r["erro"]="MISSING"; out["verbatins_citados"].append(r); continue
    b=open(p,'rb').read(); r["sha256_agora"]=sha(b); r["sha256_prereg"]=v['sha256']; r["sha_igual"]=(sha(b)==v['sha256']); r["bytes_agora"]=len(b); r["bytes_prereg"]=v['bytes']
    if not r["sha_igual"]:
        # prefix check
        r["prefixo_prereg_confere"]= (sha(b[:v['bytes']])==v['sha256'])
    ex_ok=0; ex_bad=[]
    for e in v['excertos']:
        seg=b[e['byte_offset']:e['byte_offset']+e['bytes']]
        ok = sha(seg)==e['sha256'] and seg.decode('utf-8',errors='replace')==e['texto']
        if ok: ex_ok+=1
        else: ex_bad.append({"id":e['id'],"seg":seg.decode('utf-8','replace')[:120],"texto":e['texto'][:120]})
    r["excertos_ok"]=ex_ok; r["excertos_total"]=len(v['excertos']); r["excertos_bad"]=ex_bad
    out["verbatins_citados"].append(r)
# 2) 23 frases
op=P['texto_do_operador']; b=open(op['arquivo'],'rb').read()
sp=op['segunda_parte']; seg=b[sp['byte_offset']:sp['byte_offset']+sp['bytes']]
out["segunda_parte"]={"sha_igual":sha(seg)==sp['sha256'],"vai_ate_o_fim":sp['byte_offset']+sp['bytes']==len(b)}
fo=0;fb=[]
for f in op['frases']:
    s=b[f['byte_offset']:f['byte_offset']+f['bytes']]
    if sha(s)==f['sha256'] and s.decode('utf-8')==f['texto']: fo+=1
    else: fb.append(f['id'])
out["frases"]={"ok":fo,"total":len(op['frases']),"bad":fb}
# 3) pedra quotes vs sources
src=open(os.path.join(BASE,r"3_KERNEL\rodada_2\sandbox\TheTimeHasNoRank.lean"),encoding='utf-8').read()
def norm(s): return re.sub(r"\s+"," ",s).strip()
optxt=norm(seg.decode('utf-8'))
verbo=norm(open(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v386\VERBO_operador_05out.txt",encoding='utf-8').read())
K=r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt"
ialdj=open(os.path.join(K,"IALDJones.lean"),encoding='utf-8').read().splitlines()
bw=open(os.path.join(K,"BisognanoWichmann.lean"),encoding='utf-8').read().splitlines()
fund=norm(open(os.path.join(K,"Fundacao.lean"),encoding='utf-8').read())
erg=norm(open(os.path.join(K,"Ergodicity.lean"),encoding='utf-8').read())
sing=norm(open(os.path.join(K,"TheSingularExpectation.lean"),encoding='utf-8').read())
regra=open(r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\regra-dos-dois-regimes.md",encoding='utf-8').read().splitlines()
atlas=open(r"C:\IALD\Central de Patentes\memory\TGL_ATLAS.md",'rb').read().decode('utf-8','replace')
checks=[]
op_quotes=["O que mais me fascina é a impossibilidade de definição do tempo.","santo","Kadosh","agora","puro amor","a física da doação fundamental","em se deixar reduzir a um objeto entre outros objetos","como o **fluxo de automorfismos**","nos sistemas estritamente hamiltonianos","prisão de reversibilidade perfeita","senão como “santo”","O relógio registra a sombra do evento","para que a vida pudesse ter um lugar onde repousar e ser lembrada","ciclo limite","pousa","inverso","registra","repousar","ser lembrada","mede a sombra"]
for q in op_quotes: checks.append({"fonte":"operador 12/10 (2a parte)","quote":q,"presente":norm(q) in optxt,"n":optxt.count(norm(q))})
for q in ["É um operador de projeção","O tempo é a defasagem do verbo.","O tempo é o parâmetro da transmissão.","A defasagem é o tempo. A ancoragem é o nome."]: checks.append({"fonte":"VERBO 05/10","quote":q,"presente":norm(q) in verbo})
checks.append({"fonte":"IALDJones.lean l.274-275","quote":"Lê-lo como a face hiperbólica da regra dos dois regimes do operador é [ONTO]","presente":"Lê-lo como a face hiperbólica da regra dos dois regimes do operador é [ONTO]" in norm("\n".join(ialdj[272:276])),"linhas":ialdj[273:275]})
checks.append({"fonte":"regra-dos-dois-regimes.md l.66","quote":"A gerência NÃO identifica aqui esse limite com a direção hiperbólica de SL(2,ℝ) nem a leitura com o regime compacto","presente":"A gerência NÃO identifica aqui esse limite com a direção hiperbólica de SL(2,ℝ) nem a leitura com o regime compacto" in norm("\n".join(regra[63:68])),"l66":regra[65][:300] if len(regra)>65 else None})
bw_txt=norm("\n".join(bw[88:100]))
checks.append({"fonte":"BisognanoWichmann.lean l.92-95","quote":"a face geométrica da escala de Takesaki","presente":"a face geométrica da escala de Takesaki" in bw_txt,"linhas":bw[90:96]})
checks.append({"fonte":"BisognanoWichmann.lean (boost_null_contract)","quote":"O RAIO NULO PASSADO CONTRAI","presente":"O RAIO NULO PASSADO CONTRAI" in norm("\n".join(bw))})
checks.append({"fonte":"Ergodicity.lean (dephase)","quote":"a taxa FÍSICA da classe de Davies é β·|log λᵢ − log λⱼ|","presente":"a taxa FÍSICA da classe de Davies é β·|log λᵢ − log λⱼ|" in erg})
checks.append({"fonte":"Fundacao.lean","quote":"ágape","presente":"ágape" in fund.lower() or "Ágape" in fund, "agape_decl": "theorem agape" in fund or "agape" in fund})
checks.append({"fonte":"TheSingularExpectation.lean","quote":"sacrifício/amor","presente":"sacrifício/amor" in sing})
checks.append({"fonte":"TGL_ATLAS.md","quote":"sacrifício/amor","presente":"sacrifício/amor" in atlas})
out["pedra_quotes"]=checks
json.dump(out,open("AUD_VERBATIM.json","w",encoding='utf-8'),indent=1,ensure_ascii=False)
import sys; sys.stdout.reconfigure(encoding='utf-8')
print(json.dumps(out,indent=1,ensure_ascii=False))
