import streamlit as st
import os
import pandas as pd
from unidecode import unidecode
from .league_selector import img_to_base64

# Caminhos dos ficheiros
EQUIPAS_PATH = r'C:/Users/guica/OneDrive/Desktop/AppScout/assets/equipas'
EQUIPAS_CSV = r'C:/Users/guica/OneDrive/Desktop/ScoutingDash/data/processed/equipas.csv'
EQUIPAS_XLSX = r'C:/Users/guica/OneDrive/Desktop/ScoutingDash/data/processed/EquiposJP.xlsx'
COACHES_XLSX = r'C:/Users/guica/OneDrive/Desktop/ScoutingDash/data/processed/EntrenadoresJP.xlsx'
STADIUM_XLSX = r'C:/Users/guica/OneDrive/Desktop/ScoutingDash/data/processed/EstadioJP.xlsx'

def get_stadium_info(team_logo: str) -> dict:
    """
    Obtém informações do estádio para uma equipa.
    
    Args:
        team_logo (str): Logo da equipa
        
    Returns:
        dict: Dicionário com informações do estádio (nome, capacidade, localização)
    """
    try:
        df = pd.read_excel(STADIUM_XLSX)
        row = df[df['Logo'] == team_logo]
        if row.empty:
            return {'stadium': '-', 'capacity': '-', 'location': '-'}
        row = row.iloc[0]
        return {
            'stadium': row.get('Nombre Estadio', '-') or '-',
            'capacity': row.get('Capacidad Estadio', '-') or '-',
            'location': row.get('Ciudad', '-') or '-',
        }
    except Exception as e:
        return {'stadium': '-', 'capacity': '-', 'location': '-'}

def render_general_info(liga_nome: str, pais: str, team_logo: str):
    """
    Renderiza a secção de informações gerais da equipa.
    
    Args:
        liga_nome (str): Nome da liga
        pais (str): País da equipa
        team_logo (str): Logo da equipa
    """
    stadium_info = get_stadium_info(team_logo)
    info_fields = [
        ("Competition", liga_nome if liga_nome else '-'),
        ("Country", pais if pais else '-'),
        ("Stadium", stadium_info['stadium']),
        ("Capacity", stadium_info['capacity']),
        ("Location", stadium_info['location'])
    ]
    
    html_parts = [
        '<div style="margin-top:2.5rem; margin-bottom:1.5rem; padding: 24px 32px; background: #fff; border-radius: 16px; box-shadow: 0 2px 12px rgba(0,0,0,0.07); font-family: Inter, Arial, sans-serif;">',
        '<div style="font-size:1.35rem; font-weight:700; margin-bottom:18px; letter-spacing:0.2px;">General Info</div>',
        '<div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 16px; flex-wrap:wrap; overflow-wrap:anywhere;">'
    ]
    
    for label, value in info_fields:
        html_parts.append(
            f'<div style="min-width: 100px;">'
            f'<div style="font-size:0.95rem; color:#888; font-weight:600;">{label}</div>'
            f'<div style="font-size:1.05rem; color:#222; font-weight:700;">{value if value else '-'}</div>'
            f'</div>'
        )
    
    html_parts.append('</div></div>')
    info_html = ''.join(html_parts).replace('\n', '')
    st.markdown(info_html, unsafe_allow_html=True)

