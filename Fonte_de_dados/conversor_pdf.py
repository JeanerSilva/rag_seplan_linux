import os
import json
import uuid
import re
import argparse
from collections import defaultdict
import fitz  # PyMuPDF

# Argumentos
parser = argparse.ArgumentParser(description="Extrai blocos estruturados do Espelho SIOP.")
parser.add_argument("arquivo_pdf", help="Caminho do arquivo PDF Espelho SIOP")
args = parser.parse_args()

ARQUIVO_PDF = args.arquivo_pdf
PASTA_SAIDA = "chunks"
ARQUIVO_SAIDA = os.path.join(PASTA_SAIDA, "espelho_siop_chunks.jsonl")
os.makedirs(PASTA_SAIDA, exist_ok=True)

# Categorias esperadas
CATEGORIAS = [
    "orgao", "tipo_programa", "objetivos_estrategicos", "publico_alvo",
    "problema", "causas_problema", "evidencias_problema", "justificativa",
    "evolucao_historica", "comparacoes_internacionais", "relacoes_ods",
    "agentes_envolvidos", "articulacao_federativa", "enfoque_transversal",
    "marco_legal", "planos_nacionais", "objetivo_geral", "objetivos_especificos",
    "orgaos_responsaveis", "entregas"
]

# Mapeamento de regex para cada categoria
PADROES = {cat: re.compile(cat.replace("_", " ").replace("planos", "planos nacionais, setoriais e regionais") + r":\s*((?:.|\n)+?)(?=\n[A-Z][^:\n]*:|$)", re.IGNORECASE) for cat in CATEGORIAS}

# Abrir PDF e extrair texto limpo
doc = fitz.open(ARQUIVO_PDF)
texto = "\n".join([page.get_text("text") for page in doc])

# Separar por programa
blocos = re.split(r"(?:^|\n)PROGRAMA:\s*(\d{4})\s*-\s*(.+?)(?=\n[A-Z][^:\n]*:)", texto)

chunks = []

for i in range(1, len(blocos), 3):
    programa_id = blocos[i].strip()
    nome_programa = blocos[i + 1].strip()
    conteudo = blocos[i + 2]

    header = f"PROGRAMA: {programa_id} - {nome_programa}"

    for categoria, padrao in PADROES.items():
        match = padrao.search(conteudo)
        if match:
            texto_categoria = match.group(1).strip()
            chunk_text = f"{header}\n\n{categoria.replace('_', ' ').title()}:\n{texto_categoria}"
            chunks.append({
                "text": f"<|start_header_id|>\n{chunk_text}\n<|end_header_id|>",
                "metadata": {
                    "origem": os.path.basename(ARQUIVO_PDF),
                    "categoria": categoria,
                    "programa_id": programa_id,
                    "chunk_id": str(uuid.uuid4())
                }
            })

print(f"✂️ {len(chunks)} chunks gerados de {ARQUIVO_PDF}")

# Salvar JSONL
with open(ARQUIVO_SAIDA, "w", encoding="utf-8") as f:
    for chunk in chunks:
        f.write(json.dumps(chunk, ensure_ascii=False) + "\n")

print(f"✅ Arquivo salvo em: {ARQUIVO_SAIDA}")
