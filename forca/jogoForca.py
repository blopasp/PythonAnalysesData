class Forca():

    def __init__(self, palavra):
        self.palavra = palavra
        self.letraCerta = []
        self.letraErrada = []
        print('Jogo iniciado com sucesso!\n Vamos começar?\n')

    def aposta(self, letra):
        # Verifica se a letra faz parte da palavra e, se fizer, armazena dentro da lista letraErrada
        if letra in self.palavra and letra not in self.letraErrada:
            self.letraCerta.append(letra)
        # Verifica se a letra faz parte da palavra e, se não fizer, armazena dentro da lista letraCerta
        elif letra not in self.palavra and letra not in self.letraErrada:
            self.letraErrada.append(letra)
        else:
            return False
        return True
    
    def letrasRestantes(self):
        esc = ''
        for letra in self.palavra:
            if letra not in self.letraCerta:
                esc += '*'
            else:
                esc += letra
        return esc

    def ganhou(self):
        if '*' not in self.letrasRestantes():
            return True
        return False

    def fimJogo(self):
        return self.ganhou() or (len(self.letraErrada) == 6)

    def status(self):
        print('\nPalavra '+ self.letrasRestantes())
        print('Letras erradas: ',)
        for i in self.letraErrada:
            print(i,)
        print()
        print('Letras certas: ',)
        for i in self.letraCerta:
            print(i,)
        print()

def arquivo():
    with open("palavras.txt", "rt") as f:
        palavras = f.readlines()
    #strip remover espaçoes entre as linhas
    return palavras[random.randint(0, len(palavras)-1)].strip()

def main():
    print('''
    ##################################################
    \n\t\tBem vindo ao Jogo da forca\n
    ''')
    # Objeto
    jogo = Forca(arquivo())
    while not jogo.fimJogo():
        jogo.status()
        usuario = input('\nDigite uma letra: ')
        jogo.aposta(usuario)        

    if jogo.ganhou():
        print('\n\n********* Parabéns, Você Ganhou! *********')
        print('\nPalavra: ' + jogo.palavra)
    else:
        print('\n\nNão foi dessa vez! A palavra certa é %s' %jogo.palavra)
        print('\nTente novamente!')

if __name__ == "__main__":
    import random
    main()