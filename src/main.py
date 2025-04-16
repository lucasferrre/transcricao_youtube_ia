import sys
import os
import streamlit as st  # estava escrito "stramlit"
import youtube_utils
import gemini_utils

# Adiciona o diretório 'src' ao caminho do Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

def main():
    st.title("Transcrição do YouTube do Lukinhas")
    
    video_url = st.text_input("Insira a URL do vídeo do YouTube", "https://www.youtube.com/shorts/ALMKwp4WXTk")
    
    if video_url:
        try:
            video_id = youtube_utils.extract_video_id(video_url)
            video_title = youtube_utils.get_video_title(video_url)
            transcript = youtube_utils.get_transcript(video_id)
            
            if video_title:
                st.subheader(f"Título do vídeo: {video_title}")
            
            if transcript:
                st.subheader("Transcrição:")
                st.write(transcript)
                
                if st.button("Gerar Resumo com Gemini"):
                    gemini_utils.configure_gemini()  # Busca do .env
                    summary = gemini_utils.generate_summary(transcript)

                    if summary:
                        st.subheader("Resumo Gerado por Gemini:")
                        st.write(summary)
                    else:
                        st.error("Falha ao gerar o resumo com Gemini.")
            else:
                st.error("Não foi possível obter a transcrição do vídeo.")
        
        except Exception as e:
            st.error(f"Ocorreu um erro: {e}") 

if __name__ == "__main__":
    main()  
