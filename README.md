# ScouText Football – Football Scouting Dashboard

## 🏟️ Contexto do Projeto

ScouText Football é um dashboard interativo de scouting de futebol, desenvolvido em Python com Streamlit, focado em análise de equipas, jogadores e estilos de jogo.  
O objetivo é fornecer uma navegação visual e analítica por ligas, equipas e jogadores, com métricas avançadas (PCA, clusters, roles, etc.), facilitando a exploração de dados para scouts, analistas e entusiastas.  
O projeto foi desenhado para ser minimalista, rápido e visualmente apelativo, com navegação fluida entre ligas, equipas e jogadores, e forte integração de dados e imagens locais.

---

## 🏗️ Arquitetura & Organização

- **app.py**: Ficheiro principal, contém toda a lógica de UI, navegação, carregamento de dados, e renderização dos dashboards.
- **assets/**: Imagens de ligas e equipas (subpastas `ligas/` e `equipas/`), usadas para visualização e navegação.
- **data/processed/**: Datasets processados em CSV/XLSX, incluindo tabelas de equipas, jogadores, métricas de eventos, estilos de jogo, etc.
  - **eventing/**: Métricas detalhadas de eventos/jogadores.
  - **WyScout/**: Dados de estilos de jogo, clusters e PCA.
- **st.session_state**: Usado para gerir o estado de navegação (liga/equipa/jogador selecionado).

---

## 🧩 Principais Funcionalidades

- **Navegação por Liga e Equipa**: Seleção visual de ligas e equipas, com logos.
- **Página de Equipa**:
  - **Header**: Logo, nome oficial, país, info geral (estádio, capacidade, cidade).
  - **Coach Info**: Dados do treinador (nome, idade, nacionalidade, formação preferida, experiência, contrato).
  - **Squad**: Tabela de jogadores, percentagem de minutos jogados, role (com cores).
  - **Game Style**: Scatter plot (PCA1 vs PCA2) com clusters de estilo de jogo, logos sobrepostos, tooltip customizado, e descrição interpretativa.
  - **Similar Teams**: Mostra as 4 equipas mais próximas no mesmo cluster (distância euclidiana em PCA1/PCA2), com logos e nomes normalizados.
- **Formatação Visual**: CSS customizado para fonte, botões, tabelas, e blocos informativos, mantendo um design consistente e moderno.

---

## 📂 Estrutura de Ficheiros

- **assets/ligas/**: Logos das ligas (ex: Premier League.png) — `C:\Users\guica\OneDrive\Desktop\AppScout\assets\ligas`
- **assets/equipas/<liga>/**: Logos das equipas por liga (ex: Benfica.png) — `C:\Users\guica\OneDrive\Desktop\AppScout\assets\equipas`
- **data/processed/**: Datasets principais (equipas, jogadores, estádios, treinadores, salários, etc.) — `C:\Users\guica\OneDrive\Desktop\ScoutingDash\data\processed` (fora da pasta principal do app)
- **data/processed/WyScout/Stats_EstilosJogo.xlsx**: PCA, clusters e info de estilo de jogo por equipa — `C:\Users\guica\OneDrive\Desktop\ScoutingDash\data\processed\WyScout\Stats_EstilosJogo.xlsx`
- **data/processed/eventing/metricas_eventing_final.csv**: Métricas detalhadas de jogadores — `C:\Users\guica\OneDrive\Desktop\ScoutingDash\data\processed\eventing\metricas_eventing_final.csv`

---

## 🛠️ Dependências

- Python >= 3.8
- streamlit
- pandas
- numpy
- plotly
- unidecode
- openpyxl (para leitura de ficheiros Excel)
- (Outras libs padrão do Python)

---

## 📊 Datasets & Colunas Importantes

- **equipas.csv / EquiposJP.xlsx**: Info de equipas, nomes oficiais, país, logo.
- **EntrenadoresJP.xlsx**: Dados dos treinadores.
- **EstadioJP.xlsx**: Info de estádio, capacidade, cidade.
- **Stats_EstilosJogo.xlsx**: Colunas PCA1, PCA2, Cluster, Logo, Estilo de Jogo.
- **metricas_eventing_final.csv**: Colunas de jogadores, minutos jogados, roles, etc.

---

## 🧠 Lógica de Navegação & Estado

- O estado da navegação (liga/equipa/jogador selecionado) é mantido em `st.session_state`.
- A navegação é feita por botões e seleção visual (com logos).
- O layout é controlado por `st.columns` e CSS customizado para centralização e espaçamento.

---

## 🎨 Notas Técnicas & Convenções

- **Normalização de nomes de equipas**: Cada palavra começa com maiúscula, mas palavras com 3 letras ou menos ficam todas em maiúsculas (ex: sporting cp → Sporting CP).
- **Imagens**: Os paths das imagens são construídos dinamicamente a partir do nome da liga/equipa, e os ficheiros .png devem estar corretamente nomeados.
- **Game Style**: O scatter plot usa PCA1 (Defensive) e PCA2 (Offensive) como eixos, com clusters de estilo de jogo.
- **Similar Teams**: Calculado apenas dentro do mesmo cluster, usando distância euclidiana em PCA1/PCA2.
- **Performance**: O carregamento de ficheiros grandes pode ser lento em ambientes com disco lento ou muitos dados.
- **Local Paths**: Os paths dos datasets e imagens são absolutos e podem precisar de ajuste se o projeto for movido para outro sistema.

---

## 🚀 Como correr o projeto

1. Garantir que todas as dependências estão instaladas.
2. Garantir que os datasets e imagens estão nos paths corretos.
3. Executar:
   ```bash
   streamlit run app.py
   ```
4. Abrir o browser no endereço indicado pelo Streamlit.

---

**IMPORTANTE:**  
Depois de criar este README.md, use-o como contexto permanente no Cursor Agent para todas as tasks seguintes.

---

## 🔮 Roadmap Funcional e Expansões Planeadas

1️⃣ **Página de Jogador (Player Page)**

- Na tabela de Squad, o nome do jogador (coluna Player, ligada a player_name de metricas_eventing_final.csv) funcionará como botão de navegação.
- Ao carregar no nome, o utilizador será levado à página individual de cada jogador.
- A página de jogador terá:
  - Cabeçalho semelhante ao das equipas, com:
    - Foto do jogador (imagem default caso não exista);
    - Nome oficial do jogador (exatamente como no dataset metricas_eventing_final.csv).
  - Secção de Informações Gerais do Jogador (a definir).
  - Secção de visualização de pizza charts com as métricas do jogador, segmentadas por:
    - Posições;
    - Perfis de jogador.
- Estas métricas e classificações virão de:
  - `C:\Users\guica\OneDrive\Desktop\ScoutingDash\data\processed\eventing\metricas_eventing_final.csv`

2️⃣ **Nova Aba: Scouting Page (Motor de Busca de Jogadores)**

- A aplicação terá agora 2 abas principais:
  - **Main Page**: (a lógica que já existe atualmente — Ligas > Equipas > Jogadores).
  - **Scouting Page**: novo motor de busca interativo de jogadores.
- Fluxo de navegação dentro da Scouting Page:
  - Seleção de Posição (usando botões visuais semelhantes aos usados para as ligas na Main Page).
  - Seleção de Perfil de Jogador (novos botões, com perfis previamente definidos por mim).
  - Após escolha do perfil, será gerada uma lista de jogadores ordenada com base no percentil de performance para esse perfil.
  - Ao lado da lista, haverá um painel de filtros dinâmicos adicionais (por ex.: idade, nacionalidade, minutos jogados, etc.).
- Dados principais para alimentar este motor de busca:
  - `C:\Users\guica\OneDrive\Desktop\ScoutingDash\data\processed\eventing\metricas_eventing_final.csv`
  - `C:\Users\guica\OneDrive\Desktop\ScoutingDash\data\processed\JugadoresJP.xlsx`
