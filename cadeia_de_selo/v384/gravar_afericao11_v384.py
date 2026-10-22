# -*- coding: utf-8 -*-
"""Registro da 11a verificacao (estreita, do v11 -> v12; um verificador independente; resultado da maquina em aferidor11/resultado_aferidor11.json). AO LADO:
(1) disposicoes 10a_novos[4] e 10a_itens[9N14]: «toda recusa 17 dos giros acontece com o log real ainda no lugar» vale para a dos sinais e a do log real; a da
troca do .fase0 pelo log real vem depois, sem perda; (2) disposicao 10a_novos[3]: os rascunhos v12 NAO entraram em passada10 -- e nem devem entrar num arquivo
que o rascunho cita por hash (seria circular); o registro dos rascunhos apresentados mora em registro_rascunhos_apresentados_v384.json, que o rascunho nao cita.
Backup de BYTES; temporario -> tamanho -> substituir -> conferir."""
import hashlib, json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
R11 = os.path.join(HERE, "aferidor11", "resultado_aferidor11.json"); J11 = json.load(open(R11, encoding="utf-8"))


def gravar(p, novo, conferir_prefixo=None):
    raw = open(p, "rb").read()
    bak = p + ".bak_" + time.strftime("%Y%m%d_%H%M%S"); open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
    open(p + ".tmp", "wb").write(novo); assert os.path.getsize(p + ".tmp") == len(novo); os.replace(p + ".tmp", p); assert open(p, "rb").read() == novo
    if conferir_prefixo is not None:
        assert novo[:len(conferir_prefixo)] == conferir_prefixo


DEF = [
    {"n": 1, "severidade": "BAIXO", "toca_rascunho": True, "achado": "«recusada depois da fase 0» contradiz a lista «10 a 15» (as recusas 13, 14 e 15 sao da propria fase 0)",
     "disposicao": "trocado por «a partir da fase 0» (aplicar_afer11_gerador_lancador.py)."},
    {"n": 2, "severidade": "BAIXO", "toca_rascunho": True, "achado": "a 17 da troca do .fase0 pelo log real (rito :209) fica fora da qualificacao «antes de o log real sair do lugar»; e «so depois da ultima recusa» nao vale a letra para ela",
     "disposicao": "o rascunho diz que essa 17 vem depois, sem perda, e «so depois da ultima recusa DAS GUARDAS ... (nessa ordem)»; o comentario do lancador e as disposicoes 10a_novos[4] e 10a_itens[9N14] corrigidos AO LADO."},
    {"n": 3, "severidade": "BAIXO", "toca_rascunho": False, "achado": "a disposicao 10a_novos[3] diz que os rascunhos v12 entram em passada10, mas ha 0 ocorrencias; e grava-los num arquivo que o rascunho cita por hash seria circular",
     "disposicao": "AO LADO: o registro dos rascunhos apresentados mora em registro_rascunhos_apresentados_v384.json, que o rascunho NAO cita por hash."},
    {"n": 4, "severidade": "BAIXO", "toca_rascunho": True, "achado": "o afericao10_resultado.json nao estava entre as evidencias do rascunho",
     "disposicao": "entra como evidencia obrigatoria (a 9 e a 10 obrigatorias; EV_OPC vazio)."},
]
TXT = ["\n" + "=" * 80, "11a VERIFICACAO (estreita, do v11 -> v12; verificador independente) -- %s; resultado da maquina: aferidor11/resultado_aferidor11.json, sha256 %s" % (time.strftime("%d/%m/%Y %H:%M"), h(R11)), "=" * 80,
       "VEREDITO DO VERIFICADOR: tudo o que foi alterado confere (numeros e hashes); 2 imprecisoes de redacao (BAIXO) no texto do lancador, que tocam o rascunho; 2 de registro; nenhum ALTO ou MEDIO.",
       "CAMPOS ALTERADOS v11 -> v12 (lidos pelo verificador): " + json.dumps(J11.get("json_campos_alterados_v11_v12"), ensure_ascii=False)]
for d in DEF:
    TXT.append("\n[11.%d] (%s; toca o rascunho: %s) %s\nDISPOSICAO DA GERENCIA: %s" % (d["n"], d["severidade"], d["toca_rascunho"], d["achado"], d["disposicao"]))
TXT.append("\nEVIDENCIAS (sha256): aplicar_afer11_gerador_lancador.py %s; gravar_afericao11_v384.py %s" % (h(os.path.join(HERE, "aplicar_afer11_gerador_lancador.py"))[:16], h(os.path.abspath(__file__))[:16]))
p = os.path.join(HERE, "AFERIDOR_v384.txt"); raw = open(p, "rb").read(); assert b"11a VERIFICACAO" not in raw
gravar(p, raw + ("\n".join(TXT) + "\n").encode("utf-8"), conferir_prefixo=raw)
dp = os.path.join(HERE, "disposicoes_afericoes_v384.json"); D = json.load(open(dp, encoding="utf-8")); assert "passada11" not in D
ERR = "[ERRATA AO LADO, 11a: «toda recusa 17» vale para a dos sinais e a do log real; a da troca do .fase0 pelo log real vem DEPOIS de o log real girar, sem perda -- o registro dela fica no .fase0]"
D["disposicoes_10a_novos_errata"] = {"4": ERR, "3": "[ERRATA AO LADO, 11a: os rascunhos v12 NAO entraram em passada10 -- e nao devem entrar num arquivo que o rascunho cita por hash (circular); o registro dos rascunhos apresentados mora em registro_rascunhos_apresentados_v384.json]"}
D["disposicoes_10a_itens_errata"] = {"9N14": ERR}
t = D["texto_para_o_pre_registro"]; assert "; 11ª verificação" not in t
D["texto_para_o_pre_registro"] = t + ("; 11ª verificação (estreita, um verificador independente sobre as frases que mudaram do rascunho v11 ao v12): tudo o que mudou confere "
                                      "(números e hashes); duas imprecisões de redação no texto do lançador e duas de registro, todas de severidade baixa, tratadas antes deste documento")
D["passada11"] = {"arquivo": "aferidor11/resultado_aferidor11.json", "sha256": h(R11), "defeitos": DEF, "tipo": "verificacao estreita do v11 -> v12"}
b = json.dumps(D, ensure_ascii=False, indent=1).encode("utf-8"); gravar(dp, b)
print("disposicoes:", hashlib.sha256(b).hexdigest()[:16])
