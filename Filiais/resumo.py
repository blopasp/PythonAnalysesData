import pandas as pd
import pyodbc as o
import baseFiliais as bf
import gc
from datetime import date


# Query resumo
resumo = """
	SELECT top 10
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
	
	server = server 
	database = database 

	con = o.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database) 
	cursor = con.cursor()
	base = pd.read_sql(query, con)

	print("============== Base extraída com sucesso")
	return base

# funcao para testar data de atualizacao
def shiftBase(base):
    
    ints = base.select_dtypes(include=['int64','int32','int16']).columns
    base[ints] = base[ints].apply(pd.to_numeric, downcast='integer')

    floats = base.select_dtypes(include=['float']).columns
    base[floats] = base[floats].apply(pd.to_numeric, downcast='float')

    lista = list(base.columns)

    for i in range(len(lista)):
        
        if True == list(base.columns.str.startswith('Data' or 'DT'))[i]:
            base[lista[i]] = pd.to_datetime(base[lista[i]], errors = 'coerce')
    
    del lista

    objects = base.select_dtypes('object').columns
    base[objects] = base[objects].apply(lambda x: x.astype('category'))
  
    gc.collect()
    
	print("============== Tpos de dados melhorados com sucesso")

    return base

def insertData(string, base):
    
	insert = """
		INSERT INTO {}{} VALUES(""".format(string,tuple(base.columns))

	for i in range(len(tuple(base.columns))):
		if i != (len(tuple(base.columns))-1):
			insert = insert+"'{}',"
		else:
			insert = insert+"'{}')\n"

	if len(base) != 0:
		concat = ","+insert.split(sep = ("VALUES"))[len(insert.split(sep = ("VALUES")))-1]

		for index, row in base.iterrows():
			insert = insert.format(*row)
			break

		for index, row2 in base.iterrows():
			if index == 0:
				continue
			insert = insert+concat.format(*row2)
        
		bf.comando(insert)
        
		return print("******** Dados inseridos com sucesso! ********")
    
	else:
		return print("#### BASE VAZIA! ####")

def test(base):
	
	base['DataAtualizacao'] = pd.to_datetime(base['DataAtualizacao'])
	dataAtualizacaoMax = base['DataAtualizacao'].max()

	data_max = pd.read_sql("select max(DataAtualizacao) as dataMax from FilialResumo;", bf.con)
	data_max.dataMax = pd.to_datetime(data_max['dataMax'])
	test = data_max['dataMax'].max()

	if (test != dataAtualizacaoMax):
		return True
	else:
		return False

# consultando dados no banco
base_resumo = consulta(resumo)
base_resumo = shiftBase(base_resumo)

# teste para verificar se os dados do dia já foi atualizado
# caso verdadeiro que não foi adicionado dados de hoje, chama a função de inserir dados
if test(base_resumo):
	insertData("FilialResumo", base_resumo)
else:
	print("************ Dados de hoje já adicionados ************")
