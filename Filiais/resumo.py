import pandas as pd
import pyodbc as o
import baseFiliais as bf
from datetime import date

# Query resumo
resumo = """
	SELECT 
	CAST(PF.FILI_CD_FILIAL AS NUMERIC) AS Filial,
	FL.FILI_FL_SITUACAO AS SitLoja,
	NIVEL1.CAPN_DS_CATEGORIA AS NIVEL1,
	CASE
		WHEN NIVEL2.CAPN_DS_CATEGORIA IN ('OTC', 'RX')
		THEN CONCAT(NIVEL2.CAPN_DS_CATEGORIA, ' - ', NIVEL5.CAPN_DS_CATEGORIA)
		ELSE NIVEL2.CAPN_DS_CATEGORIA
	END NIVEL2,
	COUNT(PF.PRME_CD_PRODUTO) AS SKUTotal,
	COUNT(CASE
			WHEN PRFI_FL_SITUACAO = 'A' THEN PF.PRME_CD_PRODUTO
			ELSE NULL END) SKUAtivo,
	COUNT(CASE
			WHEN PRFI_FL_SITUACAO = 'D' THEN PF.PRME_CD_PRODUTO
			ELSE NULL END) SKUDesativado,
	CAST(SUM(PF.ESTQUE_ALVO) AS NUMERIC) AS EstoqueAlvo,
	CAST(SUM(PF.PRFI_QT_UNDFAC) AS NUMERIC) AS QtdeUndFac,
	CAST(SUM(PF.PRFI_QT_ESTOQATUAL) AS NUMERIC) AS QtdeEstoqueAtual,
	CAST(SUM(PF.PRFI_QT_ESTOQATUAL*PRFI_VL_CMPG) AS MONEY) AS ValorEstoqueAtual,
	CONVERT(DATE,GETDATE(), 103) AS DataAtualizacao

	FROM PRODUTO_FILIAL PF WITH (NOLOCK)

	INNER JOIN PRODUTO_MESTRE PM (NOLOCK)
	ON PM.PRME_CD_PRODUTO = PF.PRME_CD_PRODUTO
	INNER JOIN FILIAL FL (NOLOCK)
	ON FL.FILI_CD_FILIAL = PF.FILI_CD_FILIAL
	INNER JOIN CATEGORIA_PRODUTO_NOVO CP (NOLOCK)
	ON CP.CAPN_CD_CATEGORIA = PM.CAPN_CD_CATEGORIA
	LEFT JOIN DBO.CATEGORIA_PRODUTO_NOVO NIVEL1 (NOLOCK)
	ON SUBSTRING(PM.CAPN_CD_CATEGORIA,1,1)+'.000.000.00.00.00.00.00' = NIVEL1.CAPN_CD_CATEGORIA
	LEFT JOIN DBO.CATEGORIA_PRODUTO_NOVO NIVEL2 (NOLOCK)
	ON SUBSTRING(PM.CAPN_CD_CATEGORIA,1,5)+'.000.00.00.00.00.00' = NIVEL2.CAPN_CD_CATEGORIA
	LEFT JOIN DBO.CATEGORIA_PRODUTO_NOVO NIVEL3 (NOLOCK)
	ON SUBSTRING(PM.CAPN_CD_CATEGORIA,1,9)+'.00.00.00.00.00' = NIVEL3.CAPN_CD_CATEGORIA
	LEFT JOIN DBO.CATEGORIA_PRODUTO_NOVO NIVEL5 (NOLOCK)
	ON SUBSTRING(PM.CAPN_CD_CATEGORIA,1,15)+'.00.00.00' = NIVEL5.CAPN_CD_CATEGORIA

	WHERE
		PM.CAPN_CD_CATEGORIA NOT LIKE '3%'AND
		PM.CAPN_CD_CATEGORIA NOT LIKE '1.101.009%' AND
		PM.CAPN_CD_CATEGORIA NOT LIKE '1.102.009%' AND
		PM.CAPN_CD_CATEGORIA NOT LIKE '2.504.001%'

	GROUP BY
		CAST(PF.FILI_CD_FILIAL AS NUMERIC),
		FL.FILI_FL_SITUACAO,
		NIVEL1.CAPN_DS_CATEGORIA,
		CASE
		WHEN NIVEL2.CAPN_DS_CATEGORIA IN ('OTC', 'RX')
		THEN CONCAT(NIVEL2.CAPN_DS_CATEGORIA, ' - ', NIVEL5.CAPN_DS_CATEGORIA)
		ELSE NIVEL2.CAPN_DS_CATEGORIA
		END
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
def test(base):
	
	base['DataAtualizacao'] = pd.to_datetime(base['DataAtualizacao'])
	dataAtualizacaoMax = base['DataAtualizacao'].max()

	data_max = pd.read_sql("select max(DataAtualizacao) as dataMax from FilialResumo;", bf.con)
	data_max.dataMax = pd.to_datetime(data_max['dataMax'])
	test = data_max['dataMax'].max()

	if (test != dataAtualizacaoMax):
		mes = "OK"
		return True
	else:
		mes = "Dados de hoje já adicionados ao banco"
		return False

# funcao para inserir dados para o banco
def insertDados(string, base):
	
	message = test(base)

	if message(base):

		a=0
		for i in range(len(base)):
			insert = string.format(aa = base['Filial'][a], b = base['SitLoja'][a], c = base['NIVEL1'][a], d = base['NIVEL2'][a], e = base['SKUTotal'][a], f = base['SKUAtivo'][a], g = base['SKUDesativado'][a], h = base['EstoqueAlvo'][a], i = base['QtdeUndFac'][a], j = base['QtdeEstoqueAtual'][a], k = base['ValorEstoqueAtual'][a], l = base['DataAtualizacao'][a])
			
			bf.cursor.execute(insert)
			bf.con.commit()

			print("dados %d inserido com sucesso" %a)
			a + = 1

		return print("Dados inseridos com sucesso!")

	else:
		return message

base_resumo = consulta(resumo)

dados_FR = """
INSERT INTO FilialResumo(Filial, SitLoja, NIVEL1, NIVEL2, SKUTotal, SKUAtivo, SKUDesativado, EstoqueAlvo, QtdeUndFac, QtdeEstoqueAtual, ValorEstoqueAtual, DataAtualizacao) VALUES('{aa}', \'{b}\', \'{c}\', '{d}', '{e}', '{f}', '{g}', '{h}', '{i}', '{j}', '{k}', '{l}')
"""
insertDados(dados_FR, base_resumo)