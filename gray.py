import streamlit as st
from PIL import Image
import numpy as np

def aplicar_correcao_gamma(imagem, gamma):
    img_normalizada = imagem / 255.0
    img_corrigida = np.power(img_normalizada, gamma)
    return (img_corrigida * 255).astype(np.uint8)

def ajustar_luminancia(imagem, fator):
    return np.clip(imagem * fator, 0, 255).astype(np.uint8)

st.title("Imagens em Tons de Cinza com Ajustes de Luminância e Correção Gamma")

arquivo_carregado = st.file_uploader("Escolha um arquivo", type=["jpg", "jpeg", "png"])

if arquivo_carregado is not None:
    imagem = Image.open(arquivo_carregado)
    st.image(imagem, caption="Imagem Original", use_column_width=True)

    img_rgb = imagem.convert('RGB')
    img_array = np.array(img_rgb)
    
    img_cinza = 0.2989 * img_array[..., 0] + 0.5870 * img_array[..., 1] + 0.1140 * img_array[..., 2]

    media_canais = np.mean(img_array, axis=2)
    
    gamma = st.slider("Selecione o valor de Gamma", 0.1, 3.0, 1.0)
    img_corrigida = aplicar_correcao_gamma(img_cinza, gamma)
    
    imagem_cinza = Image.fromarray(img_corrigida)

    st.subheader("Imagem em Tons de Cinza com Correção Gamma")
    st.image(imagem_cinza, use_column_width=True)

    fator_luminancia = st.slider("Ajustar Luminância", 0.0, 3.0, 1.0)
    img_ajustada = ajustar_luminancia(img_cinza, fator_luminancia)

    imagem_ajustada = Image.fromarray(img_ajustada.astype(np.uint8))
    st.subheader("Imagem com Luminância Ajustada")
    st.image(imagem_ajustada, use_column_width=True)
    
    imagem_media = Image.fromarray(media_canais.astype(np.uint8))
    st.subheader("Média dos Canais (R, G, B)")
    st.image(imagem_media, use_column_width=True)
