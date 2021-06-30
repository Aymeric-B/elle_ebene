import streamlit as st
import requests
from collections import Counter
from PIL import Image

st.markdown("""# Découvrez le type de votre chevelure""")

image_list = []

# Upload images
for i in range(3):
    
    uploaded_file = st.file_uploader("Choisissez une photo (png ou jpg)", type=['png', 'jpg', 'jpeg'], key=f"image{i}")

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        image_list.append(image)
        st.image(image)

# API url on GCP
# url = 'A récupérer'

# result_list = []

# for img in image_list:

#     params = {'image': img}  
#     result = requests.get(url, params=params).json().get('prediction', 'type inconnu')
#     result_list.append(result)

# def most_frequent(liste):
#     count_occurence = Counter(liste)
#     return count_occurence.most_common(1)[0][0]

# result = most_frequent(result_list)
    

# st.write("Votre chevelure est de ", result)