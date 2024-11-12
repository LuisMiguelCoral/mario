# import streamlit as st
# from PIL import Image
# import numpy as np

# def aplicar_correcao_gamma(imagem, gamma):
#     img_normalizada = imagem / 255.0
#     img_corrigida = np.power(img_normalizada, gamma)
#     return (img_corrigida * 255).astype(np.uint8)

# def ajustar_luminancia(imagem, fator):
#     return np.clip(imagem * fator, 0, 255).astype(np.uint8)

# st.title("Imagens em Tons de Cinza com Ajustes de Luminância e Correção Gamma")

# arquivo_carregado = st.file_uploader("Escolha um arquivo", type=["jpg", "jpeg", "png"])

# if arquivo_carregado is not None:
#     imagem = Image.open(arquivo_carregado)
#     st.image(imagem, caption="Imagem Original", use_column_width=True)

#     img_rgb = imagem.convert('RGB')
#     img_array = np.array(img_rgb)
    
#     img_cinza = 0.2989 * img_array[..., 0] + 0.5870 * img_array[..., 1] + 0.1140 * img_array[..., 2]

#     media_canais = np.mean(img_array, axis=2)
    
#     gamma = st.slider("Selecione o valor de Gamma", 0.1, 3.0, 1.0)
#     img_corrigida = aplicar_correcao_gamma(img_cinza, gamma)
    
#     imagem_cinza = Image.fromarray(img_corrigida)

#     st.subheader("Imagem em Tons de Cinza com Correção Gamma")
#     st.image(imagem_cinza, use_column_width=True)

#     fator_luminancia = st.slider("Ajustar Luminância", 0.0, 3.0, 1.0)
#     img_ajustada = ajustar_luminancia(img_cinza, fator_luminancia)

#     imagem_ajustada = Image.fromarray(img_ajustada.astype(np.uint8))
#     st.subheader("Imagem com Luminância Ajustada")
#     st.image(imagem_ajustada, use_column_width=True)
    
#     imagem_media = Image.fromarray(media_canais.astype(np.uint8))
#     st.subheader("Média dos Canais (R, G, B)")
#     st.image(imagem_media, use_column_width=True)
import streamlit as st
from PIL import Image, ImageOps
import numpy as np
import matplotlib.pyplot as plt

def grayscale_average(image):
    """Converte a imagem para tons de cinza usando a média dos canais."""
    return ImageOps.grayscale(image)

def grayscale_perceptual(image):
    """Converte a imagem para tons de cinza usando uma ponderação perceptual."""
    img_array = np.array(image)
    r, g, b = img_array[:, :, 0], img_array[:, :, 1], img_array[:, :, 2]
    gray = 0.299 * r + 0.587 * g + 0.114 * b
    return Image.fromarray(gray.astype(np.uint8))

def grayscale_improved(image):
    """Converte a imagem para tons de cinza aplicando correção gama e uma ponderação perceptual."""
    img_array = np.array(image) / 255.0
    gamma_corrected = np.power(img_array, 2.2)
    weighted = gamma_corrected @ [0.299, 0.587, 0.114]
    return Image.fromarray((weighted**(1/2.2) * 255).astype(np.uint8))

def binarize(image, threshold):
    """Binariza a imagem com base em um valor de limiar."""
    bin_img = image.point(lambda p: p > threshold and 255)
    return bin_img

def interval_threshold(image, low, high):
    """Aplica um threshold intervalado na imagem."""
    interval_img = image.point(lambda p: 255 if low < p < high else 0)
    return interval_img

st.title("Image Processing Application")
uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_image:
    img = Image.open(uploaded_image)
    st.image(img, caption="Original Image", use_column_width=True)
    
    st.write("### Grayscale Conversions Side by Side")
    
    gray_avg = grayscale_average(img)
    gray_perceptual = grayscale_perceptual(img)
    gray_improved = grayscale_improved(img)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.image(gray_avg, caption="Grayscale Average", use_column_width=True)
    with col2:
        st.image(gray_perceptual, caption="Grayscale Perceptual", use_column_width=True)
    with col3:
        st.image(gray_improved, caption="Grayscale Improved", use_column_width=True)
    
    st.write("### Histogram for Grayscale Average")
    hist = np.array(gray_avg).flatten()
    fig, ax = plt.subplots()
    ax.hist(hist, bins=256, range=(0, 256), color="gray")
    ax.set_title("Histogram")
    st.pyplot(fig)

    st.write("### Additional Processing")
    operation = st.selectbox("Select Operation", ("Binarization", "Interval Threshold"))
    mode = st.selectbox("Apply to", ("Color", "Grayscale Average", "Grayscale Perceptual", "Grayscale Improved"))
    
    if mode == "Color":
        selected_image = img
    elif mode == "Grayscale Average":
        selected_image = gray_avg
    elif mode == "Grayscale Perceptual":
        selected_image = gray_perceptual
    else:
        selected_image = gray_improved

    if operation == "Binarization":
        threshold = st.slider("Select threshold", 0, 255, 128)
        bin_img = binarize(selected_image.convert("L") if mode == "Color" else selected_image, threshold)
        st.image(bin_img, caption="Binarized Image", use_column_width=True)
    
    elif operation == "Interval Threshold":
        low = st.slider("Select lower threshold", 0, 255, 50)
        high = st.slider("Select upper threshold", 0, 255, 200)
        interval_img = interval_threshold(selected_image.convert("L") if mode == "Color" else selected_image, low, high)
        st.image(interval_img, caption="Interval Threshold Image", use_column_width=True)

