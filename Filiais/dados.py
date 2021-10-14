import sqlite3
import sys
import gc

CON = sys.argv[0]

def comando(query):
    with sqlite3.connect(CON) as con:
        cursor = con.cursor()
        cursor.execute(query)
        con.commit()

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
        
        comando(insert)
        
        return print("******** Dados inseridos com sucesso! ********")
    
    else:
        return print("#### BASE VAZIA! ####")


Regiao = """
CREATE TABLE IF NOT EXISTS FilialRegiao (
    Filial INTEGER PRIMARY KEY,
    Cidade TEXT NOT NULL,
    UF TEXT NOT NULL,
    Regiao TEXT NOT NULL,
    BRICK INTEGER NOT NULL
);
"""

Resumo = """
CREATE TABLE IF NOT EXISTS FilialResumo (
    Filial INTEGER,
    SitLoja TEXT NOT NULL,
    NIVEL1 TEXT NOT NULL,
    NIVEL2 TEXT NOT NULL,
    SKUTotal INTEGER NOT NULL,
    SKUAtivo INTEGER NOT NULL,
    SKUDesativado INTEGER NOT NULL,
    EstoqueAlvo INTEGER NOT NULL,
    QtdeUndFac INTERGER NOT NULL,
    QtdeEstoqueAtual INTEGER NOT NULL,
    ValorEstoqueAtual REAL NOT NULL,
    DataAtualizacao TEXT NOT NULL
);
"""

Atividade = """
CREATE TABLE IF NOT EXISTS FilialAtividade (
    Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    Loja INTEGER NOT NULL,
    Tipo_Movimentacao TEXT NOT NULL,
    DataOcorrencia TEXT NOT NULL,
    QtdeMovimento INTEGER NOT NULL,
    ValorMov REAL NOT NULL,
    ValorVenda REAL NOT NULL,
    CONSTRAINT fk_atividade_regiao FOREIGN KEY(id) references FilialRegiao (id)
);
"""

comando(Regiao)
comando(Resumo)
comando(Atividade)

'''
cursor.execute("""
drop table FilialRegiao;
""")
cursor.execute("""
drop table FilialResumo;
""")
cursor.execute("""
drop table FilialAtividade;
""")
cursor.execute("""
select * from FilialRegiao;
""")

'''

print("Conexão com o banco realizada com sucesso!")
