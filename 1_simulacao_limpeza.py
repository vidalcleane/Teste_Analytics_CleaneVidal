import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

np.random.seed(42)
random.seed(42)

# --- Produtos e categorias ---
PRODUTOS = {
    "Quod Score PF":        ("Análise de Crédito",  450.0, 0.30),
    "Quod Score PJ":        ("Análise de Crédito",  680.0, 0.20),
    "Quod X Antifraude":    ("Prevenção a Fraude",  920.0, 0.18),
    "Cadastro Positivo":    ("Análise de Crédito",  310.0, 0.15),
    "Cobrança as a Service":("Cobrança",            750.0, 0.10),
    "Quod Identity":        ("Prevenção a Fraude",  580.0, 0.07),
}

SETORES_CLIENTE = ["Financeiro", "Varejo", "Telecom", "E-commerce", "Seguros"]

# --- Geração do dataset ---
inicio = datetime(2023, 1, 1)
fim    = datetime(2023, 12, 31)
N      = 120

nomes_produtos = list(PRODUTOS.keys())
pesos_demanda  = [PRODUTOS[p][2] for p in nomes_produtos]
datas          = [inicio + timedelta(days=random.randint(0, (fim - inicio).days)) for _ in range(N)]

registros = []
for i, data in enumerate(datas):
    produto = random.choices(nomes_produtos, weights=pesos_demanda)[0]
    categoria, preco_base, _ = PRODUTOS[produto]
    fator_sazon = 1.30 if data.month >= 10 else 1.0
    quantidade  = max(1, int(np.random.poisson(lam=8 * fator_sazon)))
    preco       = round(preco_base * np.random.uniform(0.90, 1.15), 2)
    setor       = random.choice(SETORES_CLIENTE)
    registros.append({
        "ID":           i + 1,
        "Data":         data.strftime("%Y-%m-%d"),
        "Produto":      produto,
        "Categoria":    categoria,
        "Setor_Cliente":setor,
        "Quantidade":   quantidade,
        "Preço":        preco,
    })

df = pd.DataFrame(registros)

# --- Imperfeições propositais ---
idx_nulos = np.random.choice(df.index, size=int(N * 0.08), replace=False)
df.loc[idx_nulos[:4], "Quantidade"] = np.nan
df.loc[idx_nulos[4:], "Preço"]      = np.nan
duplicatas = df.sample(5, random_state=1)
df = pd.concat([df, duplicatas], ignore_index=True)
df["Quantidade"] = df["Quantidade"].astype(object)
df.loc[idx_nulos[:2], "Quantidade"] = "N/A"

# --- Limpeza ---
df["Quantidade"] = pd.to_numeric(df["Quantidade"], errors="coerce")
df["Data"]       = pd.to_datetime(df["Data"])
df["Quantidade"] = df["Quantidade"].astype("float64")
df["Preço"]      = df["Preço"].astype("float64")

mediana_qtd   = df.groupby("Produto")["Quantidade"].transform("median")
mediana_preco = df.groupby("Produto")["Preço"].transform("median")
df["Quantidade"] = df["Quantidade"].fillna(mediana_qtd).round().astype(int)
df["Preço"]      = df["Preço"].fillna(mediana_preco).round(2)

df.drop_duplicates(inplace=True)
df.reset_index(drop=True, inplace=True)

df["Total_Vendas"] = (df["Quantidade"] * df["Preço"]).round(2)

# --- Salvar ---
df.to_csv("data_clean.csv", index=False)
print("data_clean.csv salvo com sucesso.")

# --- Análise por produto ---
vendas_por_produto = (
    df.groupby("Produto")["Total_Vendas"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)
print(vendas_por_produto.to_string(index=False))

campeao = vendas_por_produto.iloc[0]
print(f"\nProduto com maior volume de vendas: {campeao['Produto']} — R$ {campeao['Total_Vendas']:,.2f}")
