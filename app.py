import streamlit as st
import os
import pandas as pd
import mplsoccer

# Importação dos módulos
from scoutext.components.league_selector import render_league_selector
from scoutext.components.team_selector import render_team_selector
from scoutext.components.team_header import render_team_header
from scoutext.components.squad import render_squad
from scoutext.components.game_style import render_game_style
from scoutext.components.similar_teams import render_similar_teams

# Configuração da página
st.set_page_config(page_title='ScouText', page_icon=':soccer:', layout='wide')

# Google Fonts + CSS para fonte Inter bold e ajustes visuais
st.markdown('''
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@700&display=swap" rel="stylesheet">
    <style>
    html, body, [class^="css"]  {
        font-family: 'Inter', Arial, sans-serif !important;
        font-weight: 700 !important;
    }
    .stButton > button, .stTextInput > div > input, .stSelectbox > div, .stMarkdown, .stTitle, .stHeader, .stSubheader {
        font-family: 'Inter', Arial, sans-serif !important;
        font-weight: 700 !important;
        border-radius: 10px;
    }
    .stTitle, .stTitle > h1, h1 {
        margin-bottom: 2.5rem !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px;
    }
    .liga-btn, .equipa-btn {
        background: #fff;
        border: 1px solid #eee;
        border-radius: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        transition: box-shadow 0.2s, transform 0.2s;
        height: 140px;
        width: 100%;
        padding: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        margin-bottom: 10px;
        position: relative;
        font-family: 'Inter', Arial, sans-serif !important;
        font-weight: 700 !important;
    }
    .liga-btn:hover, .equipa-btn:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.12);
        transform: translateY(-4px) scale(1.04);
        background: #f5f5f5;
    }
    .liga-img-btn, .equipa-img-btn {
        height: 80px;
        width: auto;
        object-fit: contain;
        display: block;
        margin: 0 auto;
    }
    .top-btn {
        width: 100%;
        margin-bottom: -10px;
        z-index: 3;
        position: relative;
        background: #fff;
        border: 1px solid #eee;
        border-radius: 10px 10px 0 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        font-weight: 700;
        font-size: 15px;
        color: #222;
        padding: 8px 0 4px 0;
        text-align: center;
        cursor: pointer;
        font-family: 'Inter', Arial, sans-serif !important;
    }
    .top-btn:disabled {
        color: #aaa;
        cursor: not-allowed;
    }
    .team-header {
        display: flex;
        align-items: center;
        background: #fff;
        border-radius: 18px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.07);
        padding: 24px 32px;
        margin-bottom: 32px;
        gap: 32px;
        flex-wrap: wrap;
    }
    .team-logo {
        width: 120px;
        height: 120px;
        object-fit: cover;
        border: 3px solid #eee;
        background: #fafafa;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        margin-right: 0;
        flex-shrink: 0;
    }
    .team-info-block {
        display: flex;
        flex-direction: column;
        justify-content: center;
        flex: 1;
        min-width: 0;
    }
    .team-name-row {
        display: flex;
        align-items: flex-end;
        flex-wrap: wrap;
        gap: 24px;
        justify-content: flex-start;
    }
    .team-name {
        font-size: 2.7rem;
        font-weight: 700;
        color: #222;
        letter-spacing: 0.5px;
        margin: 0;
        display: flex;
        align-items: center;
        min-height: 120px;
        font-family: 'Inter', Arial, sans-serif !important;
    }
    .team-extra-info {
        display: flex;
        flex-direction: row;
        gap: 32px;
        align-items: flex-end;
        font-size: 1.1rem;
        font-weight: 500;
        color: #444;
        margin-bottom: 8px;
        margin-left: 8px;
        flex-wrap: wrap;
    }
    .team-extra-label {
        color: #888;
        font-size: 1rem;
        font-weight: 600;
        margin-right: 4px;
    }
    .team-coach-placeholder {
        color: #bbb;
        font-size: 1.02rem;
        font-style: italic;
        margin-top: 8px;
        margin-left: 8px;
    }
    /* Highlight squad table cells by topr_class (st.dataframe) */
    /* Azul para Core Player A */
    .stDataFrame tbody tr td:nth-child(3):has(div:contains('Core Player A')) {
        background-color: #0074d980 !important;
        color: #fff !important;
    }
    /* Verde para Core Player B */
    .stDataFrame tbody tr td:nth-child(3):has(div:contains('Core Player B')) {
        background-color: #1db95480 !important;
        color: #fff !important;
    }
    /* Amarelo para Rotation Player */
    .stDataFrame tbody tr td:nth-child(3):has(div:contains('Rotation Player')) {
        background-color: #ffe06680 !important;
        color: #222 !important;
    }
    /* Laranja para Reserve Player */
    .stDataFrame tbody tr td:nth-child(3):has(div:contains('Reserve Player')) {
        background-color: #ff880080 !important;
        color: #fff !important;
    }
    /* Container principal para ajuste de layout */
    .main {
        max-width: 1500px;
        padding-left: 50px;
        padding-right: 50px;
        margin: 0 auto;
    }
    </style>
''', unsafe_allow_html=True)

# Inicialização do estado da sessão
if 'league_selected' not in st.session_state:
    st.session_state['league_selected'] = None
if 'team_selected' not in st.session_state:
    st.session_state['team_selected'] = None
if 'player_selected' not in st.session_state:
    st.session_state['player_selected'] = None

