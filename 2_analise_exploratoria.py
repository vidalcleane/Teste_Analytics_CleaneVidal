import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

# --- Carregar dados ---
df = pd.read_csv("data_clean.csv", parse_dates=["Data"])
df["Mes_num"]  = df["Data"].dt.month
df["Nome_Mes"] = df["Data"].dt.strftime("%b")

# --- Paleta Quod ---
CORES_QUOD = {
    "Quod Score PF":        "#00B4D8",
    "Quod Score PJ":        "#0077B6",
    "Quod X Antifraude":    "#023E8A",
    "Cadastro Positivo":    "#48CAE4",
    "Cobrança as a Service":"#ADE8F4",
    "Quod Identity":        "#90E0EF",
}
AZUL   = "#0077B6"
ESCURO = "#023E8A"

# --- Figura ---
fig = plt.figure(figsize=(18, 14), facecolor="#F8FBFF")
fig.suptitle("Dashboard de Vendas — Produtos Quod | 2023",
             fontsize=20, fontweight="bold", color=ESCURO, y=0.98)
gs = fig.add_gridspec(3, 2, hspace=0.45, wspace=0.35,
                      left=0.07, right=0.95, top=0.93, bottom=0.06)

# --- Gráfico 1: Tendência mensal (linha) ---
ax1 = fig.add_subplot(gs[0, :])

vendas_mensais = (
    df.groupby(["Mes_num", "Nome_Mes"])["Total_Vendas"]
    .sum()
    .reset_index()
    .sort_values("Mes_num")
)

ax1.plot(vendas_mensais["Nome_Mes"], vendas_mensais["Total_Vendas"],
         marker="o", linewidth=2.5, markersize=9,
         color=AZUL, markerfacecolor=ESCURO,
         markeredgewidth=1.5, markeredgecolor="white", zorder=5)
ax1.fill_between(range(len(vendas_mensais)), vendas_mensais["Total_Vendas"],
                 alpha=0.12, color=AZUL)

pico_idx = vendas_mensais["Total_Vendas"].idxmax()
pico_mes = vendas_mensais.loc[pico_idx, "Nome_Mes"]
pico_val = vendas_mensais.loc[pico_idx, "Total_Vendas"]
ax1.annotate(f"Pico: R$ {pico_val:,.0f}",
             xy=(vendas_mensais["Nome_Mes"].tolist().index(pico_mes), pico_val),
             xytext=(0, 18), textcoords="offset points",
             ha="center", fontsize=9.5, color=ESCURO, fontweight="bold",
             arrowprops=dict(arrowstyle="-", color=ESCURO, lw=1.2))

ax1.set_title("Tendência de Vendas Mensais — Total (R$)", fontsize=13,
              fontweight="bold", color=ESCURO, pad=10)
ax1.set_ylabel("Total de Vendas (R$)", fontsize=10)
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"R$ {x/1000:.0f}k"))
ax1.set_facecolor("#F0F7FF")
ax1.grid(axis="y", linestyle="--", alpha=0.4, color=AZUL)
for spine in ax1.spines.values():
    spine.set_visible(False)

# --- Gráfico 2: Receita por produto (barras) ---
ax2 = fig.add_subplot(gs[1, 0])

receita_prod = df.groupby("Produto")["Total_Vendas"].sum().sort_values().reset_index()
cores_barras = [CORES_QUOD[p] for p in receita_prod["Produto"]]

bars = ax2.barh(receita_prod["Produto"], receita_prod["Total_Vendas"],
                color=cores_barras, edgecolor="white", height=0.65)
for bar, val in zip(bars, receita_prod["Total_Vendas"]):
    ax2.text(val + 2000, bar.get_y() + bar.get_height() / 2,
             f"R$ {val/1000:.0f}k", va="center", fontsize=8.5, color=ESCURO)

ax2.set_title("Receita Total por Produto", fontsize=12, fontweight="bold", color=ESCURO)
ax2.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"R$ {x/1000:.0f}k"))
ax2.set_facecolor("#F0F7FF")
ax2.grid(axis="x", linestyle="--", alpha=0.35, color=AZUL)
for spine in ax2.spines.values():
    spine.set_visible(False)

# --- Gráfico 3: Participação por categoria (pizza) ---
ax3 = fig.add_subplot(gs[1, 1])

receita_cat = df.groupby("Categoria")["Total_Vendas"].sum()
CORES_CAT   = {"Análise de Crédito": AZUL,
               "Prevenção a Fraude": ESCURO,
               "Cobrança":           "#48CAE4"}
cores_cat = [CORES_CAT[c] for c in receita_cat.index]

wedges, texts, autotexts = ax3.pie(
    receita_cat, labels=receita_cat.index,
    autopct="%1.1f%%", colors=cores_cat,
    startangle=90, pctdistance=0.75,
    wedgeprops=dict(edgecolor="white", linewidth=2)
)
for at in autotexts:
    at.set_fontsize(9.5)
    at.set_color("white")
    at.set_fontweight("bold")
ax3.set_title("Receita por Categoria", fontsize=12, fontweight="bold", color=ESCURO)

# --- Gráfico 4: Heatmap produto x mês ---
ax4 = fig.add_subplot(gs[2, :])

pivot = (
    df.groupby(["Produto", df["Data"].dt.month])["Total_Vendas"]
    .sum()
    .unstack(fill_value=0)
)
pivot.columns = ["Jan","Fev","Mar","Abr","Mai","Jun",
                 "Jul","Ago","Set","Out","Nov","Dez"]

sns.heatmap(pivot, ax=ax4, cmap="YlGnBu", fmt=".0f",
            annot=True, linewidths=0.5, linecolor="white",
            cbar_kws={"label": "R$"}, annot_kws={"size": 8})
ax4.set_title("Receita por Produto e Mês — Heatmap (R$)", fontsize=12,
              fontweight="bold", color=ESCURO, pad=10)
ax4.set_xlabel("")
ax4.set_ylabel("")
ax4.tick_params(colors="#444", labelsize=8.5, rotation=0)

# --- Salvar ---
plt.savefig("graficos_vendas.png", dpi=150, bbox_inches="tight",
            facecolor=fig.get_facecolor())
print("graficos_vendas.png salvo com sucesso.")

# --- Insights ---
vendas_q4     = df[df["Data"].dt.quarter == 4]["Total_Vendas"].sum()
vendas_outros = df[df["Data"].dt.quarter != 4]["Total_Vendas"].sum() / 3
print(f"\nInsight 1 — Sazonalidade Q4: +{((vendas_q4/vendas_outros)-1)*100:.1f}% acima da média trimestral")

top_receita = df.groupby("Produto")["Total_Vendas"].sum().idxmax()
top_volume  = df.groupby("Produto")["Quantidade"].sum().idxmax()
print(f"Insight 2 — Maior receita: {top_receita} | Maior volume: {top_volume}")

setor_top = df.groupby("Setor_Cliente")["Total_Vendas"].sum().idxmax()
print(f"Insight 3 — Setor líder em receita: {setor_top}")
