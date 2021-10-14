import gc, sys, sqlite3

def consulta(query):
    server = sys.argv[1]
    database = sys.argv[2]
    con =  o.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database)
    con.cursor()
    base = pd.read_sql(query, con)

    print("============== Base extraída com sucesso!")
    return base

def test(base):
    
    base = pd.to_datetime(base)
    dataAtualizacaoMax = base.max()

    data_max = pd.read_sql("select max(DataAtualizacao) as dataMax from FilialResumo;", 
        sqlite3.connect(bf.CON))
    data_max.dataMax = pd.to_datetime(data_max['dataMax'])
    test = data_max['dataMax'].max()

    if (test != dataAtualizacaoMax):
        return True
    else:
        return False

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

if __name__ == '__main__':
    import pandas as pd
    import pyodbc as o
    import Filiais.dados as bf
    
    # ETL base de atividade
    base_ativ = shiftBase(consulta(sys.argv[3]))
    bf.insertData("FilialAtividade", base_ativ)
    
    # ETL base de resumo
    base_resumo = shiftBase(consulta(sys.argv[4]))

    # teste para verificar se os dados do dia já foi atualizado
    # caso verdadeiro que não foi adicionado dados de hoje, chama a função de inserir dados
    if test(base_resumo['DataAtualizacao']):
        bf.insertData("FilialResumo", base_resumo)
    else:
        print("************ Dados de hoje já adicionados ************")

    # ETL base de regiao
    bf.comando("""
    DELETE FROM FilialRegiao;
    """)
    
    base_regiao = consulta(regiao)
    bf.insertData("FilialRegiao", base_regiao)