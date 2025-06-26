import streamlit as st
import os
from .league_selector import img_to_base64

def render_team_selector(selected_league: str):
    """
    Renderiza o seletor de equipas para uma liga específica.
    
    Args:
        selected_league (str): Nome da liga selecionada
        
    Returns:
        str: Logo da equipa selecionada ou None se nenhuma selecionada
    """
    # Caminho do diretório de equipas da liga
    equipas_dir = os.path.join(r'C:/Users/guica/OneDrive/Desktop/AppScout/assets/equipas', selected_league)
    
    # Lista de imagens de equipas
    equipas_imgs = [f for f in os.listdir(equipas_dir) if f.endswith('.png')]
    n = len(equipas_imgs)
    
    if n == 0:
        st.warning('Nenhuma equipa encontrada para esta liga.')
        return None
    
    # Calcula o número de colunas e linhas
    n_cols = 4
    n_rows = (n + n_cols - 1) // n_cols
    
    # Índice para percorrer as imagens
    idx = 0
    
    # Renderiza os botões em grade
    for linha in range(n_rows):
        cols = st.columns(n_cols, gap="large")
        for col_idx in range(n_cols):
            if idx < n:
                team_logo = equipas_imgs[idx]
                img_path = os.path.join(equipas_dir, team_logo)
                img_b64 = img_to_base64(img_path)
                
                # HTML do botão com a imagem
                btn_html = f'''
                    <button class="equipa-btn" type="button" tabindex="-1" disabled>
                        <img src="data:image/png;base64,{img_b64}" class="equipa-img-btn" alt="{team_logo}"/>
                    </button>
                '''
                
                with cols[col_idx]:
                    team_name = team_logo.replace('.png', '')
                    if st.button(team_name, key=f"equipa_{selected_league}_{team_logo}", use_container_width=True):
                        st.session_state['team_selected'] = team_logo
                    st.markdown(btn_html, unsafe_allow_html=True)
                idx += 1
    
    # Botão para voltar às ligas
    if st.button('Back to Leagues'):
        st.session_state['league_selected'] = None
        st.session_state['team_selected'] = None
        return None
    
    return st.session_state.get('team_selected')
