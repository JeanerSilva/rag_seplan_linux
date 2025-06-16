import os
import json
import uuid
import pandas as pd
from tqdm import tqdm

PASTA_CSV = "dados_abertos"
PASTA_SAIDA = "chunks/csv"

os.makedirs(PASTA_SAIDA, exist_ok=True)

arquivos_csv = [f for f in os.listdir(PASTA_CSV) if f.lower().endswith(".csv")]

print(f"📁 Pasta de entrada: {PASTA_CSV}")
print(f"📂 Pasta de saída: {PASTA_SAIDA}")
print("🔄 Iniciando processamento dos arquivos CSV...\n")

def ler_csv_com_separador(caminho):
    """Tenta ler o CSV com diferentes separadores"""
    for sep in [",", ";"]:
        try:
            return pd.read_csv(caminho, sep=sep, encoding='utf-8')
        except Exception:
            try:
                return pd.read_csv(caminho, sep=sep, encoding='latin1')
            except Exception:
                continue
    raise ValueError("Não foi possível ler o arquivo com os separadores padrão.")

for arquivo in tqdm(arquivos_csv, desc="📄 Processando arquivos"):
    caminho_csv = os.path.join(PASTA_CSV, arquivo)

    try:
        df = ler_csv_com_separador(caminho_csv)
        df = df.dropna(how="all").fillna("")

        nome_arquivo = os.path.splitext(arquivo)[0]
        partes = nome_arquivo.split("_")
        ano = next((int(p) for p in reversed(partes) if p.isdigit()), None)
        categoria = " ".join(partes[:-1])

        saida_jsonl = os.path.join(PASTA_SAIDA, f"{nome_arquivo}.jsonl")
        total_chunks = 0

        with open(saida_jsonl, "w", encoding="utf-8") as f_out:
            for _, row in df.iterrows():
                partes_texto = []
                for coluna in df.columns:
                    valor = str(row[coluna]).strip()
                    if valor:
                        partes_texto.append(f"{coluna}: {valor}")
                if not partes_texto:
                    continue

                texto = f"<|start_header_id|> {'; '.join(partes_texto)}<|end_header_id|>"
                metadata = {
                    "origem": arquivo,
                    "categoria": categoria.replace("_", " "),
                    "ano": ano,
                    "chunk_id": str(uuid.uuid4())
                }
                f_out.write(json.dumps({"text": texto, "metadata": metadata}, ensure_ascii=False) + "\n")
                total_chunks += 1

        #print(f"✅ {arquivo}: {total_chunks} linhas convertidas → {saida_jsonl}")

    except Exception as e:
        print(f"❌ Erro ao processar '{arquivo}': {e}")

print("\n🎉 Conversão finalizada com sucesso.")
