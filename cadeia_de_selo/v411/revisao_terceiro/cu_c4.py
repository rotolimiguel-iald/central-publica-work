"""CU-C4: B-02 com frases minhas: a F67 dispara com o Z em notacao de formula (cifrao), PT e EN; sem os quatro: recusa; com os quatro: passa."""
import sys
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411"
sys.dont_write_bytecode = True
sys.path.insert(0, V)
import guarda_frases_v411 as G

casos = [
    # (rotulo, frase, deve_recusar)
    ("pt_cifrao_sem_os_quatro", r"\textbf{Teste.} O $Z$ contra o nulo vale $=7{,}01$ no H0DN.", True),
    ("pt_cifrao_sem_os_quatro_b", r"O $Z$ contra o nulo $=7{,}01$ em H0DN.", True),
    ("pt_puro_sem_os_quatro", "O Z contra o nulo = 7,01 em H0DN.", True),
    ("en_cifrao_sem_os_quatro", r"\textbf{Test.} The $Z$ against the null is $=7.01$ in H0DN.", True),
    ("en_cifrao_sem_os_quatro_b", r"The $Z$ against the null $=7.01$ in H0DN.", True),
    ("en_puro_sem_os_quatro", "The Z against the null = 7.01 in H0DN.", True),
    ("pt_cifrao_com_os_quatro", r"\textbf{Teste.} Sob o modelo de erros publicado, o $Z$ contra o nulo vale $=7{,}01$ no H0DN; com as Cefeidas livres o dado lê $4{,}38$, abaixo de 5; retrodição sem ajuste; o teste não é cego; provado é validade, não creditação.", False),
    ("en_cifrao_com_os_quatro", r"\textbf{Test.} Under the published error model, the $Z$ against the null is $=7.01$ in H0DN; with free Cepheids the data read $4.38$, below 5; retrodiction without fit; the test is not blind; proved is validity, not creditation.", False),
    ("pt_puro_com_os_quatro", "Sob o modelo de erros publicado, o Z contra o nulo vale 7,01 no H0DN; com as Cefeidas livres o dado lê 4,38, abaixo de 5; retrodição sem ajuste; o teste não é cego; provado é validade, não creditação.", False),
    ("en_puro_com_os_quatro", "Under the published error model, the Z against the null is 7.01 in H0DN; with free Cepheids the data read 4.38, below 5; retrodiction without fit; the test is not blind; proved is validity, not creditation.", False),
    # variantes de cifrao: Z com chaves e com espaco
    ("pt_cifrao_espaco", r"O $Z$  contra o nulo $=7{,}01$ em H0DN.", True),
    ("pt_provado_na_natureza_sem_os_quatro", "O elo foi provado na natureza no teste H0DN.", True),
    ("en_proved_in_nature_sem_os_quatro", "The link was proved in nature in the H0DN test.", True),
    # o que NAO pode recusar: a frase neutra
    ("neutra_pt", "A lei K foi confrontada com a razão de Hubble em outra fase.", False),
    ("neutra_en", "The K law was confronted with the Hubble ratio in another phase.", False),
]
ok = True
for rot, fr, rec in casos:
    v = G.violacoes(fr)
    recusou = bool(v)
    bom = recusou == rec
    ok = ok and bom
    print("%-40s deve_recusar=%-5s recusou=%-5s %s %s" % (rot, rec, recusou, "OK " if bom else "FALHA", [x[0][:24] for x in v][:2]))
print("TUDO COMO ESPERADO:", ok)
