# -*- coding: utf-8 -*-
# Author: Alzemand
# Eu li em http://web2py.com/books/default/chapter/29/07/forms-and-validators

## Validadores de Funcionarios

#Funcionario.email.requires = IS_EMAIL()
#Funcionario.telefone.requires = IS_NOT_EMPTY()
Funcionario.assunto.requires = IS_IN_SET(['Pagamento', 'Benefícios', 'Férias', 'Assuntos Gerais', 'Recrutamento e seleção', 'Promoção', 'Gestão de RH'])
Funcionario.status.requires = IS_IN_SET(['Aberto', 'Em Processo', 'Concluido'])
