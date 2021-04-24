import sqlite3

#criando conexão com o banco
con = sqlite3.connect("C:\\Estudos\\Resumo Filiais\\base\\FiliaisData.db")

cursor = con.cursor()

base_FilialRegiao = """
CREATE TABLE IF NOT EXISTS FilialRegiao (
    Filial INTEGER PRIMARY KEY,
    Cidade TEXT NOT NULL,
    UF TEXT NOT NULL,
    Regiao TEXT NOT NULL,
    BRICK INTEGER NOT NULL
);
"""


#Criando tabela Filial localizacao
cursor.execute(base_FilialRegiao)

#Criando tabela Filial Resumo
cursor.execute("""
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
""")

#Criando tabela Filial atividade
cursor.execute("""
CREATE TABLE IF NOT EXISTS FilialAtividade (
    Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    Filial INTEGER NOT NULL,
    TipoMov TEXT NOT NULL,
    DataOcorrencia TEXT NOT NULL,
    QtdeMovimento INTEGER NOT NULL,
    ValorMov REAL NOT NULL,
    ValorVenda REAL NOT NULL,
    CONSTRAINT fk_atividade_regiao FOREIGN KEY(id) references FilialRegiao (id)
);
""")

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

#test = pd.read_sql("select * from FilialRegiao;", con)

print("Conexão com o banco realizada com sucesso!")
