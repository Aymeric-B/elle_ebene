import streamlit as st
from collections import Counter
from PIL import Image
import sys
sys.path.insert(0, '..')
from elle_ebene.predict import prediction

st.markdown("""# Découvrez le type de votre chevelure""")

result_list = []
image_list = []
titres = []
            
def most_frequent(liste):
    count_occurence = Counter(liste)
    return count_occurence.most_common(1)[0][0]

# Upload images
with st.form("Formulaire de saisie", clear_on_submit=True):
    
    st.write("Veuillez entrer vos photos :")
    
    uploaded_file_1 = st.file_uploader('',type=['png', 'jpg', 'jpeg'],
                                     key=f"image1")
    if uploaded_file_1 is not None:
        image1 = Image.open(uploaded_file_1)
        image_list.append(image1)
        st.image(image1)
    
    uploaded_file_2 = st.file_uploader('',type=['png', 'jpg', 'jpeg'],
                                     key=f"image2")
 
    if uploaded_file_2 is not None:
        image2 = Image.open(uploaded_file_2)
        image_list.append(image2)
        st.image(image2)
    
    uploaded_file_3 = st.file_uploader('',type=['png', 'jpg', 'jpeg'],
                                     key=f"image3")

    if uploaded_file_3 is not None:
        image3 = Image.open(uploaded_file_3)
        image_list.append(image3)
        st.image(image3)

    # Every form must have a submit button.
    submitted = st.form_submit_button("Lancez la recherche")

if submitted:
    
    if len(image_list) == 3:
        
        result_list = [prediction(image) for image in image_list]

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
        st.error(f'Il manque {3-len(image_list)} photo(s). Veuillez compléter')

        