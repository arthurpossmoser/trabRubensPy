import pandas as pd
import random

# ----------------------------
# 1) LISTAS BASE (NOMES/CARGOS)
# ----------------------------
nomes_m = ["João", "Carlos", "Ricardo", "Bruno", "Fernando", "Mateus", "Lucas", "Tiago", "André", "Felipe"]
nomes_f = ["Ana", "Beatriz", "Marina", "Julia", "Fernanda", "Camila", "Larissa", "Paula", "Amanda", "Letícia"]
sobrenomes = ["Silva", "Santos", "Oliveira", "Souza", "Pereira", "Costa", "Rodrigues", "Almeida", "Nascimento", "Lima", "Rubeniano"]
cargos = ["Analista de Dados", "Gerente de Projetos", "Desenvolvedor", "Designer UX", "Recursos Humanos",
          "Vendedor", "Coordenador", "Estagiário", "Diretor"]

# ----------------------------
# 2) GERAR 500 LINHAS
#    (1 a cada 20 -> salário 0)
# ----------------------------
dados = []
for i in range(1, 501):  # 1 até 500
    sexo = random.choice(["Masculino", "Feminino"])
    primeiro_nome = random.choice(nomes_m if sexo == "Masculino" else nomes_f)
    nome = f"{primeiro_nome} {random.choice(sobrenomes)}"
    cargo = random.choice(cargos)

    # Regra: 1 a cada 20 pessoas recebe salário 0
    if i % 20 == 0:
        salario = 0
    else:
        salario = random.randint(2500, 15000)

    dados.append([nome, cargo, salario, sexo])

df = pd.DataFrame(dados, columns=["Nome", "Cargo", "Salário", "Sexo"])

# (Opcional) deixar mais “apresentável” (ordena por Nome)
df = df.sort_values(by="Nome").reset_index(drop=True)

# ----------------------------
# 3) RESUMO (MAIOR, MÉDIAS, DP)
#    (arredondar 2 casas)
# ----------------------------
# Para estatísticas da empresa, normalmente faz sentido ignorar quem está com salário 0 (sem vínculo)
df_ativos = df[df["Salário"] > 0]

maior_salario = float(df_ativos["Salário"].max())
media_salarios = round(float(df_ativos["Salário"].mean()), 2)
desvio_padrao = round(float(df_ativos["Salário"].std(ddof=1)), 2)  # ddof=1 (amostral)

media_feminino = round(float(df_ativos[df_ativos["Sexo"] == "Feminino"]["Salário"].mean()), 2)
media_masculino = round(float(df_ativos[df_ativos["Sexo"] == "Masculino"]["Salário"].mean()), 2)

resumo = pd.DataFrame({
    "Indicador": [
        "Maior salário da empresa (ativos)",
        "Média dos salários (ativos)",
        "Desvio padrão dos salários (ativos)",
        "Média dos salários Femininos (ativos)",
        "Média dos salários Masculinos (ativos)"
    ],
    "Valor": [
        maior_salario,
        media_salarios,
        desvio_padrao,
        media_feminino,
        media_masculino
    ]
})

print("\n===== RESUMO =====")
print(resumo.to_string(index=False))

# ----------------------------
# 4) BUSCADOR POR NOME (SALÁRIO)
# ----------------------------
def buscar_salario_por_nome(nome_procurado: str):
    achou = df[df["Nome"].str.lower() == nome_procurado.strip().lower()]
    if achou.empty:
        return f"Nome '{nome_procurado}' não encontrado."
    # Se houver repetidos, mostra todos
    return achou[["Nome", "Cargo", "Salário", "Sexo"]]

# Exemplo (troque pelo nome que você quiser testar)
print("\n===== BUSCA POR NOME (exemplo) =====")
print(buscar_salario_por_nome("Ana Silva"))

# ----------------------------
# 5) SALVAR ARQUIVOS
# ----------------------------
df.to_csv("tabela_funcionarios_500.csv", index=False, encoding="utf-8-sig")
df.to_excel("tabela_funcionarios_500.xlsx", index=False)

resumo.to_csv("resumo_empresa.csv", index=False, encoding="utf-8-sig")
resumo.to_excel("resumo_empresa.xlsx", index=False)

print("\nArquivos gerados:")
print("- tabela_funcionarios_500.csv")
print("- tabela_funcionarios_500.xlsx")
print("- resumo_empresa.csv")
print("- resumo_empresa.xlsx")