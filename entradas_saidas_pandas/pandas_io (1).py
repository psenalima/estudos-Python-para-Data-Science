# -*- coding: utf-8 -*-
"""Pandas IO.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1p1DPfgKFFOlnn5qsbRW-3SwKR7XnMkjA

#Criando os nomes
"""

import pandas as pd
import numpy as np

nomes_f = pd.read_json("https://servicodados.ibge.gov.br/api/v1/censos/nomes/ranking?qtd=200&sexo=f")
nomes_m = pd.read_json("https://servicodados.ibge.gov.br/api/v1/censos/nomes/ranking?qtd=200&sexo=m")

nomes_f

nomes_m

print("Quantidade de nomes: " ,len(nomes_f) + len(nomes_m))

print("Quantidade de nomes: " ,nomes_f.shape[0] + nomes_m.shape[0])

frames = [nomes_f, nomes_m]
nomes = pd.concat(frames)['nome'].to_frame()

nomes.head(10)

nomes.sample(5)

"""#Incluindo ID dos alunos"""

import numpy as np
np.random.seed(123)

total_alunos = len(nomes)
total_alunos

nomes.sample(3)

nomes["id_aluno"] =  np.random.permutation(total_alunos) + 1

nomes

dominios = ['@dominiodoemmail.com.br', '@servicodoemail.com']

dominios = ['@dominiodoemmail.com.br', '@servicodoemail.com']
nomes['dominio'] = np.random.choice(dominios, total_alunos)

nomes

nomes['email'] = nomes.nome.str.cat(nomes.dominio).str.lower()

nomes.head(10)

"""#Lista de Cursos"""

!pip3 install html5lib
!pip3 install lxml

url = 'http://tabela-cursos.herokuapp.com/index.html'
cursos = pd.read_html(url)
cursos

cursos = cursos[0]

cursos.head(10)

"""#Alterando index dos cursos"""

cursos = cursos.rename(columns={'Nome do curso': 'nome_do_curso'})
cursos.head(2)

cursos['id'] = cursos.index + 1
cursos.head()

cursos = cursos.set_index('id')
cursos.head()



"""#Matriculando os alunos nos cursos"""

nomes['matriculas'] = np.ceil(np.random.exponential(size=total_alunos) * 1.5).astype(int)
nomes.sample(5)

nomes.matriculas.describe()

import seaborn as sns

sns.distplot(nomes.matriculas)

nomes.matriculas.value_counts()

"""#Selecionando cursos"""

todas_matriculas = []
x = np.random.rand(20)
prob = x / sum(x)

for index, row in nomes.iterrows():
  id = row.id_aluno
  matriculas = row.matriculas
  for i in range(matriculas):
    mat = [id, np.random.choice(cursos.index, p = prob)]
    todas_matriculas.append(mat)

matriculas = pd.DataFrame(todas_matriculas, columns = ['id_aluno', 'id_curso'])
matriculas.head(5)

matriculas_por_curso = matriculas.groupby('id_curso').count().join(cursos['nome_do_curso']).rename(columns={'id_aluno':'quantidade_de_alunos'})

nomes.sample(3)

cursos.head()

matriculas.head()

matriculas_por_curso.head()

"""#Saída em diferentes formatos"""

matriculas_por_curso.to_csv('matriculas_por_curso.csv', index=False)

pd.read_csv('matriculas_por_curso.csv')

matriculas_json = matriculas_por_curso.to_json()
matriculas_json

matriculas_html = matriculas_por_curso.to_html()
matriculas_html

print(matriculas_html)

from sqlalchemy import create_engine, MetaData, Table, inspect # adicionando o método inspect

engine = create_engine('sqlite:///:memory:')
engine
type(engine)

matriculas_por_curso.to_sql('matriculas', engine)

inspector = inspect(engine) # criando um Inspector object
print(inspector.get_table_names()) # Exibindo as tabelas com o inspecto

"""#Criando o banco sql"""

!pip3 install sqlalchemy

from sqlalchemy import create_engine, MetaData, Table

engine = create_engine('sqlite:///:memory:')

type(engine)

matriculas_por_curso.to_sql('matriculas', engine)

print(engine.table_names())

"""#Buscando do banco sql"""

query = 'select * from matriculas where quantidade_de_alunos < 20'

pd.read_sql(query, engine)

pd.read_sql_table('matriculas', engine, columns=['nome_do_curso', 'quantidade_de_alunos'])
#query = 'select nome_do_curso,quantidade_de_alunos from matriculas'
#pd.read_sql(query, engine)

muitas_matriculas = pd.read_sql_table('matriculas', engine, columns=['nome_do_curso', 'quantidade_de_alunos'])

muitas_matriculas.query('quantidade_de_alunos > 60 ')

muitas_matriculas = muitas_matriculas.query('quantidade_de_alunos > 80')
muitas_matriculas

"""#Escrevendo no banco"""

muitas_matriculas.to_sql('muitas_matriculas', con=engine)

print(engine.table_names())

"""#Nomes dos alunos e alunas da próxima turma"""

matriculas_por_curso.head()

matriculas.head()

id_curso = 16
proxima_turma = matriculas.query("id_curso == {}".format(id_curso))

proxima_turma.head()

nomes.sample(3)

proxima_turma.set_index('id_aluno').join(nomes.set_index('id_aluno'))

proxima_turma.set_index('id_aluno').join(nomes.set_index('id_aluno'))[['nome']]

proxima_turma = proxima_turma.set_index('id_aluno').join(nomes.set_index('id_aluno'))['nome'].to_frame()

nome_curso = cursos.loc[id_curso]
nome_curso

nome_curso = nome_curso.nome_do_curso
nome_curso

proxima_turma.rename(columns = {'nome':'Alunos do curso de {}'.format(nome_curso)})

"""#Excel"""

proxima_turma.to_excel('proxima_turma.xlsx', index = False)

pd.read_excel('proxima_turma.xlsx')