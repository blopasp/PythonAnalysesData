import pandas as pd
import pyodbc as o
import baseFiliais as bf

# Conectando ao banco de dados ====

# Query regiao
regiao = """
SELECT
	FL.FILI_CD_FILIAL Filial,
	MN.MUNI_NM_MUNICIPIO AS Cidade,
	MN.ESTA_SG_UF AS UF,
	EST.REGIAO as Regiao,
	FILI_CD_BRICK AS BRICK


FROM FILIAL FL

LEFT JOIN MUNICIPIO MN
ON MN.MUNI_SG_MUNICIPIO = FL.MUNI_SG_MUNICIPIO
AND FL.ESTA_SG_UF = MN.ESTA_SG_UF 
LEFT JOIN DBO.ESTADO EST (NOLOCK)
ON MN.ESTA_SG_UF = EST.ESTA_SG_UF

GROUP BY
FL.FILI_CD_FILIAL,
	MN.ESTA_SG_UF,
	MN.MUNI_NM_MUNICIPIO,
	FILI_CD_BRICK,
	EST.REGIAO
"""
#Fazendo consulta no banco de dados

def consulta(query):
    
    server = 'cosmos'
    database = 'cosmos_v14b'
    
    con = o.connect('DRIVER={SQL SERVER};SERVER='+server+';DATABASE='+database)
    cursor = con.cursor()
    base = pd.read_sql(query, con)
    print("============== Base extraída com sucesso!")
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

bf.comando("""
DELETE FROM FilialRegiao;
""")

base_regiao = consulta(regiao)
insertData("FilialRegiao", base_regiao)


	