# Título da aplicação
st.title('SCOUTEXT FOOTBALL')

# Cria duas abas principais
tab1, tab2 = st.tabs(["📊 Analysis", "🕵️‍♂️ Scouting"])

# Aba da Análise (tudo o que já tens agora)
with tab1:
    if st.session_state['league_selected'] is None:
        selected_league = render_league_selector()
        if selected_league:
            st.session_state['league_selected'] = selected_league
            st.rerun()
    elif st.session_state['team_selected'] is None:
        selected_team = render_team_selector(st.session_state['league_selected'])
        if selected_team:
            st.session_state['team_selected'] = selected_team
            st.rerun()
    else:
        render_team_header(st.session_state['league_selected'], st.session_state['team_selected'])

        # Container principal para controle de layout
        with st.container():
            # Cria duas colunas com proporção 35%/45%
            col1, col2 = st.columns([0.35, 0.45])

            with col1:
                render_squad(st.session_state['team_selected'])

            with col2:
                render_game_style(st.session_state['team_selected'], st.session_state['league_selected'])

        # Renderiza a secção de equipas similares
        render_similar_teams(st.session_state['team_selected'], st.session_state['league_selected'])

import matplotlib.pyplot as plt
import numpy as np

def plot_spider_chart(df_jogadores, metricas, nomes):
    num_vars = len(metricas)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]  # fechar círculo

    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True), dpi=150)

    # Estilo clean e moderno
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    ax.spines['polar'].set_color("#DDD")
    ax.spines['polar'].set_linewidth(1)
    ax.grid(color="#EEE", linewidth=0.8)
    ax.tick_params(colors="#666", labelsize=8)

    # Setup ângulos e limites
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_ylim(0, 1)

    # Labels das métricas
    ax.set_thetagrids(np.degrees(angles[:-1]), metricas, fontsize=8, color="#333")

    cores = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#17becf']

    for idx, row in enumerate(df_jogadores.iterrows()):
        _, dados = row
        valores = dados[metricas].tolist()
        valores += valores[:1]
        cor = cores[idx % len(cores)]
        ax.plot(angles, valores, label=nomes[idx], color=cor, linewidth=1.5)
        ax.fill(angles, valores, color=cor, alpha=0.15)

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), fontsize=8, frameon=False, ncol=2)
    plt.tight_layout()
    return fig




from sklearn.preprocessing import MinMaxScaler