def render_coach_info(team_logo: str):
    """
    Renderiza a secção de informações do treinador.
    
    Args:
        team_logo (str): Logo da equipa
    """
    try:
        df = pd.read_excel(COACHES_XLSX)
        row = df[df['Logo'] == team_logo]
        if row.empty:
            st.warning("Coach data not available.")
            return
        
        coach = row.iloc[0]
        name = coach.get('Entrenador', '-')
        age = coach.get('Edad', '-')
        nationality = coach.get('Nacionalidad', '-')
        formation = coach.get('Formación Preferida', '-')
        experience = coach.get('Experiencia', '-')
        contract = coach.get('Contrato Hasta', '-')
        
        coach_html = f'''
        <div style="margin-top:2.5rem; margin-bottom:1.5rem; padding: 24px 32px; background: #fff; border-radius: 16px; box-shadow: 0 2px 12px rgba(0,0,0,0.07); font-family: 'Inter', Arial, sans-serif;">
            <div style="font-size:1.35rem; font-weight:700; margin-bottom:18px; letter-spacing:0.2px;">Coach Information</div>
            <div style="display:flex; flex-wrap:wrap; gap:32px;">
                <div style="min-width:180px; flex:1;">
                    <div style="font-size:1.08rem; color:#888; font-weight:600;">Name</div>
                    <div style="font-size:1.18rem; color:#222; font-weight:700;">{name}</div>
                </div>
                <div style="min-width:120px; flex:1;">
                    <div style="font-size:1.08rem; color:#888; font-weight:600;">Age</div>
                    <div style="font-size:1.18rem; color:#222; font-weight:700;">{age}</div>
                </div>
                <div style="min-width:160px; flex:1;">
                    <div style="font-size:1.08rem; color:#888; font-weight:600;">Nationality</div>
                    <div style="font-size:1.18rem; color:#222; font-weight:700;">{nationality}</div>
                </div>
                <div style="min-width:180px; flex:1;">
                    <div style="font-size:1.08rem; color:#888; font-weight:600;">Preferred Formation</div>
                    <div style="font-size:1.18rem; color:#222; font-weight:700;">{formation}</div>
                </div>
                <div style="min-width:160px; flex:1;">
                    <div style="font-size:1.08rem; color:#888; font-weight:600;">Experience</div>
                    <div style="font-size:1.18rem; color:#222; font-weight:700;">{experience}</div>
                </div>
                <div style="min-width:180px; flex:1;">
                    <div style="font-size:1.08rem; color:#888; font-weight:600;">Contract Expiration</div>
                    <div style="font-size:1.18rem; color:#222; font-weight:700;">{contract}</div>
                </div>
            </div>
        </div>
        '''
        st.markdown(coach_html, unsafe_allow_html=True)
    except Exception as e:
        st.warning("Coach data not available.")

def render_team_header(selected_league: str, selected_team: str):
    """
    Renderiza o cabeçalho completo da equipa com todas as informações.
    
    Args:
        selected_league (str): Nome da liga selecionada
        selected_team (str): Logo da equipa selecionada
    """
    # Botão voltar
    if st.button('← Back', key='voltar_equipas'):
        st.session_state['team_selected'] = None
        st.rerun()
    
    # Caminho do logo
    logo_path = os.path.join('assets', 'equipas', selected_league, selected_team)
    
    # Nome oficial da equipa
    nome_oficial = None
    try:
        df = pd.read_csv(EQUIPAS_CSV)
        row = df[df['Logo'] == selected_team]
        if not row.empty:
            nome_oficial = row.iloc[0]['Original_Eventing']
    except Exception as e:
        nome_oficial = None
    
    # País da equipa
    pais = None
    try:
        df_xlsx = pd.read_excel(EQUIPAS_XLSX)
        row_xlsx = df_xlsx[df_xlsx['Logo'] == selected_team]
        if not row_xlsx.empty:
            pais = row_xlsx.iloc[0]['Country']
    except Exception as e:
        pais = None
    
    # Verifica se o logo existe
    if not os.path.exists(logo_path):
        st.warning('Logo da equipa não encontrado.')
        return
    
    # Renderiza o logo e nome da equipa
    img_b64 = img_to_base64(logo_path)
    if nome_oficial is None:
        st.warning('Nome oficial da equipa não encontrado no CSV.')
        nome_oficial = selected_team.replace('.png', '')
    if pais is None:
        pais = '-'
    
    # HTML do cabeçalho
    header_html = f'''
        <div class="team-header">
            <img src="data:image/png;base64,{img_b64}" class="team-logo" alt="{nome_oficial}"/>
            <div class="team-info-block">
                <div class="team-name-row">
                    <span class="team-name">{nome_oficial}</span>
                </div>
            </div>
        </div>
    '''
    st.markdown(header_html, unsafe_allow_html=True)
    
    # Renderiza as informações gerais e do treinador
    render_general_info(selected_league, pais, selected_team)
    render_coach_info(selected_team)
