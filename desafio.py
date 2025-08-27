from abc import ABC, abstractmethod
from datetime import datetime
import textwrap

class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []
    
    @property
    def endereco(self):
        return self._endereco
    
    @property
    def contas(self):
        return self._contas
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def __str__(self):
        return f"""
            Endereço do cliente: {self.endereco}
            Contas: {[conta.numero for conta in self.contas]}
        """
    
class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        self._cpf = cpf
        self._nome = nome
        self._data = data_nascimento
        super().__init__(endereco)

    @property
    def cpf(self):
        return self._cpf
    
    @property
    def nome(self):
        return self._nome
    
    @property
    def data(self):
        return self._data
    
    def __str__(self) -> str:
        return f"""
            CPF:  {self.cpf}
            Nome: {self.nome}
            Nascimento: {self.data}
            Endereço do cliente: {self.endereco}
            Contas: {[str(conta.numero) for conta in self.contas]}
        """
    
class Conta:
    def __init__(self, cliente, numero):
        self._numero = numero
        self._cliente = cliente
        self._saldo = 0
        self._agencia = "101"
        self._historico = Historico()
    
    @property
    def numero(self):
        return self._numero

    @property
    def cliente(self):
        return self._cliente
    
    @property
    def agencia(self):
        return self._agencia

    @property
    def historico(self):
        return self._historico
    
    @property
    def saldo(self):
        return self._saldo
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(cliente, numero)
    
    def sacar(self, valor):
        if valor < 0:
            print("Erro: Valor inválido.")
            return False
        elif self.saldo >= valor:
            self._saldo -= valor
            print("Saque realizado com sucesso.")
            return True
        else:
            print("Erro: Saque mal sucedido")
            return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Depósito bem sucedido")
            return True
        print("Erro: Depósito mal sucedido")
        return False
    
    def __str__(self):
        return f"""
            Agência: {self.agencia}
            Código:  {self.numero}
            Titular: {self.cliente.nome}
        """
    
class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite=500, limite_saques=3):
        super().__init__(cliente, numero)
        self._limite = limite
        self._limite_saques = limite_saques
    
    @property
    def limite(self):
        return self._limite
    
    @property
    def limite_saques(self):
        return self._limite_saques
    
    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes
             if transacao["tipo"] == Saque.__name__]
        )
        if self.limite < valor:
            print("Erro: Limite atingido no valor de saque.")
            return False
        if self.limite_saques == numero_saques:
            print("Erro: Número de saques atingido.")
            return False
        else:
            return super().sacar(valor)

    def __str__(self):
        return super().__str__()    
    
class Historico:
    def __init__(self):
        self._transacoes = []
    
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        super().__init__()
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        transacao = conta.depositar(self.valor)
        
        if transacao:
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        transacao = conta.sacar(self.valor)

        if transacao:
            conta.historico.adicionar_transacao(self)

def menu():
    menu = """
    ---------- Menu ----------
        [d] Depositar
        [s] Sacar
        [e] Extrato
        [nc] Nova conta
        [nu] Novo usuário
        [lu] Lista usuários
        [lc] Lista contas
        [p] Parar

    => """

    return input(textwrap.dedent(menu))

def depositar(clientes):
    cpf = input("Informe o CPF: ")
    cliente = filtrar_cliente(cpf, clientes)
    
    if cliente != False:
        valor = float(input("Informe o valor a ser depositado: "))
        transacao = Deposito(valor)
        conta = recuperar_conta(cliente)
        if not conta:
            return
        cliente.realizar_transacao(conta, transacao)
    else:
        print("Erro: Cliente não encontrado.")

def sacar(clientes):
    cpf = input("Informe o CPF: ")
    cliente = filtrar_cliente(cpf, clientes)
    if cliente != False:
        valor = float(input("Informe o valor a ser sacado: "))
        transacao = Saque(valor)
        conta = recuperar_conta(cliente)
        if not conta: 
            return
        cliente.realizar_transacao(conta, transacao)
    else: 
        print("Erro: Cliente não encontrado.")

def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente != False:
        conta = recuperar_conta(cliente)
        if not conta:
            return
        
        print("################### EXTRATO ###################")
        transacoes = conta.historico.transacoes

        extrato = ""
        if not transacoes:
            extrato = "Não foram realizadas movimentações."
        else:
            for transacao in transacoes:
                extrato += f"\n{transacao['tipo']}:\n\tR${transacao['valor']:.2f}"
        print(extrato)
        print(f"\nSaldo: R${conta.saldo:.2f}")
        print("################################################")

def filtrar_cliente(cpf, clientes):
    for cliente in clientes:
        if cliente.cpf == cpf:
            return cliente
    return False

def recuperar_conta(cliente):
    if not cliente.contas:
        print("Erro: Conta não detectada.")
        return
    
    contas_disponiveis = ', '.join(str(conta.numero) for conta in cliente.contas)
    print(f"As contas disponíveis do cliente são:\n{contas_disponiveis}")
    num_conta = int(input("Informe o número da conta desejada: "))
    index = -1
    for conta in cliente.contas:
        index += 1
        if conta.numero == num_conta:
            return cliente.contas[index]

def criar_cliente(clientes):
    cpf = input("Escreva seu CPF: ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente == False:
        nome = input("Escreva seu nome: ")
        data = input("Escreva sua data de nascimento (dd/mm/aaaa): ")
        endereco = input("Escreva seu endereco (logradouro, n° - bairro - cidade/sigla estado): ")
        novo_cliente = PessoaFisica(cpf, nome, data, endereco)
        clientes.append(novo_cliente)
        print("Cliente criado com sucesso.")
    else:
        print("Erro: Cliente já inscrito.")

def criar_conta(numero, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    
    if cliente != False:
        conta = ContaCorrente.nova_conta(cliente, numero)
        contas.append(conta)
        cliente.adicionar_conta(conta)
        print("Conta criada com sucesso.")
    else:
        print("Erro: Cliente não detectado.")

def listar_clientes(clientes):
    for cliente in clientes:
        print(str(cliente))

def listar_contas(contas):
    for conta in contas:
        print(str(conta))

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == 'd':
            depositar(clientes)
        elif opcao == 's':
            sacar(clientes)
        elif opcao == 'e':
            exibir_extrato(clientes)
        elif opcao == 'nu':
            criar_cliente(clientes)
        elif opcao == 'nc':
            numero_conta = len(contas)+1
            criar_conta(numero_conta, clientes, contas)
        elif opcao == 'lu':
            listar_clientes(clientes)
        elif opcao == 'lc':
            listar_contas(contas)
        elif opcao == 'p':
            print("Saindo do processo...")
            break
        else:
            print("Erro: Operação inválida. Por favor, selecione novamente a operação desejada.")