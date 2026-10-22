# Involução do fator polar no H_I original — DEV

2026-09-12T13:35:19-03:00. [REAL — quatro módulos/19 alvos compilados; revisão independente e integração pendentes]

O pacote precedente integrou nove módulos/41 alvos e construiu U antiunitário,
S=UB e D(B)=D(S). Este pacote separado prova U²=I usando esse mesmo S, B e U.

1. As involuções de S e S†, com a equação do resolvente, dão SR=(I−R)S em D(S).
2. R preserva o gráfico de B. S=UB e a densidade de Ran B dão UR=(I−R)U em H_I.
3. A conjugação U T U⁻¹ é linear complexa e preserva positividade, pelo produto
   interno antiunitário já provado em GenericAntilinearAdjoint. Não se usa U=U⁻¹.
   CFC.sqrt_unique dá a conjugação das raízes positivas limitadas.
4. Escrevendo P₀=√R e Q=√(I−R), obtêm-se UP₀=QU e UQ=P₀U.
5. B(P₀v)=Qv e S=UB dão S(P₀v)=UQv. A segunda troca permite aplicar S novamente;
   S²=I e a primeira troca dão U²P₀v=P₀v. Ran P₀ é denso, logo U²=I em todo H_I.

Os 19 alvos usam somente propext, Classical.choice e Quot.sound. Os tipos finais
recebem P e vetores, não a involução polar como hipótese. O núcleo GNS, espaço,
produto interno, raiz positiva e fator U são os objetos construídos anteriormente.
Os logs rc1 permanecem no manifesto, sem servir de evidência: timeout de reescrita,
simplificação da parte real, extensionalidade excessiva até igualdade quase em toda
parte e limites de busca de instâncias. A fonte final e seus parâmetros efetivos
estão pinados. A tentativa alternativa de instâncias locais no probe foi
descartada e não é importada. A definição genérica hilbertPositiveSqrt fixa
as instâncias canônicas antes de especializar H; nenhuma mudança de orçamento de elaboração é tratada como axioma.

[OPEN] Isto não identifica a álgebra/peso com seu domínio máximo nem prova KMS,
fluxo modular, traço/escala dual, canto Three Locks, H1/H2/H3 físicos compatíveis,
setor quântico interagente, certificado completo ou runtime integral. U pode ser
usado como conjugação da decomposição polar deste S; sua identificação com os
outros candidatos chamados J exige uma ponte explícita. Não se promove gate.

O relato anterior de dois/quatro alvos permanece histórico. Seu caminho até U²=I
foi aqui percorrido em DEV. Os nove/41 integrados e seus relatórios continuam no
estado selado; estes quatro/19 ainda não entraram no embutido nem no Audit integrado.
Mãe integrada `4a09ad7b616ca8c762e4fe8882585bb015e4708749aa6ede5acb5979ed2df67b`; cópia
`60a9ae7af3f4b54e5dd0018706903c01831260bebb8981c98ad61fa35488a11b`. Original não executado/importado/modificado.
