import json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "C:/IALD/MAPA_DE_ROTAS"); import rotas
HERE = os.path.dirname(os.path.abspath(__file__))
E1 = json.load(open(os.path.join(HERE, "estresse_eig.json"), encoding="utf-8"))
regs = rotas._le()
if any(r.get("rota_id") == "infra.gpu_cusolver_geev_queda_n64" for r in regs):
    print("ja registrado"); sys.exit(0)
quedas = sorted(k for k, v in E1.items() if v["rc"] != 0)
ok = sorted(k for k, v in E1.items() if v["rc"] == 0)
o = rotas.registrar([dict(tipo="ROTA", rota_id="infra.gpu_cusolver_geev_queda_n64", dominio="INFRAESTRUTURA", status="EXAMINADA", estatuto="REAL", olhou_dados=False,
    titulo="o cuSOLVER padrao do PyTorch 2.11 (CUDA 12.8, RTX 5090) DERRUBA o processo (violacao de acesso 0xC0000005) em autovalores nao Hermitianos n = 64; o MAGMA nao",
    pergunta="por que a sonda de tempo do pilar quantico morreu com codigo 139 em torch.linalg.eig?",
    metodo="estresse em subprocessos, so matrizes aleatorias complex128: eig e eigvals x biblioteca (padrao, cusolver, magma) x n (64: 1 500 chamadas; 256: 150; 1024: 8); depois tamanhos grandes",
    resultado="quedas: %s; sem queda: %s" % (quedas, ok),
    defeito="as sondas anteriores sobreviveram por sorte; o T4 (15 000 instancias em d = 8) teria derrubado o rito",
    nao_refazer="nao usar o cuSOLVER (o padrao) para autovalores nao Hermitianos pequenos; nao confiar numa sonda curta para dizer que a biblioteca e' estavel",
    proximo_passo="a escolha por tamanho congelada na especificacao (MAGMA ate um n, cuSOLVER acima); caracterizar em que tamanhos o cuSOLVER cai",
    artefatos=[os.path.join(HERE, "estresse_eig.py"), os.path.join(HERE, "estresse_eig.json")], refs=["infra.gpu_sonda_tempo_v384", "infra.gpu_rtx5090_ambiente_02out"])],
    "claude-code/central-de-patentes (gerência) sessão 6da8f00d")
print({k: o[k] for k in o if k != "registros"})
