import os
from pathlib import Path
from django.conf import settings
from typing import Optional

def get_relative_path(full_path: Path | str, base_path: Path | str) -> Optional[Path]:
    """
    Calcula o caminho de 'full_path' relativo a 'base_path' de forma segura.
    """
    try:
        file_path = Path(full_path)
        base = Path(base_path)
        return file_path.relative_to(base)
    except ValueError:
        return None


def salvar_imagem_em_pasta(nome_da_pasta: str, nome_do_arquivo: str, dados_da_imagem: bytes) -> Optional[str]:
    """
    Salva dados de imagem binários em uma subpasta dentro do MEDIA_ROOT.
    
    Retorna o caminho relativo do arquivo salvo em caso de sucesso, ou None em caso de erro.
    """
    try:
        # Define o caminho base para salvar as imagens
        media_root = Path(settings.MEDIA_ROOT)
        
        # Garante que MEDIA_ROOT existe
        os.makedirs(media_root, exist_ok=True)
        
        # Cria a subpasta para o evento
        pasta_destino = os.path.join(media_root, nome_da_pasta)
        os.makedirs(pasta_destino, exist_ok=True)
        
        # Define o caminho completo do arquivo
        caminho_completo = os.path.join(pasta_destino, nome_do_arquivo)
        
        # Salva os dados binários no arquivo
        with open(caminho_completo, 'wb') as f:
            f.write(dados_da_imagem)
        
        # Retorna o caminho relativo à MEDIA_ROOT
        return os.path.join(nome_da_pasta, nome_do_arquivo)
    except Exception as e:
        print(f"Erro ao salvar a imagem: {e}")
        return None