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