import pandas as pd
import pyodbc as o
import baseFiliais as bf
import gc

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

	print("============== Base extraída com sucesso!")

	return base

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

base_ativ = consulta(ativ)
base_ativ = shiftBase(base_ativ)
insertData("FilialAtividade", base_ativ)


