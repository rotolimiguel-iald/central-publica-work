# -*- coding: utf-8 -*-
"""ERRATA AO LADO da gravacao da 9a (gerencia, em nome proprio, 04/10/2026): o gravar_afericao9_v384.py condicionava a ressalva de O2/O3 a encontrar «V1.json ja
existe com outro conteudo» na saida do teste dos orfaos, mas a saida guardada estava TRUNCADA em 200 caracteres («... V1.json ja existe com»); a condicao deu
falso e a ressalva NAO entrou na disposicao 9N0 nem no texto do pre-registro. O fato, lido aqui do teste_orfaos_v384.json: O2 e O3 foram recusados pela
guarda do V1 ja existente (o campo gerado muda a cada segundo), nao pela guarda nova das evidencias, que so se alcanca com o V1 IGUAL (relogio fixo). A
correcao vai AO LADO: no AFERIDOR (linha acrescentada), nas disposicoes (disposicoes_9a_novos_errata) e no fim do texto do pre-registro. Backup de BYTES."""
import hashlib, json, os, time
HERE = os.path.dirname(os.path.abspath(__file__))
TO = json.load(open(os.path.join(HERE, "teste_orfaos_v384.json"), encoding="utf-8"))
_o = [TO[k]["saida"] for k in ("O2_json_presente_pasta_adulterada", "O3_json_presente_arquivo_a_mais")]
assert all(("PREREGISTRO_PILAR_QUANTICO_20261003_V1.json ja existe com" in x) for x in _o), _o   # o fato, lido da saida (mesmo truncada)


def gravar(p, novo, conferir_prefixo=None):
    raw = open(p, "rb").read()
    bak = p + ".bak_" + time.strftime("%Y%m%d_%H%M%S"); open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
    open(p + ".tmp", "wb").write(novo); assert os.path.getsize(p + ".tmp") == len(novo); os.replace(p + ".tmp", p); assert open(p, "rb").read() == novo
    if conferir_prefixo is not None:
        assert novo[:len(conferir_prefixo)] == conferir_prefixo


TXT = ("ERRATA AO LADO (gerencia, 04/10): a disposicao 9N0 e o texto da 9a omitiram uma ressalva que deviam ter -- O2 e O3 do teste dos orfaos foram recusados "
       "pela guarda do V1 JA EXISTENTE (o campo gerado muda a cada segundo), nao pela guarda nova das evidencias, que so se alcanca com o V1 IGUAL (relogio "
       "fixo, como a 9a afericao mediu); a condicao do gravador leu a saida truncada em 200 caracteres. Script desta errata: errata_gravacao_afericao9_v384.py.")
p = os.path.join(HERE, "AFERIDOR_v384.txt"); raw = open(p, "rb").read()
assert b"9a PASSADA -- as correcoes da 8a" in raw and b"errata_gravacao_afericao9_v384.py" not in raw
gravar(p, raw + ("\n" + TXT + "\n").encode("utf-8"), conferir_prefixo=raw)
dp = os.path.join(HERE, "disposicoes_afericoes_v384.json"); D = json.load(open(dp, encoding="utf-8"))
assert "disposicoes_9a_novos_errata" not in D
D["disposicoes_9a_novos_errata"] = {"0": TXT, "script": "errata_gravacao_afericao9_v384.py", "sha256_do_script": hashlib.sha256(open(os.path.abspath(__file__), "rb").read()).hexdigest()}
t = D["texto_para_o_pre_registro"]; assert t.endswith("(«9 pela contagem corrigida na 7ª»)")
D["texto_para_o_pre_registro"] = t + ("; ERRATA AO LADO da 9ª: dois dos três casos dos órfãos (O2, O3) foram recusados pela guarda do V1 já existente, não pela "
                                       "guarda nova das evidências, que só se alcança com o V1 igual (relógio fixo)")
b = json.dumps(D, ensure_ascii=False, indent=1).encode("utf-8"); gravar(dp, b)
print("ok | disposicoes", hashlib.sha256(b).hexdigest()[:16])
