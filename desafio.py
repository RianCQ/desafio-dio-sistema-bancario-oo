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