# Mapeamento de métricas por perfil (como definiste)
metricas_pesos_por_perfil = {
    "Goalkeeper": {
        "Traditional": [
            ('gk_save_ratio', 0.2 ), 
            ('gk_conceded_p90', 0.18 ), 
            ('gk_1v1_ratio', 0.11 ), 
            ('gk_areaprot_ratio', 0.14 ), 
            ('gk_areaprot_sp_ratio', 0.12 ), 
            ('gk_sweepkeep_p90', 0.15 ), 
            ('gk_longball_ratio', 0.10 ) 
        ],
        "Constructor": [
            ('gk_save_ratio', 0.12 ), 
            ('gk_conceded_p90', 0.12 ), 
            ('gk_sweepkeep_p90', 0.14 ), 
            ('gk_xT', 0.16 ), 
            ('gk_longball_ratio', 0.14 ), 
            ('gk_longball_free_p90', 0.18 ), 
            ('gk_pass_outbox_ratio', 0.14 ) 
        ]
    },
    "Center Back": {
        "Constructor": [
            ('cb_int_block_p90', 0.12 ), 
            ('cb_duel_ratio', 0.12 ), 
            ('cb_def_actions_p90', 0.14 ), 
            ('cb_xT_carry', 0.17 ), 
            ('cb_xT_passe', 0.19 ), 
            ('cb_longb_flanks_p90', 0.11 ), 
            ('cb_z14passes_p90', 0.15 ) 
        ],
        "Aggressive": [
            ('cb_int_block_p90', 0.14 ), 
            ('cb_foul_ratio', 0.14 ), 
            ('cb_duel_ratio', 0.17 ), 
            ('cb_aerial_duel_ratio', 0.14 ), 
            ('cb_def_actions_p90', 0.16 ), 
            ('cb_xT_carry', 0.12 ), 
            ('cb_xT_passe', 0.13 ) 
        ]
    },
    "Full Back": {
        "Traditional": [
            ('fb_int_block_p90', 0.15 ), 
            ('fb_duel_ratio', 0.14 ), 
            ('fb_aerial_duel_ratio', 0.10 ), 
            ('fb_carry_buildup_p90', 0.15 ), 
            ('fb_passes_vert_int_p90', 0.17 ), 
            ('fb_xT_p90', 0.12 ), 
            ('fb_cross_ratio', 0.17 ) 
        ],
        "Wing Back": [
            ('fb_int_block_p90', 0.15 ), 
            ('fb_duel_ratio', 0.15 ), 
            ('fb_carry_p90', 0.14 ), 
            ('fb_xT_p90', 0.14 ), 
            ('fb_cross_ratio', 0.14 ), 
            ('fb_delayed_cross_ratio', 0.13 ), 
            ('fb_passes_leadshot_p90', 0.15 ) 
        ],
        "Inverted": [
            ('fb_int_block_p90', 0.13 ), 
            ('fb_duel_ratio', 0.13 ), 
            ('fb_aerial_duel_ratio', 0.10 ), 
            ('fb_passes_leadshot_p90', 0.11 ), 
            ('fb_central_actions_p90', 0.19 ), 
            ('fb_xT_p90', 0.17 ), 
            ('fb_z14passes_p90', 0.17 ) 
        ]
    },
    "Center Midfielder": {
        "Holding": [
            ('cm_int_block_p90', 0.17 ), 
            ('cm_duel_ratio', 0.16 ), 
            ('cm_aerial_duel_ratio', 0.13 ), 
            ('cm_def_actions_p90', 0.18 ), 
            ('cm_def_cover_ratio', 0.14 ), 
            ('cm_xT_postrec_90', 0.12 ), 
            ('cm_xT_passe_p90', 0.10 ) 
        ],
        "Defensive Playmaker": [
            ('cm_int_block_p90', 0.11 ), 
            ('cm_duel_ratio', 0.11 ), 
            ('cm_def_actions_p90', 0.13 ), 
            ('cm_con_actions_p90', 0.14 ), 
            ('cm_passes_leadshot_p90', 0.14 ), 
            ('cm_xT_p90', 0.15 ), 
            ('cm_chip_through_p90', 0.12 ), 
            ('cm_longp_ratio', 0.10 ) 
        ],
        "Box-to-Box": [
            ('cm_duel_ratio', 0.12 ), 
            ('cm_defactions_opphalf_p90', 0.15 ), 
            ('cm_def_cover_ratio', 0.13 ), 
            ('cm_xT_postrec_90', 0.12 ), 
            ('cm_shots_p90', 0.16 ), 
            ('cm_boxtobox_actions_p90', 0.18 ), 
            ('cm_xT_carry_p90', 0.14 ) 
        ],
        "Interior": [
            ('cm_duel_ratio', 0.12 ), 
            ('cm_defactions_opphalf_p90', 0.15 ), 
            ('cm_lat_def_actions_p90', 0.15 ), 
            ('cm_con_actions_p90', 0.12 ), 
            ('cm_xT_passe_p90', 0.12 ), 
            ('cm_xT_carry_p90', 0.17 ), 
            ('cm_passes_leadshot_p90', 0.17 ) 
        ],
        "Offensive": [
            ('cm_defactions_opphalf_p90', 0.10 ), 
            ('cm_con_actions_p90', 0.10 ), 
            ('cm_xT_p90', 0.15 ), 
            ('cm_z14_receptions_p90', 0.17 ), 
            ('cm_shots_p90', 0.13 ), 
            ('cm_passes_leadshot_p90', 0.17 ), 
            ('cm_prod_index', 0.18 ) 
        ]
    },
    "Winger": {
        "Dribbler": [
            ('w_defactions_opphalf_p90', 0.05 ), 
            ('w_carries_box_p90', 0.12 ), 
            ('w_takeons_p90', 0.18 ), 
            ('w_takeons_ratio', 0.18 ), 
            ('w_cross_ratio', 0.14 ), 
            ('w_xT_p90', 0.15 ), 
            ('w_prod_index', 0.18 ) 
        ],
        "Interior": [
            ('w_defactions_opphalf_p90', 0.07 ), 
            ('w_z14_receptions_p90', 0.18 ), 
            ('w_passes_leadshot_z14_p90', 0.18 ), 
            ('w_con_actions_p90', 0.10 ), 
            ('w_takeons_ratio', 0.14 ), 
            ('w_xT_p90', 0.15 ), 
            ('w_prod_index', 0.18 ) 
        ],
        "Exterior Midfielder": [
            ('w_def_actions_p90', 0.12 ), 
            ('w_xT_carry_90', 0.15 ), 
            ('w_passes_leadshot_p90', 0.16 ), 
            ('w_cross_ratio', 0.17 ), 
            ('w_delayed_cross_ratio', 0.10 ), 
            ('w_takeons_ratio', 0.13 ), 
            ('w_prod_index', 0.17 ) 
        ]
    },
    "Striker": {
        "Target": [
            ('cf_defactions_opphalf_p90', 0.08 ), 
            ('cf_goals_p90', 0.18 ), 
            ('frontal_support_per_90', 0.14 ), 
            ('cf_aerial_duel_ratio', 0.15 ), 
            ('cf_box_aerial_duel_ratio', 0.15 ), 
            ('cf_shots_ontarget_ratio', 0.16 ), 
            ('cf_passes_received_box_p90', 0.14 ) 
        ],
        "Advanced": [
            ('cf_defactions_opphalf_p90', 0.10 ), 
            ('cf_goals_p90', 0.16 ), 
            ('cf_through_received_p90', 0.16 ), 
            ('cf_xT_carry_90', 0.12 ), 
            ('cf_lat_receptions_p90', 0.14 ), 
            ('cf_shots_ontarget_ratio', 0.16 ), 
            ('cf_prod_index', 0.16 ) 
        ],
        "False 9": [
            ('cf_defactions_opphalf_p90', 0.09 ), 
            ('cf_goals_p90', 0.15 ), 
            ('frontal_support_per_90', 0.13 ), 
            ('cf_xT_total', 0.16 ), 
            ('cf_passes_leadshot_p90', 0.16 ), 
            ('cf_z14_receptions_p90', 0.16 ), 
            ('cf_shots_ontarget_ratio', 0.15 ) 
        ]
    }
}


