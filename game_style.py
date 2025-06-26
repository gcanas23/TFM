import streamlit as st
import pandas as pd
import plotly.express as px
import os
import base64

# Caminhos dos ficheiros
STYLES_XLSX = r'C:/Users/guica/OneDrive/Desktop/ScoutingDash/data/processed/WyScout/Stats_EstilosJogo.xlsx'
EQUIPAS_PATH = r'C:/Users/guica/OneDrive/Desktop/AppScout/assets/equipas'

# Mapeamento de cores para cada estilo de jogo
COLOR_MAP = {
    'Conservative': '#FF0000',  # Red
    'Transition': '#FFD700',    # Yellow
    'Hybrid': '#32CD32',        # Green
    'Dominant': '#1E90FF'       # Blue
}

# Mapeamento de clusters para estilos de jogo
CLUSTER_LABELS = {
    0: 'Transition',
    1: 'Conservative',
    2: 'Hybrid',
    3: 'Dominant'
}

# Interpretação dos clusters
CLUSTER_INTERPRETATION = {
    0: """
• Passes per possession: 3.96 (low)


• Positional Attacks Ratio: 0.81 (low)


• PPDA: 14.03 (very weak pressing)


• High Recovery Ratio: 0.14 (low)~

Interpretation:
Teams that defend deep, concede possession to the opponent, and look to exploit quick transitions. They have few positional attacks and little high pressing. Typical style of reactive teams, often underdogs or clubs with a more pragmatic approach.""",

    1: """
• Passes per possession: 3.77 (low)

• Positional Attacks Ratio: 1.00 (medium)

• PPDA: 10.68 (medium pressing)

• High Recovery Ratio: 0.15 (medium-low)

Interpretation:
Teams with a more cautious playing style, who don't circulate the ball much and take fewer risks in possession. They press at a medium height and don't particularly stand out in high recoveries. Typical profile of defensive teams or those who prioritize solidity over taking control of the game.""",

    2: """
• Passes per possession: 5.12 (medium-high)

• Positional Attacks Ratio: 1.25 (high)

• PPDA: 10.91 (good pressing)

• High Recovery Ratio: 0.17 (medium-high)

Interpretation:
Balanced teams, capable of maintaining possession and building in positional attack, while also competitive in pressing without the ball. They don't dominate like the "Dominant" group but can adapt to the context. Typical style of well-coached, flexible teams with clear ideas.""",

    3: """
• Passes per possession: 5.98 (high)

• Positional Attacks Ratio: 1.82 (very high)

• PPDA: 9.56 (very high pressing)

• High Recovery Ratio: 0.21 (very high)

Interpretation:
Teams with total game control. They circulate the ball extensively, create many positional attacks, and constantly suffocate the opponent with pressure. They play high, recover quickly, and impose their game model. Typical style of top teams."""
}

def get_game_style_data() -> pd.DataFrame:
    """
    Obtém os dados de estilo de jogo.
    
    Returns:
        pd.DataFrame: DataFrame com os dados ou DataFrame vazio se erro
    """
    try:
        # Carrega os dados
        df = pd.read_excel(STYLES_XLSX)
        
        # Verifica se as colunas necessárias existem
        required_columns = ['Team', 'PCA1', 'PCA2', 'Cluster', 'Logo']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            st.error(f"Colunas em falta no ficheiro de estilos: {', '.join(missing_columns)}")
            return pd.DataFrame()
        
        # Adiciona a coluna Style baseada no Cluster
        df['Style'] = df['Cluster'].map(CLUSTER_LABELS)
        
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados de estilo de jogo: {str(e)}")
        return pd.DataFrame()

