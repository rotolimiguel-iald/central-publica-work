# -*- coding: utf-8 -*-
"""_r1_parteB_delta_v410.py -- R1 (D92), PARTE B, o delta com as pedras R3: a ratificacao D87 confere contra o sha256 da pedra que o operador ratificou (guardado no recibo dos nomes como sha256_ratificada_D87; a R3 tem outro sha256);
os 13 NOMES NOVOS e os 3 campos novos da estrutura, LIDOS do recibo dos nomes ([DECLARADO pela gerencia e pela autoria], a ratificar pelo operador); a PONTE com os pesos (o brilho do leitor do fundo e' e^(-s k): 1/2 por oitava de tempo pago; em n oitavas, 2^(-n k)), calculada por Fraction.
Backup de BYTES; temporario -> substituir; ast.parse; import de conferencia."""
import ast, hashlib, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); P = os.path.join(HERE, "delta_v410.py")
b0 = open(P, "rb").read(); t = b0.decode("utf-8"); assert b"\r\n" not in b0


def tr(a, b, n=1):
    global t
    c = t.count(a); assert c == n, (c, n, a[:140]); t = t.replace(a, b)


tr('_RAT87["pedra_sha256_depois"] == _REC_AESC["sha256"]', '_RAT87["pedra_sha256_depois"] == _REC_AESC.get("sha256_ratificada_D87", _REC_AESC["sha256"])')
i = t.index('NOMES_AESCALA = list(_REC_AESC["nomes"])'); j = t.index("\n", i) + 1
t = t[:j] + ('# (R1, D92: a pedra R3, a ESCALA NO TIPO) os nomes NOVOS e os campos novos da estrutura LeitorDoFundo, LIDOS do recibo dos nomes: [DECLARADO pela gerencia e pela autoria], a ratificar pelo operador; os 44 ratificados (D87) ficam\n'
             'NOMES_NOVOS_AESCALA = list(_REC_AESC.get("nomes_novos_a_ratificar") or [])\n'
             'CAMPOS_NOVOS_AESCALA = list(_REC_AESC.get("campos_novos_da_estrutura") or [])\n'
             'ESTATUTO_NOMES_NOVOS_AESCALA = "[DECLARADO pela gerencia e pela autoria; a ratificar pelo operador]"\n'
             'assert len(NOMES_NOVOS_AESCALA) == 13 and len(CAMPOS_NOVOS_AESCALA) == 3 and not (set(NOMES_NOVOS_AESCALA) & set(NOMES_AESCALA)), "os nomes novos da R3 nao sao os 13 do recibo (ou repetem um ratificado)"\n'
             'ANCORAS_NOVAS_AESCALA = [NS_AESCALA + n_ for n_ in NOMES_NOVOS_AESCALA if (NS_AESCALA + n_) in ANCORAS_AESCALA]   # (as que tem #print axioms na fonte; as duas definicoes derivadas, leitura e limite, sao auditadas pelos teoremas que as usam)\n'
             'RATIFICACAO_PENDENTE_AESCALA = {"nomes_novos": list(NOMES_NOVOS_AESCALA), "campos_novos_da_estrutura": list(CAMPOS_NOVOS_AESCALA), "estatuto": ESTATUTO_NOMES_NOVOS_AESCALA, "decisao": "D92", "nota": "se o operador ratificar depois, isso se registra no HANDOFF; a pedra nao e\' reeditada"}\n') + t[j:]
i = t.index("assert NUMEROS_AESCALA == {"); j = t.index("\n", i) + 1
t = t[:j] + ('# (R1, D92) a PONTE com os pesos, por Fraction: o brilho do leitor do fundo e\' e^(-s k) (k o custo do pixel, s o tempo pago); em uma oitava (s = ln 2) um pixel de custo 1 brilha 1/2; em n oitavas um pixel de custo k brilha 2^(-n k); em n oitavas o fundo de n bits pesa um pixel (1/2^n)\n'
             'PONTE_OITAVAS = ((1, 1), (1, 3), (2, 2), (3, 4))   # (k, n): o custo do pixel e o numero de oitavas de tempo pago\n'
             'PONTE_AESCALA = {"brilho_de_um_pixel_em_uma_oitava": str(_MEIO), "casos": [[k_, n_, str(_MEIO ** (n_ * k_))] for k_, n_ in PONTE_OITAVAS], "em_n_oitavas_o_fundo_pesa_um_pixel": [[n_, str(_MEIO ** n_)] for n_ in (1, 3, 8)]}\n'
             'assert PONTE_AESCALA["brilho_de_um_pixel_em_uma_oitava"] == "1/2" and PONTE_AESCALA["casos"] == [[1, 1, "1/2"], [1, 3, "1/8"], [2, 2, "1/16"], [3, 4, "1/4096"]] and PONTE_AESCALA["em_n_oitavas_o_fundo_pesa_um_pixel"] == [[1, "1/2"], [3, "1/8"], [8, "1/256"]]\n') + t[j:]
nb = t.encode("utf-8"); ast.parse(nb)
open(P + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_pre_r1_parteB", "wb").write(b0)
open(P + ".tmp", "wb").write(nb); assert os.path.getsize(P + ".tmp") == len(nb) > len(b0); os.replace(P + ".tmp", P)
print("delta_v410.py", len(b0), "->", len(nb), "| sha16", hashlib.sha256(b0).hexdigest()[:16], "->", hashlib.sha256(nb).hexdigest()[:16])
sys.path.insert(0, HERE)
import delta_v410 as DL
print("import ok | ancoras AEscala", len(DL.ANCORAS_AESCALA), DL.N_ANCORAS_AESCALA, "| novas com ancora", len(DL.ANCORAS_NOVAS_AESCALA), "| nomes", len(DL.NOMES_AESCALA), "+", len(DL.NOMES_NOVOS_AESCALA), "| ponte", DL.PONTE_AESCALA["casos"])
