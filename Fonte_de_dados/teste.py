import fitz
import re

ARQUIVO_PDF = "pdf/espelho/Espelho_SIOP_sem_metas.pdf"  # ajuste se necessário
doc = fitz.open(ARQUIVO_PDF)

# Extrai o texto de todas as páginas
texto = "".join(page.get_text("text") for page in doc)

# Remove cabeçalho repetido do Ministério
cabecalho_repetido = (
    "Ministério do Planejamento e Orçamento\n"
    "Mapeamento de Programas Integrantes do\n"
    "Plano Plurianual 2024-2027\n"
    "Secretaria Nacional de Planejamento"
)
texto = texto.replace(cabecalho_repetido, "")


print(f"texto {texto[:500]}")

blocos = re.split(r"\nPrograma\n", texto)
print(f"quantidade de blocos {len(blocos)}")

for i, bloco in enumerate(blocos):
    print(f"🔹 Bloco {i+1}: {bloco[:100]!r}")