def render_game_style_scatter(df: pd.DataFrame, selected_team: str, selected_league: str):
    """
    Renderiza o scatter plot do estilo de jogo.
    
    Args:
        df (pd.DataFrame): DataFrame com os dados
        selected_team (str): Logo da equipa selecionada
        selected_league (str): Nome da liga selecionada
    """
    try:
        # Cria o gráfico base
        fig = px.scatter(
            df,
            x='PCA1',
            y='PCA2',
            color='Style',
            color_discrete_map=COLOR_MAP,
            opacity=0.7,
            width=1000,
            height=500,
            custom_data=['Team', 'Style'],
            labels={"PCA1": "Defensive", "PCA2": "Offensive"}
        )
        
        # Atualiza o template do hover
        hover_template = '<b>Team:</b> %{customdata[0]}<br><b>Game Style:</b> %{customdata[1]}<extra></extra>'
        
        fig.update_traces(
            hovertemplate=hover_template,
            selector=dict(mode='markers')
        )
        
        # Adiciona logos das equipas
        logo_normal_size = 0.455
        logo_selected_size = logo_normal_size * 1.7
        
        # Adiciona logos das equipas
        for _, row in df.iterrows():
            team_logo = row['Logo']
            x_logo = row['PCA1']
            y_logo = row['PCA2']
            
            # Procura o logo no diretório de equipas
            logo_path = os.path.join(EQUIPAS_PATH, selected_league, team_logo)
            if os.path.exists(logo_path):
                with open(logo_path, "rb") as image_file:
                    encoded = base64.b64encode(image_file.read()).decode()
                
                # Define o tamanho do logo
                size = logo_selected_size if team_logo == selected_team else logo_normal_size
                
                fig.add_layout_image(
                    dict(
                        source=f"data:image/png;base64,{encoded}",
                        xref="x",
                        yref="y",
                        x=x_logo,
                        y=y_logo,
                        sizex=size,
                        sizey=size,
                        xanchor="center",
                        yanchor="middle",
                        layer="above"
                    )
                )
        
        # Atualiza o layout
        fig.update_layout(
            title=None,
            font=dict(family='Inter, Arial, sans-serif'),
            plot_bgcolor='#fafafa',
            paper_bgcolor='#fafafa',
            margin=dict(l=20, r=20, t=20, b=20),
            legend_title_text='Game Style',
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
            showlegend=True
        )
        
        # Renderiza o gráfico
        st.markdown('<h4 style="margin-top:2.5rem;margin-bottom:0.7rem;font-weight:700;letter-spacing:0.2px; text-align:center;">Game Style</h4>', unsafe_allow_html=True)
        st.markdown('<div style="text-align:center;">', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=False)
        st.markdown('</div>', unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Erro ao renderizar gráfico de estilo de jogo: {str(e)}")

def render_game_style_description(df: pd.DataFrame, selected_team: str):
    """
    Renderiza a descrição do estilo de jogo da equipa.
    
    Args:
        df (pd.DataFrame): DataFrame com os dados
        selected_team (str): Logo da equipa selecionada
    """
    try:
        # Filtra dados da equipa selecionada
        team_data = df[df['Logo'] == selected_team]
        
        if team_data.empty:
            st.warning(f"Não foram encontrados dados de estilo de jogo para {selected_team}")
            return
            
        # Obtém o cluster e estilo
        cluster = team_data.iloc[0]['Cluster']
        style = team_data.iloc[0]['Style']
        style_color = COLOR_MAP.get(style, '#222')
        
        # Obtém os valores estatísticos
        passes_per_possession = team_data.iloc[0]['Average passes per possession']
        positional_attacks = team_data.iloc[0]['Positional attacks Ratio']
        ppda = team_data.iloc[0]['PPDA']
        high_recovery = team_data.iloc[0]['High Recovery Ratio']
        
        # Obtém a interpretação do cluster
        interpretation = CLUSTER_INTERPRETATION.get(int(cluster), "Estilo de jogo não categorizado")
        
        # Extrai apenas a parte de interpretação do texto
        interpretation_text = interpretation.split('Interpretation:')[-1].strip()
        
        # Constrói a descrição estatística em formato vertical
        stats_description = f"""
• Passes per possession: {passes_per_possession:.2f}
• Positional Attacks Ratio: {positional_attacks:.2f}
• PPDA: {ppda:.2f}
• High Recovery Ratio: {high_recovery:.2f}
"""
        
        # Renderiza o título do estilo
        st.markdown(f'<div style="text-align:center; margin-top:0.7rem; font-family:Inter, Arial, sans-serif; font-size:1.50rem; font-weight:700; color:{style_color}; letter-spacing:0.2px;">{style}</div>', unsafe_allow_html=True)
        
        # Renderiza as métricas
        st.markdown(f'''
        <div style="text-align:center; color:#222; font-family:Inter, Arial, sans-serif; font-size:1.08rem; font-weight:500; margin-top:0.5rem; margin-bottom:0.5rem; max-width:480px; margin-left:auto; margin-right:auto;">
        {stats_description}
        </div>
        ''', unsafe_allow_html=True)
        
        # Renderiza a interpretação
        st.markdown(f'''
        <div style="text-align:center; color:#222; font-family:Inter, Arial, sans-serif; font-size:1.08rem; font-weight:500; margin-top:0.5rem; margin-bottom:1.2rem; max-width:480px; margin-left:auto; margin-right:auto;">
        {interpretation_text}
        </div>
        ''', unsafe_allow_html=True)
                
    except Exception as e:
        st.error(f"Erro ao renderizar descrição do estilo de jogo: {str(e)}")

def render_game_style(selected_team: str, selected_league: str):
    """
    Renderiza a secção de estilo de jogo.
    
    Args:
        selected_team (str): Logo da equipa selecionada
        selected_league (str): Nome da liga selecionada
    """
    # Carrega os dados
    df = get_game_style_data()
    if df.empty:
        return
        
    # Renderiza o gráfico e a descrição
    render_game_style_scatter(df, selected_team, selected_league)
    render_game_style_description(df, selected_team)
