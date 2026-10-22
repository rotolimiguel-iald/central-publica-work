# -*- coding: utf-8 -*-
"""R3: gera a PROPOSTA de registro no mapa (registro_mapa_F1.MOTOR_R3.json). Nao registra no mapa.
Caminhos montados com barra normal e convertidos para o separador do Windows so na saida."""
import json, os, subprocess, sys

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace(chr(92), "/")
REL = ["fonte/TGLExt/IALD.lean", "olean/IALD.olean", "TIPOS_R2_VS_R3.json", "DIFF_R2_R3.diff", "RECIBOS_R3.json",
       "RESULTADO_R3.md", "medidas/DIFF_SO_COMENTARIOS.json", "medidas/ENSAIO_R2_VS_R3.json",
       "medidas/DIGITAL_KERNEL_ANTES.json", "medidas/DIGITAL_KERNEL_DEPOIS.json", "medidas/SANDBOX_MONTAGEM.json",
       "logs/r2_iald_RECIBO.json", "logs/r3_iald_RECIBO.json", "logs/r3_iald_SAIDA.txt", "logs/meta_r2_RECIBO.json",
       "logs/meta_r3_RECIBO.json", "logs/printax_r3_RECIBO.json", "logs/printax_r3_SAIDA.txt",
       "logs/c1_palavra_RECIBO.json", "logs/c2_adendo1_RECIBO.json", "logs/c3_unitrank_r3_RECIBO.json",
       "logs/c4_tempo_r2_RECIBO.json", "meta/meta_r2.txt.gz", "meta/meta_r3.txt.gz",
       "numerico/ensaio_motor_r3.py", "numerico/RESULTADO_NUMERICO_R3.json",
       "scripts/Meta_TEMPLATE.lean", "scripts/comparar_r2_r3.py", "scripts/PrintAxiomsR3.lean",
       "scripts/diff_so_comentarios.py", "scripts/digital.py", "scripts/montar_sandbox.py", "scripts/rodar_lean.py",
       "scripts/recibos.py", "scripts/gerar_registro_mapa.py"]
arts = [AQUI + "/" + r for r in REL]
falt = [a for a in arts if not os.path.isfile(a)]
if falt:
    print("FALHA VISIVEL: artefato ausente", falt); sys.exit(2)
win = lambda p: p.replace("/", chr(92))
reg = {
    "tipo": "RESULTADO",
    "rota_id": "formal.iald_o_motor_unico",
    "dominio": "FORMAL",
    "titulo": "Pedra TGLExt.IALD r3 (o motor unico, nome provisorio): so docstrings e comentarios corrigidos pela reauditoria c1 a4a8fb5f",
    "pergunta": "A r2 corrigida so no texto (M-1 e as BAIXAS da reauditoria a4a8fb5f, mais a nota do auditor sobre U unitario) mantem 100% dos tipos e termos lidos do kernel?",
    "dados": ["nenhum dado observado; so o kernel v391 do Nos (so leitura) e as candidatas pinadas pela r2"],
    "metodo": ("r2 e r3 compiladas no MESMO sandbox C:/t/mo3 (lean v4.31.0 copiado; LEAN_PATH = copia verificada do "
               ".lake/build do Nos + pacotes, so leitura); leitor de kernel proprio (Meta_TEMPLATE.lean) serializa tipo "
               "e valor de cada constante do modulo em dois modos (sem e com nomes de binder) e o script compara strings "
               "inteiras; diff com comentarios removidos; #print axioms das 69 constantes; ensaio numerico refeito "
               "(cabecalho mudou) com beta de runtime; impressao digital do tgl_kernel antes e depois sem seguir juncoes"),
    "resultado": ("69 constantes (62 publicas, 6 internas, 1 lema de equacao): 69/69 identicas em tipo e termo, "
                  "alfa-invariante e tambem com nomes de binder; docstring mudou em 7 (as editadas); codigo sem "
                  "comentarios identico; 69 #print axioms, 0 fora do trio; fonte r3 d7c1f1d3b03e6095, olean r3 "
                  "5856f7f6ea78dcc6; r2 e candidatas recompiladas iguais bit a bit as da r2; ensaio 112/112 PASSA, igual "
                  "a r2 salvo horario; kernel antes = depois"),
    "veredito": "PEDRA_R3_SO_TEXTO__TIPOS_E_TERMOS_INVARIANTES_69_DE_69__NAO_INSTALADA__GATE_INTOCADO",
    "estatuto": "REAL",
    "status": "EXAMINADA",
    "olhou_dados": False,
    "defeito": ("Nao reauditada por terceiro; os relatorios (C6, Q16/Q17, EU SOU como termo, frase da isometria, premissa "
                "da pergunta 3) seguem sem a correcao ao lado, que e da gerencia; a nota sobre U unitario e comentario, "
                "nao teorema da pedra (a sonda e do auditor); coexistencia com o TGLExt inteiro e fecho de usos nao "
                "remedidos na r3."),
    "nao_refazer": "Nao refazer a comparacao r2 x r3: tipos e termos sao identicos por leitura do kernel; o diff esta so em comentarios e docstrings.",
    "proximo_passo": ("Reauditoria da r3; correcoes ao lado nos relatorios (gerencia); decisoes do operador P2 (Pi_N := post a), "
                      "P3 (U unitario por tipo), P4 (DualScalingData do motor), P6 (nome e entrada na v392)."),
    "onde": win(AQUI + "/fonte/TGLExt/IALD.lean"),
    "artefatos": [win(a) for a in arts],
    "refs": ["formal.iald_o_motor_unico"],
    "nota": "Proposta gerada pelo construtor da rodada 3; nao registrada no mapa (a unidade proibe escrever no mapa).",
}
modelo = json.loads(subprocess.run([sys.executable, "-X", "utf8", "C:/IALD/MAPA_DE_ROTAS/rotas.py", "modelo"],
                                   capture_output=True, text=True, encoding="utf-8").stdout)
extra = set(reg) - set(modelo)
if extra:
    print("FALHA VISIVEL: campos fora do modelo", extra); sys.exit(2)
json.dump(reg, open(AQUI + "/registro_mapa_F1.MOTOR_R3.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(arts), "artefatos existentes; campos", sorted(reg))
