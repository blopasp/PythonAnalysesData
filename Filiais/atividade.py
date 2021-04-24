import pandas as pd
import pyodbc as o
import baseFiliais as bf

#consulta da atividade das filiais (diário)
ativ = """
	SELECT
		KF.KAFI_CD_FILIAL AS Filial,
		KF.KAFI_TP_MOV AS TipoMov,
		CONVERT(DATE,KF.KAFI_DH_OCORRREAL) AS DataOcorrencia,
		CAST(SUM(KF.KAFI_QT_MOV) AS NUMERIC) AS QtdeMovimento,
		CAST(SUM(KF.KAFI_VL_CMPG*KAFI_QT_MOV) AS MONEY) AS  ValorMov,
		CAST(SUM(KF.KAFI_VL_PREVEN*KAFI_QT_MOV) AS MONEY) AS ValorVenda

	FROM KARDEX_FILIAL KF WITH (NOLOCK)
	INNER JOIN PRODUTO_MESTRE PM (NOLOCK)
	ON PM.PRME_CD_PRODUTO = KF.KAFI_CD_PRODUTO
	INNER JOIN CATEGORIA_PRODUTO_NOVO CP
	ON CP.CAPN_CD_CATEGORIA = PM.CAPN_CD_CATEGORIA

	WHERE
		DATEDIFF(DAY, KAFI_DH_OCORRREAL, GETDATE()) = 1 AND
		PM.CAPN_CD_CATEGORIA NOT LIKE '3%'AND
		PM.CAPN_CD_CATEGORIA NOT LIKE '1.101.009%' AND
		PM.CAPN_CD_CATEGORIA NOT LIKE '1.102.009%' AND
		PM.CAPN_CD_CATEGORIA NOT LIKE '2.504.001%'

	GROUP BY
		KAFI_CD_FILIAL,
		KAFI_TP_MOV,
		CONVERT(DATE,KAFI_DH_OCORRREAL)
"""

# funcao para extrair base do servidor
def consulta(query):
	
	server = 'cosmos' 
	database = 'cosmos_v14b' 

	con = o.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database) 
	cursor = con.cursor()
	base = pd.read_sql(query, con)

	return base

# funcao para testar data de atualizacao
def insertDados(string, base):
	a=0
	for i in range(len(base)):
		insert = string.format(aa=base['Filial'][a], b=base['TipoMov'][a], c=base['DataOcorrencia'][a], d=base['QtdeMovimento'][a], e=base['ValorMov'][a], f=base['ValorVenda'][a])
		
		bf.cursor.execute(insert)
		bf.con.commit() 
		print("dados %d inserido com sucesso" %a)
		a+=1
	return print("Dados adicionados com sucesso!")


dados_FA = """
INSERT INTO FilialAtividade(Filial, TipoMov, DataOcorrencia, QtdeMovimento, ValorMov, ValorVenda) VALUES('{aa}', \'{b}\', '{c}', '{d}', '{e}', '{f}')
"""

base_ativ = consulta(ativ)
insertDados(dados_FA, base_ativ)


