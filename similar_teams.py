import streamlit as st
import pandas as pd
import numpy as np
import os
import base64

# Caminhos dos ficheiros
STYLES_XLSX = r'C:/Users/guica/OneDrive/Desktop/ScoutingDash/data/processed/WyScout/Stats_EstilosJogo.xlsx'
EQUIPAS_PATH = r'C:/Users/guica/OneDrive/Desktop/AppScout/assets/equipas'

def get_team_league(team_logo: str) -> str:
    """
    Obtém a liga de uma equipa baseado no seu logo.
    
    Args:
        team_logo (str): Nome do logo da equipa
        
    Returns:
        str: Nome da liga ou None se não encontrada
    """
    try:
        # Procura o logo em todas as ligas
        for liga in os.listdir(EQUIPAS_PATH):
            liga_path = os.path.join(EQUIPAS_PATH, liga)
            if os.path.isdir(liga_path):
                if team_logo in os.listdir(liga_path):
                    return liga
        return None
    except Exception as e:
        return None

def get_similar_teams(selected_team: str, selected_league: str, n_similar: int = 4) -> pd.DataFrame:
    """
    Encontra as equipas mais similares baseado na distância euclidiana no espaço PCA.
    
    Args:
        selected_team (str): Logo da equipa selecionada
        selected_league (str): Nome da liga selecionada
        n_similar (int): Número de equipas similares a retornar
        
    Returns:
        pd.DataFrame: DataFrame com as equipas similares
    """
    try:
        # Carrega os dados
        df = pd.read_excel(STYLES_XLSX)
        
        # Verifica se as colunas necessárias existem
        required_columns = ['Logo', 'PCA1', 'PCA2', 'Cluster']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            st.error(f"Colunas em falta no ficheiro de estilos: {', '.join(missing_columns)}")
            return pd.DataFrame()
        
        # Encontra a equipa selecionada
        selected_row = df[df['Logo'] == selected_team]
        if selected_row.empty:
            st.warning(f"Equipa {selected_team} não encontrada nos dados de estilo de jogo")
            return pd.DataFrame()
        
        # Obtém o cluster e coordenadas PCA da equipa selecionada
        selected_cluster = selected_row.iloc[0]['Cluster']
        selected_pca1 = selected_row.iloc[0]['PCA1']
        selected_pca2 = selected_row.iloc[0]['PCA2']
        
        # Filtra equipas do mesmo cluster, exceto a própria
        same_cluster = df[(df['Cluster'] == selected_cluster) & (df['Logo'] != selected_team)].copy()
        
        if len(same_cluster) == 0:
            st.warning(f"Não foram encontradas outras equipas no mesmo cluster {selected_cluster}")
            return pd.DataFrame()
        
        # Calcula distância euclidiana
        same_cluster['dist'] = np.sqrt(
            (same_cluster['PCA1'] - selected_pca1)**2 + 
            (same_cluster['PCA2'] - selected_pca2)**2
        )
        
        # Ordena por distância
        same_cluster = same_cluster.sort_values('dist')
        
        # Retorna as n_similar equipas mais próximas
        result = same_cluster.head(n_similar)
        
        return result
    
    except Exception as e:
        st.error(f"Erro ao calcular equipas similares: {str(e)}")
        return pd.DataFrame()

def render_similar_teams_section(similar_teams: pd.DataFrame, selected_league: str):
    """
    Renderiza a secção de equipas similares.
    
    Args:
        similar_teams (pd.DataFrame): DataFrame com as equipas similares
        selected_league (str): Nome da liga selecionada
    """
    if similar_teams.empty:
        st.warning("Não foram encontradas equipas similares suficientes.")
        return
    
    # Título da secção
    st.markdown('<h4 style="margin-top:2.2rem;margin-bottom:1.1rem;font-weight:700;letter-spacing:0.2px; text-align:center;">Similar Teams</h4>', unsafe_allow_html=True)
    
    # Container principal com flexbox
    container_html = '<div style="display:flex;justify-content:center;gap:48px;align-items:center;margin-bottom:1.5rem;flex-wrap:wrap;">'
    
    # Renderiza cada logo
    for _, row in similar_teams.iterrows():
        team_logo = row['Logo']
        distance = row['dist']
        
        # Procura a liga da equipa similar
        team_league = get_team_league(team_logo)
        
        if team_league:
            # Procura o logo no diretório da liga correta
            logo_path = os.path.join(EQUIPAS_PATH, team_league, team_logo)
            if os.path.exists(logo_path):
                with open(logo_path, "rb") as image_file:
                    encoded = base64.b64encode(image_file.read()).decode()
                
                # Container individual para cada equipa
                container_html += '<div style="display:flex;flex-direction:column;align-items:center;min-width:120px;">'
                
                # Logo da equipa
                container_html += f'<img src="data:image/png;base64,{encoded}" alt="{team_logo}" style="height:72px;width:auto;object-fit:contain;margin-bottom:0.5rem;"/>'
                
                # Nome da equipa
                team_name = team_logo.replace('.png', '')
                container_html += f'<span style="font-size:0.9rem;font-family:Inter,Arial,sans-serif;font-weight:600;color:#222;text-align:center;max-width:110px;overflow-wrap:anywhere;margin-bottom:0.2rem;">{team_name}</span>'
                
                # Liga da equipa
                container_html += f'<span style="font-size:0.8rem;font-family:Inter,Arial,sans-serif;font-weight:500;color:#666;text-align:center;">{team_league}</span>'
                
                # Fecha o container da equipa
                container_html += '</div>'
            else:
                st.write(f"⚠️ Debug: Logo não encontrado para {team_logo} em {logo_path}")
        else:
            st.write(f"⚠️ Debug: Liga não encontrada para {team_logo}")
    
    # Fecha o container principal
    container_html += '</div>'
    
    # Renderiza o HTML
    st.markdown(container_html, unsafe_allow_html=True)

def render_similar_teams(selected_team: str, selected_league: str):
    """
    Renderiza a secção completa de equipas similares.
    
    Args:
        selected_team (str): Logo da equipa selecionada
        selected_league (str): Nome da liga selecionada
    """
    try:
        # Obtém as equipas similares
        similar_teams = get_similar_teams(selected_team, selected_league)
        
        # Renderiza a secção
        render_similar_teams_section(similar_teams, selected_league)
        
    except Exception as e:
        st.error(f"Erro ao carregar equipas similares: {str(e)}") 