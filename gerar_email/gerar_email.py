# Classe para gerar email para servidores em geral


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders
import os, mimetypes, smtplib
import datetime as dt


class gerar_email:

    def __init__(self, login, senha, assunto, servidor, porta, destino, copia = '', bcc = ''):
        self.login = login
        self.senha = senha
        self.destino = destino
        self.copia = copia
        self.bcc = bcc
        self.assunto = assunto

        # informações sobre servidor
        self.servidor = servidor
        self.porta = porta

        self.msg = MIMEMultipart()

    # = Funcao para adicionar anexos
    def add_anexo(self, filename):
        # verificando se o arquivo existe no caminho indicado
        if not os.path.isfile(filename):
            return
        
        #extraindo ctype (classe do tipo do arquivo) e o encoding do arquivo
        ctype, encoding = mimetypes.guess_type(filename)
        
        # caso não tenho classe de tipo definido ou a ausência do encoding
        # adiciona o ctype padrao
        if ctype is None or encoding is not None:
            ctype = 'application/octet-stream'
            
        #pegando o tipo principal e o subtipo da classe do tipo do arquivo
        maintype, subtype = ctype.split('/', 1)
        
        # ESTRUTURA CONDICIONAL DE ACORDO COM O TIPO DE ARQUIVOS
        
        # tipo de arquiivo texto
        if maintype == 'text':
            with open(filename) as f:
                mime = MIMEText(f.read(), _subtype = subtype)
                
        # tipo de arquivo imagem        
        elif maintype == 'image':
            with open(filename, 'rb') as f:
                mime = MIMEImage(f.read(), _subtype = subtype)
                
        # outros tipos de arquivos        
        else:
            with open(filename, 'rb') as f:
                mime = MIMEBase(maintype, subtype)
                mime.set_payload(f.read())
                
            encoders.encode_base64(mime)
            
        # formatando nome do arquivo    
        arquivo_add = filename.split('\\')
        arquivo_add = arquivo_add[len(arquivo_add) - 1]
        
        # adicionando o cabeçalho do arquivo em relação ao email
        mime.add_header('Content-Disposition', 'attachment; filename= %s' %arquivo_add)
        # adicionando anexo ao email
        self.msg.attach(mime)

    # = Funcao para enviar email
    def emailGT(self, corpo_email, anexos:list, imagens_corpo_texto_com_assinatura:list, html = True):    
        
        # parametros do email 
        self.msg['Subject'] = self.assunto
        self.msg['To'] = ', '.join(self.destino)
        self.msg['Cc'] = ', '.join(self.copia)
        self.msg['Bcc'] = ','.join(self.bcc)
        self.msg['From'] = self.login

        # escolhenco corpo do email
        if html:
            self.msg.attach(MIMEText(corpo_email, 'html'))
        else:
            self.msg.attach(MIMEText(corpo_email, 'plain'))
        
        # adicionando no corpo do texto de forma cid, em caso de corpo email html
        # gerando lista da seguinte forma list_anexo = [[caminho_imagem, assinatura]]
        if html:
            for imagem in imagens_corpo_texto_com_assinatura:
                with open(imagem[0], 'rb') as imagem_arq:
                    imagem = MIMEImage(imagem_arq.read())
                imagem.add_header('Content-ID', imagem[1])
                self.msg.attach(imagem)       
        # adicionando anexo
        for anexo in anexos:
            # aplicando funcao de adicionar anexo
            self.add_anexo(self.msg, anexo)

        # adicionando todos os email ao conjunto destinos
        destinos = set(self.destino)
        [destinos.add(c) for c in self.copia]
        [destinos.add(b) for b in self.bcc]

        #  server = smtplib.SMTP(servidor, porta)    
        try:
            with smtplib.SMTP(self.servidor, self.porta) as server:
                # iniciar servidor
                server.starttls()
                # fazendo login
                server.login(self.login, self.senha)
                # enviando enmail
                server.sendmail(self.login, destinos, self.msg.as_string())
                
            with open('log.txt', 'a') as add:                
                add.write('OK envio ' + self.assunto + ' - '+ format(dt.date.today(), '%d/%m/%Y') + '\n\nAnexos:\n')
                for anexo in anexos:
                    anexo_arq = anexo.split('\\')
                    anexo_arq = anexo_arq[len(anexo_arq)-1]
                    
                    add.write(anexo_arq+'\n')
                add.write('\nDESTINOS:\n')
                for destino in destinos:
                                       
                    add.write(destino+'\n')
                            
        except:
            with open('log.txt', 'a') as add:
                
                add.write('NOT OK envio - Nome Comprador: '+self.assunto + format(dt.date.today(), '%d/%m/%Y') + '\n\nAnexos:\n')
                for anexo in anexos:
                    anexo_arq = anexo.split('\\')
                    anexo_arq = anexo_arq[len(anexo_arq)-1]
                    add.write(anexo_arq+'\n')

                add.write('\nDESTINOS:\n')
                for destino in destinos:                
                    add.write(destino+'\n')