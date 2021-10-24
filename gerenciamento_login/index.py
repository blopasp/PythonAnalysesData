#importar bibliotecas
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import DataBaser

#==== Criar Janelas e configurando-as
jan = Tk()
#nome da janela
jan.title("DP Systems - Acess Panel")
#tamanho da janela
jan.geometry("600x300")
#Cor de fundo da janela
jan.configure(background="white")
#não permiter que a caixa se expanda ou diminua
jan.resizable(width=False, height=False)
#Deixar tela transparente
jan.attributes("-alpha", 0.9)
#adicionando ícones
jan.iconbitmap(default="icons/LogoIcon.ico")

#===== Carregar Imagens
logo = PhotoImage(file="icons/logo.png")

#===== widgtes ==================
LeftFrame = Frame(jan, width=200, height=300, bg="MIDNIGHTBLUE", relief="raise")
LeftFrame.pack(side=LEFT)

RightFrame = Frame(jan, width=395, height=300, bg="MIDNIGHTBLUE", relief="raise")
RightFrame.pack(side=RIGHT)

#licando imagem
LogoLabel = Label(LeftFrame, image=logo, bg="MIDNIGHTBLUE")
LogoLabel.place(x=5, y=100)

#legenda para entrda de dados do usuário
UserLabel = Label(RightFrame, text="Username:", font=("Century Gothic", 15), bg="MIDNIGHTBLUE", fg="White")
UserLabel.place(x=5,y=100)

#Criando Caixa de texto para o usuário
UserEntry = ttk.Entry(RightFrame, width=30)
UserEntry.place(x=120, y=108)

#Criando Legenda para o usuário entrar com a senha
PassLabel = Label(RightFrame, text="Password:", font=("Centure Gothic", 15), bg="MIDNIGHTBLUE", fg="White")
PassLabel.place(x=5,y=150)

#Criando Caixa de texto para o usuário inserir senha
PassEntry = ttk.Entry(RightFrame, width=30, show="•")
PassEntry.place(x=120, y=155)

#===== Botões

#Função de login
def Login():
    User = UserEntry.get()
    Pass = PassEntry.get()

    DataBaser.cursor.execute("""
    SELECT User, Password FROM Users
    WHERE User = ? AND Password = ?
    """, (User, Pass))
    print("Selecionou")
    #Vrificar login
    VerifyLogin = DataBaser.cursor.fetchone()
    try:
        if (User in VerifyLogin and Pass in VerifyLogin):
            messagebox.showinfo(title="Login Info", message="Acesso Confirmado. Bem Vindo!")
    except:
            messagebox.showerror(title="Login Info", message="Acesso Negado. Verifique se está cadastrado no sistema!")

#Botão de Login
LoginButton = ttk.Button(RightFrame, text="Login", width=30, command=Login)
LoginButton.place(x=140, y=200)

#funcao registro
def Register():
    #Removendo widgets de login
    LoginButton.place(x=5000)
    RegisterButton.place(x=5000)
    #inserindo widgets de cadastro
    NomeLabel = Label(RightFrame, text="Name:", font=("Century Gothic", 15), bg="MIDNIGHTBLUE", fg="White")
    NomeLabel.place(x=5, y=5)
    
    NomeEntry = ttk.Entry(RightFrame, width=40)
    NomeEntry.place(x=80, y=12)

    EmailLabel = Label(RightFrame, text="Email:", font=("Century Gothic", 15), bg="MIDNIGHTBLUE", fg="White")
    EmailLabel.place(x=5, y=55)

    EmailEntry = ttk.Entry(RightFrame, width=40)
    EmailEntry.place(x=80, y=60)
    
    # Função para inserir dados no banco de dados
    def RegisterToDataBase():
        # Get retorna o valor inserido pelo usuário
        Name = NomeEntry.get()
        Email = EmailEntry.get()
        User = UserEntry.get()
        Pass = PassEntry.get()

        if (Name == "" and Email == "" and User == "" and Pass == ""):
            messagebox.showerror(title="Register Error", message="Não Deixe Nenhum Campo Vazio. Preencha Todos os Campos")
        else:
            DataBaser.cursor.execute("""
            INSERT INTO Users(Name, Email, User, Password) VALUES(?, ?, ?, ?)
            """, (Name, Email, User, Pass))
            DataBaser.conn.commit() 
            messagebox.showinfo(title="Register Info", message="Conta criada com sucesso")

    Register = ttk.Button(RightFrame, text="Register", width=30, command=RegisterToDataBase)
    Register.place(x=140, y=200)

    #função back
    def BackLogin():
        #Removendo Widgets de Cadastro
        NomeLabel.place(x=5000)
        NomeEntry.place(x=5000)
        EmailLabel.place(x=5000)
        EmailEntry.place(x=5000)
        Register.place(x=5000)
        Back.place(x=5000)
        #trazendo de volta botoes de login e register
        LoginButton.place(x=140, y=200)
        RegisterButton.place(x=140,y=250)

    Back = ttk.Button(RightFrame, text="Back", width=20, command=BackLogin)
    Back.place(x=140, y=250)

#botão de Registrar
RegisterButton = ttk.Button(RightFrame, text="Register", width=20, command=Register)
RegisterButton.place(x=140,y=250)


jan.mainloop()