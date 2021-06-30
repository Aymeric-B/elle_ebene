import streamlit as st
import requests
from collections import Counter
from PIL import Image
import sys
sys.path.insert(0, '..')
from elle_ebene.predict import baseline

st.markdown("""# Découvrez le type de votre chevelure""")

result_list = []

# Upload images
for i in range(3):
    
    uploaded_file = st.file_uploader("Choisissez une photo (png ou jpg)",
                                     type=['png', 'jpg', 'jpeg'],
                                     key=f"image{i}")

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        result = baseline(image)
        result_list.append(result)
        st.image(image)

if st.button("Lancez la recherche"):

    if len(result_list) == 3:

        def most_frequent(liste):
            count_occurence = Counter(liste)
            return count_occurence.most_common(1)[0][0]

        res = most_frequent(result_list)
        
        if res == 0:
            result = "type 3"
        else:
            result = "type 4"
            
        st.write("Votre chevelure est de ", result)
        
    else:
        st.write(f'Il manque {3-len(image_list)} photo(s). Veuillez en télécharger')
    