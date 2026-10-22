# -*- coding: utf-8 -*-
"""REGISTRO de uma intervencao de AMBIENTE durante o rito v385 (gerencia, em nome proprio): as 11:47:5x (hora local) a prioridade do processo do trabalhador
do pilar (PID 213604, nascido BelowNormal por desenho do um.py -- «o rito tem a vez na CPU») foi elevada a Normal, por PowerShell, sem tocar no processo
do rito nem no calculo. Motivo medido: entre 11:26 e 11:47 o T1 (d = 32) avancou ~1 injecao a cada 36-60 s com ~21 nucleos ocupados pelo trabalhador em
BelowNormal, enquanto rodavam em paralelo compilacoes Lean dos verificadores (prioridade Normal) e, no desktop, explorer/VS Code; na v384 o T1 inteiro levou
43 min. Logo depois (11:48-11:51) o T1 fechou as 200 de d = 32, as 20 de d = 64 e as 2.000 de d = 8, e o T4 comecou aos ~4.100 s (na v384, aos 4.904 s).
NAO se afirma qual das duas causas (o fim da carga paralela / a prioridade) explica a retomada: as duas mudaram quase juntas. O que a intervencao NAO muda:
nenhum numero do calculo (escalonamento so); o pre-registro V1 nao fixa prioridade. Fica DITO, para a reprodutibilidade ser lida com isso ao lado."""
import json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
rec = {"quando_local": "2026-10-05 11:47:5x", "o_que": "prioridade do processo do trabalhador do pilar (PID 213604) BelowNormal -> Normal (PowerShell: (Get-Process -Id 213604).PriorityClass = 'Normal')",
       "por_que": "ritmo medido: 11:26 done 1195 (2677 s) -> 11:37 done 1207 (3594 s) -> 11:44-11:47 5 injecoes em 180 s (36 s/injecao, 17 nucleos); na v384 o T1 inteiro (3220 injecoes) levou 2585 s",
       "carga_paralela_medida": "verificadores da gerencia compilando Lean (lake env lean; ate 3 processos lean) entre ~11:20 e ~11:47; ensaios da cadeia em copias (11:24-11:40); explorer ~1,5 nucleo; VS Code",
       "o_que_aconteceu_depois": "11:48-11:51: o T1 fechou (d=32: 200, d=64: 20, d=8: 2000); T4 iniciado aos ~4100 s de trabalhador (v384: 4904 s); threads do trabalhador 205 -> 157",
       "causa": "NAO DISCRIMINADA: o fim da carga paralela e a prioridade mudaram quase juntos; o que se sabe: trabalhador em BelowNormal com ~21 threads OpenMP/MAGMA sob carga Normal concorrente = patologia conhecida de barreiras OpenMP",
       "o_que_nao_muda": "nenhum numero do calculo (escalonamento apenas); o V1 nao fixa prioridade; o trabalhador e a especificacao seguem os congelados",
       "estatuto": "[REAL — intervencao de ambiente, dita]; a leitura da causa e' [CONJECTURE]",
       "quem": "gerencia (sessao 6da8f00d), em nome proprio"}
p = os.path.join(HERE, "INTERVENCAO_PRIORIDADE_v385.json")
with open(p + ".tmp", "w", encoding="utf-8") as f:
    json.dump(rec, f, ensure_ascii=False, indent=1)
os.replace(p + ".tmp", p)
print("OK", p)
