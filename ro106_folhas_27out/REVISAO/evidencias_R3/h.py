import hashlib
W=r"C:\IALD\Central de Patentes\work\ro106_folhas_27out"
exp={"FOLHAS_SUBSTITUTIVAS_050576.pdf":"884d978a39b20d1a","FOLHAS_SUBSTITUTIVAS_050576_VARIANTE_PHOT.pdf":"4417390dcbd5b998","ALTERNATIVA_FOLHA_1_050576_PHOT.pdf":"c60f4e9ca17c0e22","CARTA_REGRA_26_4_050576.md":"dbe1caff15ed32e4","CARTA_REGRA_26_4_050576.pdf":"a72a89c3571cb828","CARTA_REGRA_26_4_050576_PHOT.md":"cff588eaff8c0a3e","CARTA_REGRA_26_4_050576_PHOT.pdf":"453663db5c4c0ff8","CONFERENCIA_050576.json":"d171e2bc9be9668e",
"FOLHAS_SUBSTITUTIVAS_050579.pdf":"4faa43ca81442fc5","CARTA_REGRA_26_4_050579.pdf":"2378f978494f2fdf","CONFERENCIA_050579.json":"529ca8412ad6baa1"}
for k,v in exp.items():
    h=hashlib.sha256(open(W+"\\"+k,"rb").read()).hexdigest()[:16]
    print(k,h,"OK" if h==v else "MISMATCH expected "+v)
