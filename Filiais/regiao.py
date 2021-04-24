import pandas as pd
import pyodbc as o
import baseFiliais as bf

# Conectando ao banco de dados ====
server = 'cosmos' 
database = 'cosmos_v14b' 

conn = o.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database) 
curs = conn.cursor()

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
base_regiao = pd.read_sql(regiao, conn)

bf.cursor.execute("""
drop table FilialRegiao;
""")

bf.cursor.execute(bf.base_FilialRegiao)

#inserindo dados para o banco
a=0
for i in range(len(base_regiao)):
	insert = """
	INSERT INTO FilialRegiao(Filial, Cidade, UF, Regiao, BRICK) VALUES('{Filial}', \'{Cidade}\', '{UF}', '{Regiao}', '{BRICK}')
	""".format(Filial=base_regiao['Filial'][a], Cidade=base_regiao['Cidade'][a], UF=base_regiao['UF'][a], Regiao=base_regiao['Regiao'][a], BRICK=base_regiao['BRICK'][a])
	
	bf.cursor.execute(insert)
	bf.con.commit() 
	
	print("dados %d inserido com sucesso" %a)
	a+=1
	