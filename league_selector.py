import streamlit as st
import os
import base64

# Caminho para as imagens das ligas
LIGAS_PATH = r'C:/Users/guica/OneDrive/Desktop/AppScout/assets/ligas'

# Lista de ligas e respetivas imagens
LEAGUES = [
    'Premier League.png',
    'La Liga.png',
    'Bundesliga.png',
    'Serie A.png',
    'Ligue 1.png',
    'Primeira Liga.png',
    'Eredivisie.png',
    'Belgian Pro League.png',
    'EFL Championship.png',
    'Segunda Division.png',
]

def img_to_base64(img_path):
    """Converte uma imagem para base64."""
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def render_league_selector():
    """
    Renderiza o seletor de ligas com os botões e imagens.
    Atualiza o session_state['league_selected'] quando uma liga é selecionada.
    
    Returns:
        str: Nome da liga selecionada ou None se nenhuma liga foi selecionada
    """
    selected_league = None

    # Texto condicional abaixo do título
    if st.session_state.get('league_selected') is None:
        st.markdown('<div style="margin-bottom:2.2rem;font-size:1.2rem;">Select a league to start:</div>', unsafe_allow_html=True)

    # Renderiza os botões das ligas em uma grade 2x5
    for linha in range(2):
        cols = st.columns(5, gap="large")
        for col_idx in range(5):
            idx = linha * 5 + col_idx
            if idx < len(LEAGUES):
                liga_img = LEAGUES[idx]
                img_path = os.path.join(LIGAS_PATH, liga_img)
                liga_nome = liga_img.replace('.png', '')
                img_b64 = img_to_base64(img_path)

                # HTML do botão com a imagem
                btn_html = f'''
                    <button class="liga-btn" type="button" tabindex="-1" disabled>
                        <img src="data:image/png;base64,{img_b64}" class="liga-img-btn" alt="{liga_nome}"/>
                    </button>
                '''

                with cols[col_idx]:
                    # 🔧 key única prefixada com 'seleciona_liga_'
                    if st.button(liga_nome, key=f"seleciona_liga_{liga_nome}", use_container_width=True):
                        selected_league = liga_nome
                        st.session_state['league_selected'] = liga_nome
                        st.session_state['team_selected'] = None
                    st.markdown(btn_html, unsafe_allow_html=True)

    return selected_league

