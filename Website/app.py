import streamlit as st
import requests
from collections import Counter
from PIL import Image
import sys
sys.path.insert(0, '..')
from elle_ebene.predict import baseline

st.markdown("""# Découvrez le type de votre chevelure""")

result_list = []
image_list = []
titres = []

# Upload images
for i in range(3):
    
    uploaded_file = st.file_uploader("Choisissez une photo (png ou jpg)",
                                     type=['png', 'jpg', 'jpeg'],
                                     key=f"image{i}")

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        result = baseline(image)
        st.write(result)
        result_list.append(result)
        image_list.append(image)
        titres.append(f"image{i+1}")
        st.image(image)
        
#st.image(image_list, width=200, caption=titres)

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
        
        chevelure = "Votre chevelure est de " + result    
        
        if sum(result_list) == 0 or sum(result_list) == 3:
            st.success(chevelure)
        else:
            st.warning(chevelure)
        
    else:
        st.error(f'Il manque {3-len(image_list)} photo(s). Veuillez en télécharger')
        
    st.write(result_list)
    