pesos_por_tier = {
    "English Premier League": 1.00,
    "Italian Serie A": 0.98,
    "Spanish La Liga": 1.00,
    "German Bundesliga": 0.98,
    "French Ligue 1": 0.96,
    
    "Portuguese Primeira Liga": 0.93,
    "Dutch Eredivisie": 0.93,
    
    "Belgian Jupiler Pro League": 0.85,
    "Spanish Segunda Division": 0.85,
    "English Football League - Championship": 0.85
}

from sklearn.preprocessing import MinMaxScaler  # Continua aqui caso queiras alternar depois
import pandas as pd

def calcular_ranking_com_pesos(df_base, posicao, perfil, metricas_por_perfil, coluna_minutos=None):
    metricas_com_pesos = metricas_por_perfil[posicao][perfil]
    metricas = [m for m, _ in metricas_com_pesos]
    metricas_validas = [m for m in metricas if m in df_base.columns]

    # 👉 Subconjunto válido (sem NaNs)
    df_valido = df_base.dropna(subset=metricas_validas).copy()
    if df_valido.empty:
        return pd.DataFrame()

    # 👉 Lista de métricas em que "menos é melhor"
    metricas_negativas = ["gk_conceded_p90", "cb_foul_ratio"]

    # 👉 Calcular percentis (0 a 100) dinâmicos
    for metrica in metricas_validas:
        if metrica in metricas_negativas:
            df_valido[metrica + "_percentil"] = 100 - df_valido[metrica].rank(pct=True) * 100
        else:
            df_valido[metrica + "_percentil"] = df_valido[metrica].rank(pct=True) * 100

    # 👉 Calcular perfil_score como média ponderada dos percentis
    df_valido["perfil_score"] = 0
    for metrica, peso in metricas_com_pesos:
        coluna_percentil = metrica + "_percentil"
        if coluna_percentil in df_valido.columns:
            df_valido["perfil_score"] += df_valido[coluna_percentil] * peso

    # 👉 Ajustar pelo peso da liga
    if "competition_known_name" in df_valido.columns:
        df_valido["liga_peso"] = df_valido["competition_known_name"].map(pesos_por_tier).fillna(1.00)
        df_valido["perfil_score"] *= df_valido["liga_peso"]

    # 👉 Colunas extra e resultado final
    colunas_extra = ["player_id", "player_name", "team_name", "position", "perfil_score"]
    if coluna_minutos and coluna_minutos in df_valido.columns:
        colunas_extra.append(coluna_minutos)

    # 👉 Mostrar percentis no resultado final (só os percentis)
    percentis_final = [m + "_percentil" for m in metricas_validas]
    df_ranking = df_valido.sort_values(by="perfil_score", ascending=False).copy()

    return df_ranking[colunas_extra + percentis_final].head(50)




