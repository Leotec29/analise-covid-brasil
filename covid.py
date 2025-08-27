import pandas as pd
from sqlalchemy import create_engine, text
import matplotlib.pyplot as plt
import seaborn as sns

# ----------------------------
# CONFIGURAÇÃO DO MYSQL
# ----------------------------
usuario = 'root'
senha = ''
host = 'localhost'
banco = 'covid_db'

engine = create_engine(f'mysql+mysqlconnector://{usuario}:{senha}@{host}/{banco}')

# ----------------------------
# LEITURA DO CSV
# ----------------------------
caminho_csv = r"C:\Users\leona\OneDrive\Documentos\Analise de Dados e Big Data 2\caso_full.csv.gz"

colunas = [
    'city', 
    'city_ibge_code', 
    'date', 
    'last_available_confirmed', 
    'last_available_deaths', 
    'estimated_population_2019'
]

print("⌛ Lendo o CSV...")
df = pd.read_csv(caminho_csv, compression='gzip', usecols=colunas, encoding='utf-8')
print(f"✅ CSV carregado com {len(df)} linhas")

# ----------------------------
# LIMPEZA DOS DADOS
# ----------------------------
df = df.dropna(subset=['city', 'city_ibge_code', 'date'])
df['city_ibge_code'] = df['city_ibge_code'].astype(int)
df['last_available_confirmed'] = df['last_available_confirmed'].fillna(0).astype(int)
df['last_available_deaths'] = df['last_available_deaths'].fillna(0).astype(int)
df['estimated_population_2019'] = df['estimated_population_2019'].fillna(0).astype(int)
df['date'] = pd.to_datetime(df['date'])
print("✅ Dados limpos e tipos ajustados")


# ----------------------------
# LIMPAR TABELA ANTES DE INSERIR
# ----------------------------
with engine.connect() as conn:
    if engine.dialect.has_table(conn, "covid_city"):
        conn.execute(text("TRUNCATE TABLE covid_city"))
        print("🗑 Tabela 'covid_city' limpa antes da inserção")

# ----------------------------
# INSERÇÃO EM BLOCOS NO MYSQL
# ----------------------------
tamanho_bloco = 10000
for i, inicio in enumerate(range(0, len(df), tamanho_bloco)):
    fim = inicio + tamanho_bloco
    bloco = df.iloc[inicio:fim]
    try:
        with engine.begin() as conn:
            bloco.to_sql('covid_city', con=conn, if_exists='append', index=False)
        print(f"✅ Bloco {i+1} inserido: linhas {inicio} a {fim-1}")
    except Exception as e:
        print(f"❌ Erro no bloco {i+1}: {e}")

print("🎉 Todos os dados foram inseridos no MySQL com sucesso!")

# ----------------------------
# RELATÓRIOS
# ----------------------------
df_mysql = pd.read_sql('SELECT * FROM covid_city', con=engine)

# 1️⃣ Todos os casos de morte por cidade
mortes_por_cidade = df_mysql.groupby('city')['last_available_deaths'].sum().sort_values(ascending=False)
print("\n💀 Casos de morte por cidade (Top 10):")
print(mortes_por_cidade.head(10))

# Gráfico mortes
plt.figure(figsize=(12,6))
sns.barplot(x=mortes_por_cidade.head(10).values, y=mortes_por_cidade.head(10).index, palette="Reds_r")
plt.title("Top 10 cidades por mortes COVID")
plt.xlabel("Número de mortes")
plt.ylabel("Cidade")
plt.show()

# 2️⃣ População estimada antes e depois dos casos para todas as cidades
populacao = df_mysql.groupby('city')[['estimated_population_2019', 'last_available_confirmed']].sum()
populacao['pop_apos_casos'] = populacao['estimated_population_2019'] - populacao['last_available_confirmed']
print("\n👥 População estimada antes e depois dos casos (Top 10 cidades):")
print(populacao.head(10))

print("📊 Verificando dados de entrada:")
print(df_mysql[['city', 'estimated_population_2019', 'last_available_confirmed']].dropna().head(10))
print(f"Total de linhas após dropna: {len(df_mysql[['city', 'estimated_population_2019', 'last_available_confirmed']].dropna())}")


# Gráfico população vs casos (Top 10)
top10_pop = populacao.sort_values('estimated_population_2019', ascending=False).head(10)
plt.figure(figsize=(12,6))
sns.barplot(x=top10_pop['estimated_population_2019'], y=top10_pop.index, palette="Blues_r", label="População")
sns.barplot(x=top10_pop['pop_apos_casos'], y=top10_pop.index, palette="Greens_r", label="População após casos")
plt.title("Top 10 cidades: População antes e depois dos casos")
plt.xlabel("População")
plt.ylabel("Cidade")
plt.legend()
plt.show()

# 3️⃣ Cidade com maior quantidade de casos
maior_cidade = df_mysql.groupby('city')['last_available_confirmed'].sum().idxmax()
quant_maior = df_mysql.groupby('city')['last_available_confirmed'].sum().max()
print(f"\n🏙 Cidade com maior quantidade de casos: {maior_cidade} ({quant_maior} casos)")

# 4️⃣ Cidade com menor quantidade de casos (com pelo menos 1 caso)
df_com_casos = df_mysql[df_mysql['last_available_confirmed'] > 0]
menor_cidade = df_com_casos.groupby('city')['last_available_confirmed'].sum().idxmin()
quant_menor = df_com_casos.groupby('city')['last_available_confirmed'].sum().min()
print(f"🏘 Cidade com menor quantidade de casos: {menor_cidade} ({quant_menor} casos)")

# Gráfico maior e menor cidade em casos
plt.figure(figsize=(8,4))
sns.barplot(x=[quant_maior, quant_menor], y=[maior_cidade, menor_cidade], palette=["green","orange"])
plt.title("Cidade com maior e menor quantidade de casos")
plt.xlabel("Número de casos")
plt.ylabel("Cidade")
plt.show()