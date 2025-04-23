import streamlit as st
import youtube_utils
import gemini_utils
from datetime import datetime
import time
from PIL import Image
import os

# Configuração da página
st.set_page_config(
    page_title="CARAVELS",
    page_icon="./imagens/logo3.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Customizado
def load_css():
    st.markdown(f"""
    <style>
        .main {{
            background-color: #121212;
            color: #8191AA;
        }}
        .stTextInput>div>div>input {{
            background-color: #1E1E1E;
            color: white;
        }}
        .stButton>button {{
            background: linear-gradient(90deg, #43e97b 0%, #38f9d7 100%);
            border: none;
            color: white;
            font-weight: bold;
            transition: all 0.3s;
        }}
        .stButton>button:hover {{
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(255, 75, 75, 0.4);
        }}
        .video-card {{
            background: #1E1E1E;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .progress-bar {{
            height: 5px;
            background: linear-gradient(90deg, #FF4B4B 0%, #FF8E53 100%);
            margin-top: 10px;
            border-radius: 5px;
        }}
    </style>
    """, unsafe_allow_html=True)

def main():
    load_css()

    # Caminho da imagem com base no local do script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.join(script_dir, "..", "imagens", "nova_busca.png")
    img = Image.open(img_path)

    # Convertendo a imagem para bytes base64
    import base64
    from io import BytesIO
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    encoded = base64.b64encode(buffer.getvalue()).decode()

    # Centralizando com HTML + CSS
    st.markdown(f"""
    <div style='display: flex; justify-content: center;'>
        <img src='data:image/png;base64,{encoded}' width='500'/>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar Elegante
    with st.sidebar:
        st.markdown("## Configurações")
        language = st.selectbox("Idioma preferido", ["Português", "Inglês", "Espanhol"])
        ai_model = st.radio("Modelo de IA", ["Gemini Flash", "Gemini Pro"])
        st.markdown("---")
        st.markdown("Desenvolvido por [Lucas de Souza Ferreira]")
    
    # Área Principal
    with st.container():
        url = st.text_input("", placeholder="Cole a URL do YouTube aqui...", key="url_input")
        
        if url:
            with st.spinner("Processando vídeo..."):
                progress_bar = st.empty()
                for percent_complete in range(100):
                    time.sleep(0.01)
                    progress_bar.progress(percent_complete + 1)
                
                try:
                    # Card do Vídeo
                    with st.container():
                        st.markdown('<div class="video-card">', unsafe_allow_html=True)
                        
                        video_id = youtube_utils.extract_video_id(url)
                        video_title = youtube_utils.get_video_title(url)
                        
                        if video_title:
                            st.markdown(f"### 🎬 {video_title}")
                            st.markdown(f"`📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}`")
                        
                        transcript = youtube_utils.get_transcript(video_id)
                        
                        if transcript:
                            # Abas Interativas
                            tab1, tab2, tab3 = st.tabs(["📝 Transcrição", "📊 Análise", "🎯 Resumo"])
                            
                            with tab1:
                                st.markdown("#### Transcrição Completa")
                                st.write(transcript)
                            
                            with tab2:
                                st.markdown("#### 🧠 Tema Principal do Vídeo")
                                if st.button("🔍 Analisar Tema"):
                                    with st.spinner("Analisando o conteúdo..."):
                                        gemini_utils.configure_gemini()
                                        prompt = f"Com base na transcrição abaixo, identifique o tema principal do vídeo em uma frase clara:\n\n{transcript}"
                                        theme = gemini_utils.generate_summary(prompt)
                                        if theme:
                                            st.success(f"🎯 Tema: {theme}")
                                        else:
                                            st.error("Não foi possível identificar o tema.")
                            
                            with tab3:
                                if st.button("✨ Gerar Resumo Premium"):
                                    with st.spinner("Criando resumo mágico..."):
                                        gemini_utils.configure_gemini()
                                        summary = gemini_utils.generate_summary(transcript)
                                        if summary:
                                            st.success(summary)
                                        else:
                                            st.error("Não foi possível gerar o resumo")
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                
                except Exception as e:
                    st.error(f"🚨 Erro: {str(e)}")

if __name__ == "__main__":
    main();