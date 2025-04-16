from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi

def get_video_title(video_url):
    """Extrai o título de um vídeo do YouTube."""
    try:
        yt = YouTube(video_url)
        return yt.title
    except Exception as e:
        print(f"Erro ao obter o título do vídeo: {e}")
        return None
    
def get_transcript(video_id):
    """Obtém a transcrição de um vídeo do YouTube, priorizando português."""
    try:
        # Tenta primeiro pegar em português (pt)
        transcript = YouTubeTranscriptApi.get_transcript(
            video_id,
            languages=['pt', 'pt-BR', 'en']  # Ordem de prioridade
        )
        return ' '.join([entry['text'] for entry in transcript])
    except Exception as e:
        print(f"Erro ao obter a transcrição: {e}")
        return None
    
def extract_video_id(url):
    """Extrai o ID do vídeo da URL do YouTube."""
    try:
        yt = YouTube(url)
        return yt.video_id  # Corrigido para retornar o ID correto
    except Exception as e:
        print(f"Erro ao extrair o ID do vídeo: {e}")
        return None

if __name__ == "__main__":
    # Teste apenas quando executado diretamente
    video_url = "https://www.youtube.com/shorts/ALMKwp4WXTk"
    
    title = get_video_title(video_url)
    print(f"Título do vídeo: {title}")

    video_id = extract_video_id(video_url)
    print(f"ID do vídeo: {video_id}")

    transcript = get_transcript(video_id)
    print(f"Transcrição do vídeo: {transcript}")
    