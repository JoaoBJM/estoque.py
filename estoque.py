import pandas as pd
import numpy as np
import networkx as nx

# Read CSV
def load_data(file_path):
    return pd.read_csv(file_path)

# 1. Estoque
def exibir_dados_estoque(df):
    print("Exibindo Dados de Estoque...")
    estoque_df = df[['Centro_Distribuicao', 'Capacidade_Caminhao_kg', 'Carga_kg', 'Prazo_Entrega_dias']].copy()
    estoque_df.columns = ['local', 'capacidade_max', 'nivel_estoque', 'lead_time']
    estoque_df['custo_armazenagem'] = np.round(np.random.uniform(0.5, 2.5, size=len(estoque_df)), 2)
    estoque_df['ruptura'] = (estoque_df['nivel_estoque'] < 1000).astype(int)
    print(estoque_df.head(), "\n")

# 2. Transportes
def exibir_dados_transportes(df):
    print("Exibindo Dados de Transportes...")
    transporte_df = df[['ID_Entrega', 'Centro_Distribuicao', 'Cidade_Destino', 'Estado_Destino',
                        'Distancia_km', 'Prazo_Entrega_dias', 'Capacidade_Caminhao_kg', 'Carga_kg', 'Status_Entrega']].copy()
    transporte_df.columns = ['entrega_id', 'origem', 'destino_cidade', 'destino_estado',
                             'distancia_km', 'prazo_dias', 'capacidade_kg', 'carga_kg', 'status']
    print(transporte_df.head(), "\n")

# 3. Pedidos
def exibir_dados_pedidos(df):
    print("Exibindo Dados de Pedidos...")
    pedidos_df = df[['ID_Entrega', 'Centro_Distribuicao', 'Estado_Destino', 'Data_Entrega']].copy()
    pedidos_df.columns = ['pedido_id', 'local_cd', 'cliente_uf', 'entrega']
    print(pedidos_df.head(), "\n")

# 4. Centros de Distribuição
def exibir_dados_centros_distribuicao(df):
    print("Exibindo Dados de Centros de Distribuição...")
    centros = df.groupby('Centro_Distribuicao').agg({
        'Capacidade_Caminhao_kg': 'mean',
        'Prazo_Entrega_dias': 'mean'
    }).reset_index()
    centros.columns = ['cd', 'capacidade_media', 'tempo_medio_entrega']
    centros['custo_operacional_mensal'] = np.random.randint(50000, 70000, size=len(centros))
    centros['performance_operacional'] = np.random.choice([90, 92, 95, 97, 98], size=len(centros))
    print(centros.head(), "\n")

# 5. Dados Contextuais
def exibir_dados_contextuais(df):
    print("Exibindo Problemas...")
    eventos = ['Chuva', 'Feriado', 'Greve', 'Normal']
    impactos = [10, 20, 30, 40, 50]
    
    contextual_data = df.apply(lambda x: [
        x['Data_Entrega'], 
        x['Centro_Distribuicao'], 
        np.random.choice(eventos), 
        np.random.choice(impactos)
    ], axis=1)
    
    contextual_df = pd.DataFrame(contextual_data.tolist(), columns=['data', 'local', 'evento', 'impacto_estimado'])
    print(contextual_df.head(), "\n")

# Function to identify bottlenecks
def identificar_gargalos(df):
    return df.groupby('etapa')['tempo_espera'].mean().sort_values(ascending=False)

# Example of usage
def main():
    arquivo_csv = 'entregas_datalog_amplo.csv'
    df = load_data(arquivo_csv)
    
    exibir_dados_estoque(df)
    exibir_dados_transportes(df)
    exibir_dados_pedidos(df)
    exibir_dados_centros_distribuicao(df)
    exibir_dados_contextuais(df)

    dados_processo = pd.DataFrame({
        'etapa': ['recebimento', 'armazenagem', 'expedicao'],
        'tempo_espera': [5, 10, 15]  # in hours
    })

    gargalos = identificar_gargalos(dados_processo)
    print("Gargalos identificados:\n", gargalos)

    # Route Optimization
    def otimizar_rotas(grafo, origem, destino):
        caminho = nx.dijkstra_path(grafo, origem, destino)
        custo = nx.path_weight(grafo, caminho, weight='peso')
        return caminho, custo

    grafo = nx.Graph()
    grafo.add_edge('A', 'B', peso=1)
    grafo.add_edge('A', 'C', peso=4)
    grafo.add_edge('B', 'C', peso=2)
    grafo.add_edge('B', 'D', peso=5)
    grafo.add_edge('C', 'D', peso=1)

    caminho, custo = otimizar_rotas(grafo, 'A', 'D')
    print(f"Caminho: {caminho}, Custo: {custo}")
  


if __name__ == '__main__':
    main()
