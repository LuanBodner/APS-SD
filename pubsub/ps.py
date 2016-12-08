#coding:latin

import redis
import threading
import sys


class Listener(threading.Thread):
    def __init__(self, pubsub, canal):
        threading.Thread.__init__(self)
        self.pubsub = pubsub
        self.canal = canal
        self.working = 0
        self.subscribe(self.canal)

    def subscribe(self, canal):
        self.pubsub.subscribe(canal)
        self.working = 1

    def unsubscribe(self):
        self.pubsub.unsubscribe(self.canal)
        self.working = 0

    def imprime_mensagem(self, item):
        sys.stdout.write("\n\a" + str(item['channel'])+":"+str(item['data']) + "\n")

    def run(self):
        if self.working:
            for item in self.pubsub.listen():
                self.imprime_mensagem(item)

def listar():
    pass

def listar_proprios(inscritos):
    canais = []
    for k in inscritos.keys():
        canais.append(k)
    if len(canais) == 0:
        print("Nenhuma inscrição até o momento")
    else:
        print(canais)


def inscrever(pubsub):
    canal = input("Nome do canal:")
    l = Listener(pubsub,canal)
    l.start()
    return canal,l

def desinscrever(inscritos):
    canal = input("Canal a desinscrever:")
    if not canal in inscritos:
        print("Canal inexistente em suas inscrições")
    else:
        inscritos[canal].unsubscribe()
        del inscritos[canal]

def publicar(r):
    canal = input("Entre com o canal no qual deseja publicar:")
    mensagem=input("mensagem:")
    quantidade = r.publish(canal, mensagem)
    print("Mensagem enviada para " + str(quantidade) + " assinantes.")

def finalizar(inscritos):
    for k in inscritos.keys():
        inscritos[k].unsubscribe()
    print("FIM!")
    exit()

def main_menu(r):
    inscritos={}
    option = -1
    while option != 0:
        print("Digite:\n1\tListar canais disponíveis\n2\tListar seus canais\n3\tInscrever-se em um canal\n4\tabandonar um canal\n5\tpublicar em um canal\n0\tSair")
        option = int(input("Digite a opção:"))
        if option == 0:
            finalizar(inscritos)
        elif option == 1:
            listar(r)
        elif option == 2:
            listar_proprios(inscritos)
        elif option == 3:
            canal, listener = inscrever(r.pubsub())
            inscritos[canal]=listener
        elif option == 4:
            desinscrever(inscritos)
        elif option == 5:
            publicar(r)
        else:
            print("Opção inválida")

def le_dados_de_entrada():
    host = input("Digite o host de entrada - padrão localhost")
    if host == '':
        host = 'localhost'
    return host

def main():
    print("\tRSS Simplificado com REDIS\n\tDisciplina: Sistemas Distribuídos\n\tProf:Rodrigo Campiolo\n\tAutores:Felipe Veiga Ramos & Luan Bodner do Rosário")

    host = le_dados_de_entrada()
    r = redis.Redis(host=host)
    main_menu(r)

if __name__ == "__main__":
    main()
