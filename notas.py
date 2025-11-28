# Sistema de Gestão de Notas dos Alunos


# função para cadastrar uma nova disciplina
def cadastrar_disciplina(nome_disciplina):
    print(f"Disciplina {nome_disciplina} cadastrada com sucesso.")



def cadastrar_aluno(nome, nota):
    notas.append(nota)
    print(f"Aluno {nome} cadastrado com nota {nota}.") 



notas = [8.5, 9.0, 7.5, 6.0, 10.0]


# Função regular para calcular a média

def calcular_media(notas):

    total = sum(notas)

    media = total / len(notas)

    return media



# Função lambda para arredondar a média para duas casas decimais

arredondar_media = lambda media: round(media, 2)


# Calcular a média

media = calcular_media(notas)

media_arredondada = arredondar_media(media)



# Verificar se os estudantes foram aprovados

situacao = "O aluno está Aprovado" if media_arredondada >= 7 else "O aluno está Reprovado"


# Função de gerar Relatórios do Alunos
def gerar_relatorio(notas):
    relatorio = "Relatório de Notas dos Alunos:\n"
    for i, nota in enumerate(notas):
      relatorio += f"Aluno{i+1}: Nota {nota}\n"
    return relatorio

relatorio = gerar_relatorio(notas)




# Resultados

print(relatorio)

print("Notas:", notas)

print("Média arredondada:", media_arredondada)

print("Situação", situacao)