# TAB 2 – SCOUTING
with tab2:
    st.subheader("🕵️‍♂️ Scouting by Position and Role")

    # 1. Carregar CSV principal
    caminho_csv = r"C:\Users\guica\OneDrive\Desktop\AppScout\data\metricas_eventing_final.csv"
    df_metricas = pd.read_csv(caminho_csv)

    # 2. Filtro por ligas
    ligas_disponiveis = [
        'German Bundesliga', 'English Football League - Championship',
        'English Premier League', 'Portuguese Primeira Liga',
        'Dutch Eredivisie', 'Italian Serie A', 'Spanish La Liga',
        'Spanish Segunda Division', 'French Ligue 1',
        'Belgian Jupiler Pro League'
    ]



    ligas_selecionadas = st.multiselect(
        "🌍 Select League(s):",
        ligas_disponiveis,
        default=ligas_disponiveis
    )

    df_metricas = df_metricas[df_metricas["competition_known_name"].isin(ligas_selecionadas)].copy()

    # 3. Dicionários
    perfis_por_posicao = {
        "Goalkeeper": ["Traditional", "Constructor"],
        "Center Back": ["Constructor", "Aggressive"],
        "Full Back": ["Traditional", "Wing Back", "Inverted"],
        "Center Midfielder": ["Holding", "Defensive Playmaker", "Box-to-Box", "Interior", "Offensive"],
        "Winger": ["Dribbler", "Interior", "Exterior Midfielder"],
        "Striker": ["Target", "Advanced", "False 9"]
    }

    pos_mapping = {
        "Goalkeeper": ["GK"],
        "Center Back": ["CB"],
        "Full Back": ["LWB", "RWB", "LB", "RB"],
        "Center Midfielder": ["CDM", "CM", "CAM"],
        "Winger": ["LM", "RM", "LW", "RW"],
        "Striker": ["ST"]
    }

    # 4. Filtros de posição e perfil
    posicao_escolhida = st.selectbox("🧩 Select a Position:", list(perfis_por_posicao.keys()), key="posicao_scouting")
    perfil_escolhido = st.selectbox("🎯 Select a Role:", perfis_por_posicao[posicao_escolhida], key="perfil_scouting")

    coluna_minutos = "minutos_gr_jogados" if posicao_escolhida == "Goalkeeper" else "minutos_jogados"

    # 5. Filtrar posição e aplicar slider de minutos
    # 5. Filtrar posição e aplicar slider de minutos
    posicoes_filtrar = pos_mapping[posicao_escolhida]
    df_filtrado = df_metricas[df_metricas["position"].isin(posicoes_filtrar)].copy()

    if coluna_minutos in df_filtrado.columns and not df_filtrado.empty:
        min_disponivel = int(df_filtrado[coluna_minutos].min())
        max_disponivel = int(df_filtrado[coluna_minutos].max())

        minutos_range = st.slider(
            f"⏱️ Filter by Minutes Played:",
            min_value=min_disponivel,
            max_value=max_disponivel,
            value=(min_disponivel, max_disponivel),
            step=10
        )

        df_filtrado = df_filtrado[
            (df_filtrado[coluna_minutos] >= minutos_range[0]) &
            (df_filtrado[coluna_minutos] <= minutos_range[1])
        ]

    # 6. Calcular ranking
    ligas_txt = ", ".join(ligas_selecionadas)
    
    st.markdown(f"**Players Found:** {len(df_filtrado)}")

    top_50_perfil = calcular_ranking_com_pesos(
        df_filtrado,
        posicao_escolhida,
        perfil_escolhido,
        metricas_pesos_por_perfil,
        coluna_minutos=coluna_minutos
    )


    # 👉 8. Adicionar colunas extras dos jogadores
    caminho_jp = r"C:\Users\guica\OneDrive\Desktop\ScoutingDash\data\processed\JugadoresJP.xlsx"

    # 👉 Formatador de valores em euros
    def formatar_euros(valor):
        try:
            if pd.isna(valor):
                return ""
            return f"€ {int(valor):,}".replace(",", ".")
        except:
            return valor


    try:
        df_jp = pd.read_excel(caminho_jp)

                # Garantir que o campo player_id existe em ambos e está limpo
        df_jp["player_id"] = df_jp["player_id"].astype(str).str.strip()
        top_50_perfil["player_id"] = top_50_perfil["player_id"].astype(str).str.strip()

        # Selecionar colunas de interesse
        colunas_extras = [
            "player_id", "Edad Guille", "Altura", "Peso", "Pie Preferido",
            "Nacionalidad", "Valor de Mercado", "Bruto Anual", "Expiración"
        ]
        df_extras = df_jp[colunas_extras].copy()

        # Merge pelo player_id
        top_50_perfil = top_50_perfil.merge(df_extras, on="player_id", how="left")


    except Exception as e:
        st.error(f"❌ Erro ao juntar dados extras dos jogadores: {e}")
        
    # 👉 Filtro por idade (deve vir depois do merge com os dados extra)
    if "Edad Guille" in top_50_perfil.columns and not top_50_perfil.empty:
        idade_min = int(top_50_perfil["Edad Guille"].min(skipna=True))
        idade_max = int(top_50_perfil["Edad Guille"].max(skipna=True))

        idade_range = st.slider(
            "👶 Filter by Age:",
            min_value=idade_min,
            max_value=idade_max,
            value=(idade_min, idade_max),
            step=1
        )

        top_50_perfil = top_50_perfil[
            (top_50_perfil["Edad Guille"].isna()) |  # manter os que não têm idade
            ((top_50_perfil["Edad Guille"] >= idade_range[0]) & (top_50_perfil["Edad Guille"] <= idade_range[1]))
        ]

    if "Valor de Mercado" in top_50_perfil.columns and not top_50_perfil.empty:
        mv_min = int(top_50_perfil["Valor de Mercado"].min(skipna=True))
        mv_max = int(top_50_perfil["Valor de Mercado"].max(skipna=True))

        mv_range = st.slider(
            "💰 Filter by Market Value (€):",
            min_value=mv_min,
            max_value=mv_max,
            value=(mv_min, mv_max),
            step=100000,
        )

        top_50_perfil = top_50_perfil[
            (top_50_perfil["Valor de Mercado"].isna()) |
            ((top_50_perfil["Valor de Mercado"] >= mv_range[0]) & (top_50_perfil["Valor de Mercado"] <= mv_range[1]))
        ]


    if "Bruto Anual" in top_50_perfil.columns and not top_50_perfil.empty:
        sal_min = int(top_50_perfil["Bruto Anual"].min(skipna=True))
        sal_max = int(top_50_perfil["Bruto Anual"].max(skipna=True))

        sal_range = st.slider(
            "📈 Filter by Annual Salary (€):",
            min_value=sal_min,
            max_value=sal_max,
            value=(sal_min, sal_max),
            step=100000,
        )

        top_50_perfil = top_50_perfil[
            (top_50_perfil["Bruto Anual"].isna()) |
            ((top_50_perfil["Bruto Anual"] >= sal_range[0]) & (top_50_perfil["Bruto Anual"] <= sal_range[1]))
        ]



    if "Expiración" in top_50_perfil.columns and not top_50_perfil["Expiración"].isna().all():
        top_50_perfil["Expiración"] = pd.to_datetime(
            top_50_perfil["Expiración"], errors="coerce"
        )
        anos_disponiveis = top_50_perfil["Expiración"].dt.year.dropna().astype(int)
        ano_min = int(anos_disponiveis.min())
        ano_max = int(anos_disponiveis.max())

        ano_range = st.slider(
            "📆 Filter by Contract Expiration Year:",
            min_value=ano_min,
            max_value=ano_max,
            value=(ano_min, ano_max),
            step=1
        )

        top_50_perfil = top_50_perfil[
            top_50_perfil["Expiración"].isna() |
            ((top_50_perfil["Expiración"].dt.year >= ano_range[0]) &
            (top_50_perfil["Expiración"].dt.year <= ano_range[1]))
        ]



    # 7. Mostrar tabela e radar
    if top_50_perfil.empty:
        st.warning("⚠️ Nenhum jogador com dados completos para este perfil.")
    else:
        
                # 👉 Ocultar colunas de percentis individuais (mas manter o perfil_score)
        colunas_a_ocultar = [col for col in top_50_perfil.columns if "_percentil" in col and col != "perfil_score"]
        top_50_perfil = top_50_perfil.drop(columns=colunas_a_ocultar)

        top_50_perfil = top_50_perfil.drop(columns=["player_id"], errors="ignore")

        top_50_perfil = top_50_perfil.drop_duplicates()

            # 👉 Renomear colunas para nomes mais bonitos
        top_50_perfil = top_50_perfil.rename(columns={
            "player_name": "Player",
            "team_name": "Team",
            "position": "Position",
            "perfil_score": "Percentile",
            "minutos_jogados": "Minutes Played",
            "minutos_gr_jogados": "Minutes Played",
            "Edad Guille": "Age",
            "Altura": "Height",
            "Peso": "Weight",
            "Pie Preferido": "Foot",
            "Nacionalidad": "Nationality",
            "Valor de Mercado": "Market Value",
            "Bruto Anual": "Annual Salary",
            "Expiración": "Contract Expiration"
        })



