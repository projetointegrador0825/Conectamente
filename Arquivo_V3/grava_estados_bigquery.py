# %%
import pandas as pd
from google.cloud import storage
from google.cloud import bigquery
import io
import sys

# %%
def ler_excel_do_gcs(bucket_name, arquivo_path):
    """
    Lê arquivo Excel do Google Cloud Storage.
    
    Args:
        bucket_name (str): Nome do bucket (ex: dados_ibge_sm)
        arquivo_path (str): Caminho do arquivo dentro do bucket (ex: capitais.xlsx)
    
    Returns:
        pd.DataFrame: DataFrame com os dados do Excel
    """
    try:
        # Criar cliente do GCS
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(arquivo_path)
        
        # Baixar arquivo em memória
        print(f"📥 Lendo arquivo do GCS: gs://{bucket_name}/{arquivo_path}")
        arquivo_bytes = blob.download_as_bytes()
        
        # Ler Excel usando pandas
        df = pd.read_excel(io.BytesIO(arquivo_bytes))
        
        #print(f"✓ Arquivo lido com sucesso: {len(df)} linhas, {len(df.columns)} colunas")
        #print(f"  Colunas: {', '.join(df.columns)}")
        
        return df
    
    except Exception as e:
        print(f"✗ Erro ao ler arquivo do GCS: {e}")
        sys.exit(1)

def gravar_no_bigquery(df, projeto_id, dataset_id, tabela_id, if_exists="replace"):
    """
    Escreve DataFrame no BigQuery.
    
    Args:
        df (pd.DataFrame): DataFrame a escrever
        projeto_id (str): ID do projeto GCP
        dataset_id (str): ID do dataset BigQuery
        tabela_id (str): ID da tabela BigQuery
        if_exists (str): Ação se tabela existe: "fail", "replace", "append"
    
    Returns:
        bool: True se sucesso, False se erro
    """
    try:
        # Criar cliente BigQuery
        bq_client = bigquery.Client(project=projeto_id)
        
        # Construir ID da tabela
        tabela_completa = f"{projeto_id}.{dataset_id}.{tabela_id}"
        
        print(f"\n📤 Gravando dados no BigQuery: {tabela_completa}")
        print(f"  Modo: {if_exists}")
        
        # Configurar job de escrita
        job_config = bigquery.LoadJobConfig(
            write_disposition={
                "replace": bigquery.WriteDisposition.WRITE_TRUNCATE,
                "append": bigquery.WriteDisposition.WRITE_APPEND,
                "fail": bigquery.WriteDisposition.WRITE_EMPTY
            }.get(if_exists, bigquery.WriteDisposition.WRITE_TRUNCATE)
        )
        
        # Escrever dados
        job = bq_client.load_table_from_dataframe(
            df,
            tabela_completa,
            job_config=job_config
        )
        
        # Aguardar conclusão
        job.result()
        
        print(f"✓ Dados gravados com sucesso!")
        print(f"  Linhas: {len(df)}")
        print(f"  Colunas: {len(df.columns)}")
        
        return True
    
    except Exception as e:
        print(f"✗ Erro ao gravar no BigQuery: {e}")
        return False

# %%
"""
Função principal do script.
"""
print("=" * 60)
print("Ler Excel do GCS e Gravar no BigQuery")
print("=" * 60)

# Configurações
bucket_name = "ibge_sm"
arquivo_path = "estados.xlsx"
projeto_id = "projeto-integrador-sm"  # ALTERAR para seu projeto
dataset_id = "dados_ibge"      # ALTERAR para seu dataset
tabela_id = "estados"          # ALTERAR se necessário

print(f"\n📋 Configurações:")
print(f"  Bucket GCS: {bucket_name}")
print(f"  Arquivo: {arquivo_path}")
print(f"  Projeto: {projeto_id}")
print(f"  Dataset: {dataset_id}")
print(f"  Tabela: {tabela_id}")

# Ler arquivo do GCS
df = ler_excel_do_gcs(bucket_name, arquivo_path)

# Mostrar preview dos dados
#print(f"\n📊 Preview dos dados:")
#print(df.head())

 # Gravar no BigQuery
if gravar_no_bigquery(df, projeto_id, dataset_id, tabela_id, if_exists="replace"):
    print("\n✓ Script executado com sucesso!")
else:
    print("\n✗ Script finalizado com erro!")
    sys.exit(1)

# %%



