import sys

CONFIG = {
    'my_env': {
        'server': 'site',
        'api_version': '3.7',
        'username': sys.argv[0],
        'password': sys.argv[1],
        'site_name': '',
        'site_url': ''
    }
}

filial = """
    select * from Resumo;
"""
atividade = """
    select * from Atividade
"""
regiao = """
    select * from Regiao
"""

def consultBase(consult):
    con = sqlite3.connect("C:\\Estudos\\Resumo Filiais\\base\\FiliaisData.db")
    cursor = con.cursor()

    base = pd.read_sql(consult, con)
    base = formatBase(base)

    return base

def formatBase(base):
    
    ints = base.select_dtypes(include=['int64','int32','int16']).columns
    base[ints] = base[ints].apply(pd.to_numeric, downcast='integer')

    floats = base.select_dtypes(include=['float']).columns
    base[floats] = base[floats].apply(pd.to_numeric, downcast='float')

    lista = list(base.columns)

    for i in range(len(lista)):
        
        if True == list(base.columns.str.startswith('Data' or 'DT'))[i]:
            base[lista[i]] = pd.to_datetime(base[lista[i]])
    
    del lista

    objects = base.select_dtypes('object').columns
    base[objects] = base[objects].apply(lambda x: x.astype('category'))

    return base

def constructTableau(TO_SAIDA, base):

    lista = list(base.columns)
    dates = list(base.select_dtypes('datetime64[ns]').columns)
    categories = list(base.select_dtypes('category').columns)
    floats = list(base.select_dtypes(include=['floating']).columns)
    ints = list(base.select_dtypes(include=['integer']).columns)


    with HyperProcess(Telemetry.SEND_USAGE_DATA_TO_TABLEAU, 'meuapp') as hyper:
        with Connection(endpoint = hyper.endpoint,
                        create_mode = CreateMode.CREATE_AND_REPLACE,
                        database = TO_SAIDA) as connection:

            schema = TableDefinition(
                table_name = 'base',
                columns=[
                    
            ])
                
            for i in lista:
                if i in ints:
                    schema.add_column(i, SqlType.int())
                elif i in floats:
                    schema.add_column(i, SqlType.double())
                elif i in categories:
                    schema.add_column(i, SqlType.text())
                elif i in dates:
                    schema.add_column(i, SqlType.date())
                else: 
                    print("Tipo não encontrado")

            connection.catalog.create_table(schema)
            
            with Inserter(connection, schema) as inserter:
                for index, row in base.iterrows():
                    inserter.add_row(row)
                inserter.execute()
                
        print("A conexão com o arquivo Hyper está fechada.")
    
    return TO_SAIDA

def connTableau(config, saida, base, name): 
    conn = TableauServerConnection(config_json=config, env='my_env')
    conn.sign_in()

    response = conn.publish_data_source(datasource_file_path=constructTableau(saida, base),
                                        datasource_name=name,
                                        project_id='c2f823f5-790c-49bb-996f-a1e022125bc8')

    print(response.json())

    conn.sign_out()

if __name__ == '__main__':
    from tableauhyperapi import (HyperProcess, Connection, TableDefinition, SqlType,
                             Telemetry, Inserter, CreateMode, TableName)
    from tableau_api_lib import TableauServerConnection
    import pandas as pd
    import sqlite3

    # ==== Base Filial ====
    sainda_resumo = 'resumo.hyper'
    baseFilial = consultBase(filial)
    connTableau(CONFIG, sainda_resumo, baseFilial, name = 'Resumo')

    # ==== Base Atividade ====
    saida_atividade = 'atividade.hyper'
    baseAtividade = consultBase(atividade)
    connTableau(CONFIG, saida_atividade, baseAtividade, name = 'Atividade')

    # ==== Base Regiao ====
    saida_regiao = 'regiao.hyper'
    baseRegiao = consultBase(regiao)
    connTableau(CONFIG, saida_regiao, baseRegiao, name = 'Regiao')