# 👉 Identificar colunas com percentis
        colunas_percentis = [col for col in top_50_perfil.columns if "_percentil" in col or col == "Percentile"]

        # 👉 Aplicar gradiente de cor do vermelho (baixo) ao verde (alto)
        df_colorido = top_50_perfil.style.background_gradient(
            subset=colunas_percentis,
            cmap="RdYlGn",
            axis=0
        ).format(precision=1, formatter={
            "Market Value": formatar_euros,
            "Annual Salary": formatar_euros,
            "Minutes Played": "{:.0f}",
            "Minutes Played": "{:.0f}",
            "Age": "{:.0f}",
            "Weight": "{:.0f}",
            "Height": "{:.2f}"
        }).set_properties(**{'text-align': 'center'}).set_table_styles([
            {"selector": "th", "props": [("text-align", "center")]}
        ])

        top_50_perfil["Contract Expiration"] = top_50_perfil["Contract Expiration"].dt.strftime("%B %d, %Y")

        # 👉 Mostrar tabela estilizada
        st.write(df_colorido)


        from mplsoccer import PyPizza
        import matplotlib.pyplot as plt
        import numpy as np

        from mplsoccer import PyPizza
        import matplotlib.pyplot as plt
        import numpy as np
        from matplotlib.patches import Patch

        # 👉 Dicionário com nomes bonitos e grupo de cada métrica
        metricas_info = {
            "gk_save_ratio":           {"nome": "Save Ratio %", "grupo": "Defensive"},
            "gk_conceded_p90":         {"nome": "Goals Conceded p90", "grupo": "Defensive"},
            "gk_1v1_ratio":            {"nome": "1v1 %", "grupo": "Defensive"},
            "gk_areaprot_ratio":       {"nome": "Area Protection %", "grupo": "Defensive"},
            "gk_areaprot_sp_ratio":    {"nome": "Set-Piece Area Protection %", "grupo": "Defensive"},
            "gk_sweepkeep_p90":        {"nome": "Sweeper Actions p90", "grupo": "Defensive"},
            "gk_xT":                   {"nome": "xT p90", "grupo": "Offensive"},
            "gk_longball_ratio":       {"nome": "Long Ball %", "grupo": "Offensive"},
            "gk_longball_free_p90":    {"nome": "Long Balls to Free Man p90", "grupo": "Offensive"},
            "gk_pass_outbox_ratio":    {"nome": "Passes Outside the Box %", "grupo": "Offensive"},

            "cb_int_block_p90":        {"nome": "Interceptions / Blocked Passes p90", "grupo": "Defensive"},
            "cb_duel_ratio":           {"nome": "Duel %", "grupo": "Defensive"},
            "cb_def_actions_p90":      {"nome": "Defensive Actions p90", "grupo": "Defensive"},
            "cb_xT_carry":             {"nome": "Carries p90", "grupo": "Offensive"},
            "cb_xT_passe":             {"nome": "xT per Carry", "grupo": "Offensive"},
            "cb_longb_flanks_p90":     {"nome": "Long Balls to Flanks p90", "grupo": "Offensive"},
            "cb_z14passes_p90":        {"nome": "Zone 14+ Passes p90", "grupo": "Offensive"},
            "cb_foul_ratio":           {"nome": "Foul %", "grupo": "Defensive"},
            "cb_aerial_duel_ratio":    {"nome": "Aerial Duel %", "grupo": "Defensive"},

            "fb_int_block_p90":        {"nome": "Interceptions / Blocked Passes     p90", "grupo": "Defensive"},
            "fb_duel_ratio":           {"nome": "Duel %", "grupo": "Defensive"},
            "fb_def_actions_p90":      {"nome": "Defensive Actions p90", "grupo": "Defensive"},
            "fb_carry_p90":            {"nome": "Carries p90", "grupo": "Offensive"},
            "fb_cross_ratio":          {"nome": "Cross %", "grupo": "Offensive"},
            "fb_xT_p90":               {"nome": "xT p90", "grupo": "Offensive"},
            "fb_delayed_cross_ratio":  {"nome": "Delayed Cross %", "grupo": "Offensive"},
            "fb_passes_vert_int_p90":  {"nome": "Interior / Vertical Passes p90", "grupo": "Offensive"},
            "fb_passes_leadshot_p90":  {"nome": "Passes Leading to Shot p90", "grupo": "Offensive"},
            "fb_aerial_duel_ratio":    {"nome": "Aerial Duel %", "grupo": "Defensive"},
            "fb_carry_buildup_p90":    {"nome": "Carries in Buildup Phase p90", "grupo": "Offensive"},
            "fb_central_actions_p90":  {"nome": "Central Actions p90", "grupo": "Offensive"},
            "fb_z14passes_p90":        {"nome": "Zone 14+ Passes p90", "grupo": "Offensive"},

            "cm_int_block_p90":        {"nome": "Interceptions / Blocked Passes p90", "grupo": "Defensive"},
            "cm_duel_ratio":           {"nome": "Duel %", "grupo": "Defensive"},
            "cm_aerial_duel_ratio":    {"nome": "Aerial Duel %", "grupo": "Defensive"},
            "cm_def_actions_p90":      {"nome": "Defensive Actions p90", "grupo": "Defensive"},
            "cm_xT_postrec_90":        {"nome": "xT After Recovery p90", "grupo": "Offensive"},
            "cm_xT_passe_p90":         {"nome": "xT per Pass p90", "grupo": "Offensive"},
            "cm_con_actions_p90":      {"nome": "Conneccting Actions p90", "grupo": "Offensive"},
            "cm_passes_leadshot_p90":  {"nome": "Passes Leading to Shot p90", "grupo": "Offensive"},
            "cm_xT_p90":               {"nome": "xT p90", "grupo": "Offensive"},
            "cm_chip_through_p90":     {"nome": "Chipped / Through Passes p90", "grupo": "Offensive"},
            "cm_longp_ratio":          {"nome": "Long Pass %", "grupo": "Offensive"},
            "cm_defactions_opphalf_p90":{"nome": "Defensive Actions in Opponents Half p90", "grupo": "Defensive"},
            "cm_def_cover_ratio":      {"nome": "Defensive Coverage %", "grupo": "Defensive"},
            "cm_shots_p90":            {"nome": "Shots p90", "grupo": "Offensive"},
            "cm_boxtobox_actions_p90": {"nome": "Box-to-Box Actions p90", "grupo": "Offensive"},
            "cm_xT_carry_p90":         {"nome": "xT per Carry p90", "grupo": "Offensive"},
            "cm_lat_def_actions_p90":  {"nome": "Lateral Defensive Actions p90", "grupo": "Defensive"},
            "cm_z14_receptions_p90":   {"nome": "Zone 14+ Receptions p90", "grupo": "Offensive"},
            "cm_prod_index":           {"nome": "Productivity Index", "grupo": "Offensive"},

            "w_defactions_opphalf_p90":{"nome": "Defensive Actions in Opponents Half p90", "grupo": "Defensive"},
            "w_carries_box_p90":       {"nome": "Carries into Box p90", "grupo": "Offensive"},
            "w_takeons_p90":           {"nome": "Take-Ons p90", "grupo": "Offensive"},
            "w_takeons_ratio":         {"nome": "Take-Ons %", "grupo": "Offensive"},
            "w_cross_ratio":           {"nome": "Cross %", "grupo": "Offensive"},
            "w_xT_p90":                {"nome": "xT p90", "grupo": "Offensive"},
            "w_prod_index":            {"nome": "Productivity Index", "grupo": "Offensive"},
            "w_z14_receptions_p90":    {"nome": "Zone 14+ Receptions p90", "grupo": "Offensive"},
            "w_passes_leadshot_z14_p90":{"nome": "Passes Leading to Shot p90", "grupo": "Offensive"},
            "w_con_actions_p90":       {"nome": "Connecting Actions p90", "grupo": "Offensive"},
            "w_defactions_p90":        {"nome": "Defensive Actions p90", "grupo": "Defensive"},
            "w_xT_carry_90":           {"nome": "xT per Carry", "grupo": "Offensive"},
            "w_passes_leadshot_p90":   {"nome": "Passes Leading to Shot p90", "grupo": "Offensive"},
            "w_delayed_cross_ratio":   {"nome": "Delayed Cross %", "grupo": "Offensive"},

            "cf_defactions_opphalf_p90":{"nome": "Defensive Actions in Opponents Half p90", "grupo": "Defensive"},
            "cf_goals_p90":             {"nome": "Goals p90", "grupo": "Offensive"},
            "frontal_support_per_90":   {"nome": "Frontal Support p90", "grupo": "Offensive"},
            "cf_aerial_duel_ratio":     {"nome": "Aerial Duel %", "grupo": "Defensive"},
            "cf_box_aerial_duel_ratio": {"nome": "Aerial Duel in Box %", "grupo": "Offensive"},
            "cf_shots_ontarget_ratio":  {"nome": "Shots on Target %", "grupo": "Offensive"},
            "cf_passes_received_box_p90":{"nome": "Passes Received in Box p90", "grupo": "Offensive"},
            "cf_through_received_p90":  {"nome": "Through Balls Received p90", "grupo": "Offensive"},
            "cf_xT_carry_90":           {"nome": "xT Carry p90", "grupo": "Offensive"},
            "cf_lat_receptions_p90":    {"nome": "Lateral Receptions p90", "grupo": "Offensive"},
            "cf_prod_index":            {"nome": "Productivity Index", "grupo": "Offensive"},
            "cf_xT_total":              {"nome": "xT p90", "grupo": "Offensive"},
            "cf_passes_leadshot_p90":   {"nome": "Passes Leading to Shot p90", "grupo": "Offensive"},
            "cf_z14_receptions_p90":    {"nome": "Zone 14+ Receptions p90", "grupo": "Offensive"}
        }

        # 👉 Cores atribuídas a cada grupo
        cores_por_grupo = {
            "Defensive": "#1A78CF",
            "Offensive": "#D70232",
        }

        # 👉 1. Métricas do perfil selecionado
        metricas_atuais = metricas_pesos_por_perfil[posicao_escolhida][perfil_escolhido]
        metricas_radar = [metrica + "_percentil" for metrica, _ in metricas_atuais]

        # 👉 2. Jogadores disponíveis
        jogadores_disponiveis = top_50_perfil["Player"].unique().tolist()
        jogadores_selecionados = st.multiselect("🧬 Select Player(s):", jogadores_disponiveis)

        # 👉 Atualiza o df_metricas com os percentis globais
        df_metricas = calcular_ranking_com_pesos(
            df_metricas,
            posicao_escolhida,
            perfil_escolhido,
            metricas_pesos_por_perfil,
            coluna_minutos=coluna_minutos
        )

        # 👉 3. Se houver jogadores
        if jogadores_selecionados:

            # ✅ Usar os percentis já calculados com base em todos os jogadores
            df_radar = df_metricas.copy()


            jogadores_validos = []
            graficos = []

            for jogador in jogadores_selecionados:
                jogador_df = df_radar[df_radar["player_name"].str.strip().str.lower() == jogador.strip().lower()]
                valores_raw = jogador_df[metricas_radar].apply(pd.to_numeric, errors='coerce')

                if valores_raw.empty or valores_raw.isnull().values.any():
                    st.warning(f"⚠️ O jogador **{jogador}** foi ignorado por ter dados em falta.")
                    continue

                jogadores_validos.append(jogador)
                valores = valores_raw.values.flatten().tolist()
                valores_formatados = [float(f"{v:.1f}") for v in valores]  # arredondados, mas continuam floats
                graficos.append(valores_formatados)



            if jogadores_validos:
                # Radar compacto: 4x4 por radar
                n = len(jogadores_validos)
                cols = 2
                rows = int(np.ceil(n / cols))
                fig, axs = plt.subplots(rows, cols, figsize=(4, 4 * rows), subplot_kw=dict(polar=True), dpi=300)
                axs = axs.flatten()

                for idx, (jogador, valores) in enumerate(zip(jogadores_validos, graficos)):

                    metricas = [m.replace("_percentil", "") for m in metricas_radar]
                    nomes_legiveis = [metricas_info.get(m, {"nome": m})["nome"] for m in metricas]
                    grupos = [metricas_info.get(m, {"grupo": "Outro"})["grupo"] for m in metricas]
                    slice_colors = [cores_por_grupo.get(grupo, "#BBBBBB") for grupo in grupos]

                    baker = PyPizza(
                        params=nomes_legiveis,
                        background_color="#FFFFFF",
                        straight_line_color="#FFFFFF",
                        last_circle_lw=0.3,
                        other_circle_lw=0,
                        inner_circle_size=4.5,  # círculo central um pouco mais pequeno
                    )

                    baker.make_pizza(
                        valores,  # <- NÃO uses valores_formatados aqui, senão dá erro no .make_pizza()
                        ax=axs[idx],
                        color_blank_space="same",
                        slice_colors=slice_colors,
                        blank_alpha=0.4,
                        kwargs_slices=dict(edgecolor="#F2F2F2", zorder=2, linewidth=0.8),
                        kwargs_params=dict(color="#000000", fontsize=3, va="center"),  # nome das métricas
                        kwargs_values=dict(
                            color="#000000",
                            fontsize=3,
                            zorder=3,
                            bbox=dict(
                                edgecolor="#000000",
                                facecolor="#ffffff",
                                boxstyle="round,pad=0.15",
                                lw=0.1
                            )
                        )
                    )

                    axs[idx].set_title(f"{jogador}", fontsize=4, color="#000000", weight="bold", loc='left')

                # Esconder eixos a mais
                for j in range(len(jogadores_validos), len(axs)):
                    fig.delaxes(axs[j])

                # Legenda das cores
                grupos_usados = set(grupos)
                legenda = [
                    Patch(facecolor=cores_por_grupo[g], edgecolor="none", label=g)
                    for g in grupos_usados if g in cores_por_grupo
                ]
                fig.legend(
                    handles=legenda,
                    loc='upper center',
                    bbox_to_anchor=(0.5, 1.05),
                    ncol=len(legenda),
                    frameon=False,
                    fontsize=4
                )

                from io import BytesIO
                buf = BytesIO()
                fig.savefig(buf, format="png", dpi=300, bbox_inches="tight", pad_inches=0.05)
            

                with st.container():
                    st.markdown("<div style='margin-top:-10px'></div>", unsafe_allow_html=True)
                    st.image(buf.getvalue())




