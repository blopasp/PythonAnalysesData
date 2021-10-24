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
    conveniados = re.findall(r'([A-Z][A-Z ]+\s)([A-Z ]+[,]\s[N]\S\s\d*)(\s[-]\s[S][L]+\s\d*|\s\W\d*|\s[-][S][A][L][A]+\s\d*|\s[S][A][L][A]+\s\d*|)(\s[-]\s[A-Z][A-Z ]+)', texto)

    # criando dicionario com os padroes encontrados
    cad = {
        'Conveniado':[row[0] for row in conveniados], 
        'Endereco':[row[1] for row in conveniados], 
        'Complemento':[row[2] for row in conveniados], 
        'Cidade':[row[3] for row in conveniados]
    }
    # Criando um dataframe para 
    df = pd.DataFrame(cad)

    # Tratando dataframe
    df['Conveniado'] = df['Conveniado'].apply(lambda x: x.replace('\n', ''))
    df['Cidade'] = df['Cidade'].apply(lambda x: x.replace(' - ', ''))
    df['Complemento'] = df['Complemento'].apply(lambda x: x.replace('-', '').strip())
    df['Numero'] = df['Endereco'].apply(lambda x: x.split(',')[1])
    df['Numero'] = df['Numero'].apply(lambda x: x.split(' ')[2])
    df['Endereco'] = df['Endereco'].apply(lambda x: x.split(',')[0])

    # Reordenando as colunas e salvando o arquivo
    df = df[['Conveniado', 'Endereco', 'Numero', 'Complemento', 'Cidade']]
    df.to_csv('regex/arquivos_saida/Conveniado.csv', index=False)