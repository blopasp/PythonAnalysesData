# Processo para extrair, atraves de uma lista nao estruturada de informacoes
# de empresas conveniadas com o plano de saúde bradesco, um dataframe com
# as informacoes estruturadas, forma tabelar, utilizando técnicas de expressões
# regulares
#
# autor: Pablo Andreson

CAMINHO_PDF = "regex/arquivos_entrada/Gmail - INDICAÇÃO DE LOCAL REFERENCIADO.pdf"

def write_txt_list(list, filename):
    with open(filename, 'w') as f:
        for ele in list:
            f.write(ele+'\n')

def extract_from_pdf(path_filename):
    with fitz.open(path_filename) as pdf:
        text = ""
        for page in pdf:
            text += page.getText()
    return text

if __name__ == '__main__':
    import fitz
    import re
    from fitz.utils import write_text
    import pandas as pd

    # extraindo texto do arquivo pdf
    texto = extract_from_pdf(CAMINHO_PDF)

    # Salvando arquivo original para um arquivo txt
    with open('regex/arquivos_saida/conveniado.txt', 'w') as conv:
        conv.write(texto)

    # procurando padrao nos bairros e nas quantidades de ocorrencias
    bairros = re.findall(r'[A-Z][A-Z ]+\B\W\d{1,2}\W', texto)

    # salvando bairros para um arquivo txt
    write_txt_list(bairros, 'regex/arquivos_saida/bairros.txt')

    # Procurando padrao para encontrar conveniada, endereco, complemento e bairro
    conveniados1 = re.findall(r'(\n[A-Z]+\s.+)(\n[A-Z].+[,]\s[N]\S\s\d*)(|.+[0-9]*.+)(\s[-]\s[A-Z][A-Z ]+)([\n]\W\d{2}\W\s\d*[-]\d*\s\W\s\W\d{2}\W\s\d*[-]\d*|[\n]\W\d{2}\W\s\d*[-]\d*|)', texto)
    conveniados2 = re.findall(r'(\n[A-Z]+.+)(\n[R][a][z].+.+)(\n[A-Z].+[,]\s[N]\S\s\d*)(|.+[0-9]*.+)(\s[-]\s[A-Z][A-Z ]+)([\n]\W\d{2}\W\s\d*[-]\d*\s\W\s\W\d{2}\W\s\d*[-]\d*|[\n]\W\d{2}\W\s\d*[-]\d*|)', texto)
    
    # criando dicionario com os padroes encontrados
    cad1 = {
        'Conveniado':[row[0] for row in conveniados1], 
        'Endereco':[row[1] for row in conveniados1], 
        'Complemento':[row[2] for row in conveniados1], 
        'Bairro':[row[3] for row in conveniados1],
        'Contato 1':[row[4] for row in conveniados1]
    }

    cad2 = {
        'Conveniado':[row[0] for row in conveniados2], 
        'Endereco':[row[2] for row in conveniados2], 
        'Complemento':[row[3] for row in conveniados2], 
        'Bairro':[row[4] for row in conveniados2],
        'Contato 1':[row[5] for row in conveniados2]
    }
    # Criando um dataframe para 
    df = pd.concat([pd.DataFrame(cad1), pd.DataFrame(cad2)])

    # Tratando dataframe
    df['Conveniado'] = df['Conveniado'].apply(lambda x: x.replace('\n', ''))
    df['Bairro'] = df['Bairro'].apply(lambda x: x.replace(' - ', '').strip())
    df['Complemento'] = df['Complemento'].apply(lambda x: x.replace('-', '').strip())
    df['Numero'] = df['Endereco'].apply(lambda x: x.split(',')[1])
    df['Numero'] = df['Numero'].apply(lambda x: x.split(' ')[2])
    df['Endereco'] = df['Endereco'].apply(lambda x: x.replace('\n', '').split(',')[0])
    df['Contato 2'] = df['Contato 1'].apply(lambda x: x.split(' / ')[1].strip() if len(x.split(' / ')) == 2 else '')
    df['Contato 1'] = df['Contato 1'].apply(lambda x: x.replace('\n', '')\
        .split(' / ')[0]\
        .strip() if len(x.split(' / ')) == 2 else x.replace('\n', '').strip())

    # Reordenando as colunas e salvando o arquivo
    df = df[['Conveniado', 'Endereco', 'Numero', 'Complemento', 'Bairro', 'Contato 1', 'Contato 2']]
    
    df.to_csv('regex/arquivos_saida/Conveniado.csv', index=False)