import streamlit as st
import pandas as pd
import os

# Caminho do ficheiro
METRICAS_CSV = r'C:/Users/guica/OneDrive/Desktop/ScoutingDash/data/processed/eventing/metricas_eventing_final.csv'

# Mapeamento de cores para cada tipo de jogador
PLAYER_COLORS = {
    'Core Player A': '#0074d980',  # Azul translúcido
    'Core Player B': '#1db95480',  # Verde translúcido
    'Rotation Player': '#ffe06680',  # Amarelo translúcido
    'Reserve Player': '#ff880080',  # Laranja translúcido
}

def get_player_data(selected_team: str) -> pd.DataFrame:
    """
    Obtém os dados dos jogadores para uma equipa específica.
    
    Args:
        selected_team (str): Logo da equipa selecionada
        
    Returns:
        pd.DataFrame: DataFrame com os dados dos jogadores ou DataFrame vazio se erro
    """
    try:
        # Carrega os dados
        df = pd.read_csv(METRICAS_CSV)
        
        # Verifica se as colunas necessárias existem
        required_columns = ['player_name', 'time_on_pitch_rate', 'topr_class', 'Logo']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            st.error(f"Colunas em falta no ficheiro de métricas: {', '.join(missing_columns)}")
            return pd.DataFrame()
        
        # Filtra por equipa usando o Logo
        df_filtered = df[df['Logo'] == selected_team][required_columns].copy()
        
        # Remove duplicados
        df_filtered = df_filtered.drop_duplicates(subset=['player_name'])
        
        # Converte time_on_pitch_rate para float, removendo o símbolo %
        df_filtered['time_on_pitch_rate'] = df_filtered['time_on_pitch_rate'].str.rstrip('%').astype(float)
        
        # Ordena por tempo em campo
        df_filtered = df_filtered.sort_values(by='time_on_pitch_rate', ascending=False)
        
        # Formata a coluna time_on_pitch_rate como percentagem
        df_filtered['time_on_pitch_rate'] = df_filtered['time_on_pitch_rate'].map(
            lambda x: f"{x:.1f}%" if pd.notnull(x) else "-"
        )
        
        return df_filtered
    except Exception as e:
        st.error(f"Erro ao carregar dados dos jogadores: {str(e)}")
        return pd.DataFrame()

def render_squad(selected_team: str):
    """
    Renderiza a tabela de jogadores da equipa selecionada.
    
    Args:
        selected_team (str): Logo da equipa selecionada
    """
    st.markdown('### Squad')
    
    # Obtém os dados dos jogadores
    df = get_player_data(selected_team)
    if df.empty:
        st.warning(f"Não foram encontrados jogadores para a equipa {selected_team}")
        return
    
    # Cria o HTML da tabela
    table_html = '<div style="margin-top:1.5rem; margin-bottom:1.5rem; padding: 24px 32px; background: #fff; border-radius: 16px; box-shadow: 0 2px 12px rgba(0,0,0,0.07); font-family: Inter, Arial, sans-serif; max-width: 90%; margin-left: auto; margin-right: auto;">'
    table_html += '<table style="width:100%; border-collapse:collapse;">'
    table_html += '<thead><tr style="border-bottom:2px solid #eee;">'
    table_html += '<th style="padding:4px; text-align:left; font-size:0.9rem; color:#222;">Player</th>'
    table_html += '<th style="padding:4px; text-align:center; font-size:0.9rem; color:#222;">Time on Pitch (%)</th>'
    table_html += '<th style="padding:4px; text-align:center; font-size:0.9rem; color:#222;">Role</th>'
    table_html += '</tr></thead><tbody>'
    
    # Adiciona as linhas da tabela
    for _, row in df.iterrows():
        player_name = row['player_name']
        time_on_pitch = row['time_on_pitch_rate']
        role = row['topr_class']
        color = PLAYER_COLORS.get(role, '')
        
        table_html += f'<tr style="border-bottom:1px solid #eee;">'
        table_html += f'<td style="padding:4px; font-size:0.9rem; color:#222;">{player_name}</td>'
        table_html += f'<td style="padding:4px; text-align:center; font-size:0.9rem; color:#222;">{time_on_pitch}</td>'
        table_html += f'<td style="padding:4px; text-align:center; font-size:0.9rem; color:#222; background-color:{color};">{role}</td>'
        table_html += '</tr>'
    
    # Fecha a tabela
    table_html += '</tbody></table></div>'
    
    # Renderiza a tabela usando st.markdown com unsafe_allow_html=True
    st.markdown(table_html, unsafe_allow_html=True) 