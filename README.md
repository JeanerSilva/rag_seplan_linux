# PPA inteligente

## Uso de RAG para análise do PPA


### Sumário Executivo 

O projeto PPA Inteligente visa modernizar o ciclo de planejamento governamental por meio da incorporação de Inteligência Artificial (IA) ao Plano Plurianual (PPA). A iniciativa prevê o desenvolvimento de soluções baseadas em modelos de linguagem e recuperação de informações (RAG), com foco na melhoria do acesso, análise e utilização do PPA por diferentes públicos, por meio da entrega dos seguintes produtos:
1.	Assistente Virtual para Consultas Internas ao PPA
Ferramenta interativa voltada a técnicos e gestores públicos, capaz de responder perguntas sobre metas, programas, vínculos orçamentários e diretrizes do PPA, com base em documentos oficiais e atualizados.
2.	Assistente Virtual para Apoio à Leitura dos Manuais do PPA
Solução de atendimento inteligente voltada ao público externo (sociedade civil, universidades, órgãos de controle) e também a usuários internos, facilitando a compreensão das orientações metodológicas e operacionais dos manuais.
3.	Módulo de Análise Automatizada do PPA com IA
Sistema de análise que utiliza inteligência artificial para identificar padrões, inconsistências e oportunidades de melhoria nos dados do PPA, contribuindo para o aperfeiçoamento contínuo do planejamento estratégico federal.
4.	Relatórios Automatizados de Apoio à Tomada de Decisão
Geração de relatórios explicativos e visualizações que consolidam achados da IA sobre lacunas, sinergias e sugestões de ajustes no planejamento, de forma transparente e acessível.

### Etapas e Metodologia
A entrega dos produtos será realizada em quatro fases: diagnóstico e levantamento de dados, prova de conceito, desenvolvimento técnico e testes, e implantação com capacitação de usuários. A metodologia adotada envolve o uso de LLMs, técnicas de RAG, bancos vetoriais e validação contínua por especialistas.

### Resultados Esperados
- Redução do tempo de resposta a dúvidas técnicas sobre o PPA e os sistemas relativos;
- Aumento do uso qualificado dos documentos de planejamento;
- Aprimoramento da análise técnica de metas e programas;
- Ampliação da transparência e da participação social no planejamento público.


## Funcionamento

### Executar o programa
```sh
streamlit run .\app.py
```

## Modelo de uso

As fases de processamento seguem o seguinte padrão:

1. Preparação dos fontes de dados para servirem ao RAG.

Na pasta Fonte_de_dados existem pastas com arquivos PDF e XLS que podem ser usados.
Além disso, foi criado um conversor para o anexo do PPA, com vistas a extrair os programas, objetivos gerais, estratégicos, específicos e público alvo.
O conversor está sendo usado para pegar o arquivo anexo-iii-programas-finalisticos na Fonte_de_dados/pdf/programas, mas um dia deve ser criado um arquivo específico gerado a partir da extração de dados diretamente do SIOP, com vistas a ter uma única fonte confiável de dados.

Para tal existe o script A3_gerar_jsonl_do_anexo_III.py, que executa os outros2 para tal.

Além dos programas, há pastas com normas, guias e as agendas.
Para tal deve-se criar categorias específicas na função def "detectar_categoria(texto):", com vistas a deixar o RAG mais especializado. 

Nesse caso, deve-se executar os scripts conversor_pdf.py e conversor_xls.py. Essa situação também é intermediaria, pois elas podem ser incorporadas na função de upload.

No final do processo são gerados arquivos jsonl (json em uma linha) com o conteúdo gerado, categorizado e com tags de STOP para o modelo E5.

2. Embedding dos dados

É feito por meio da UI no botão Reindexar agora, a partir da seleção do modelo (E5, BGE ou MiniLM).
O E5 é o mais robusto e específico. O BGE e intermediário.

Nesse caso, são pegos os arquivo jsonl criados na fase anterior e criados os bancos de dados FAISS, que serão usados para envio junto com a pergunta na LLM.
O RAG, portanto, pega a pergunta, e seleciona os k chunks (parâmetro definido nas configurações ou na UI) e envia junto com a pergunta.

Após feito o embedding deve-se criar pastas na pasta vectors/modelos com cada um em separadao, para que seja possível escolher qual deles na tela principal.
O processo precisa ser automatizado também.

3. Pergunta à LLM
- Reranker: antes de envio da pergunta é feito um processo de ranqueamento, em que a LLM reordena os chunks com base na importância.
- Pergunta: existem prompts salvos e usuário pode criar mais.


## Configurações

### Chunks

O tamanho dos chunks é essencial para a configuração e deve estar alinhado com os parâmetros de LIMITE_CARACTERES do conversor_pdf.py.

### Ollama
Para saber quais as propriedades do Ollama
```sh
ollama show llama3.2
```

No caso do llama3.2 temos:

- Parâmetros: 3.2 bilhões (3.2B)
- Janela de contexto: 128k
- Embedding length:	3072 tokens
- Quantização:Q4_K_M


📊
✅ 
⚠️ 
📌 
📝 
❌ 

### Torch com cuda
```sh
pip uninstall torch -y
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

✅ 1. Streamlit (sua aplicação RAG)
URL: http://localhost:8501

✅ 2. Ollama (servidor da LLM)
API: http://localhost:11434
curl http://localhost:11434/api/tags
curl http://localhost:11434/api/generate -H "Content-Type: application/json" -d '{"model":"llama3.2", "prompt":"Jeaner é feliz?"}'
curl.exe http://localhost:11434/api/generate -H "Content-Type: application/json" -d "{\"model\":\"llama3.2\",\"prompt\":\"Jeaner é feliz?\"}"
curl http://localhost:11434/api/generate -d '{"model":"llama3.2","prompt":"Jeaner é feliz?"}'


‣慲彧敳汰湡江湩硵