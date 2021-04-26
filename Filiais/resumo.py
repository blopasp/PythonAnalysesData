import pandas as pd
import pyodbc as o
import baseFiliais as bf
import gc
from datetime import date


# Query resumo
resumo = """
consulta
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
	
	base = pd.to_datetime(base)
	dataAtualizacaoMax = base.max()

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
if test(base_resumo['DataAtualizacao']):
	insertData("FilialResumo", base_resumo)
else:
	print("************ Dados de hoje já adicionados ************")
