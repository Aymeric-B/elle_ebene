import streamlit as st
from collections import Counter
from PIL import Image, ExifTags
import sys
sys.path.insert(0, '..')
from elle_ebene.predict import prediction

def most_frequent(liste):
    count_occurence = Counter(liste)
    return count_occurence.most_common(1)[0][0]

logo = Image.open('Website/logo.png')
st.image(logo, output_format='PNG')
st.write("-> [Notre site](https://elleebene.com/)")
st.markdown("""# Découvrez le type de votre chevelure""")

result_list = []
image_list = []
rotation = {1: 0, 3: 180, 6: 270, 8: 90}
visage = ['face', 'profil', 'dos']
commentaire = ["Prenez une photo de votre visage bien encadré par vos cheveux",
               "N'attachez pas vos cheveux",
               "Présentez bien toute l'envergure de vos cheveux"]
        
# Upload images
st.sidebar.markdown("""## Téléchargez vos photos :""")
for i in range(3):
    
    uploaded_file = st.sidebar.file_uploader(f"Photo de {visage[i]}",type=['png', 'jpg', 'jpeg'],
                                     key=f"image{i}", help=f"{commentaire[i]}")
    
    if uploaded_file is not None:
        
        image = Image.open(uploaded_file)
        
        # Hide filename on UI
        st.markdown('''<style>.uploadedFile {display: none}<style>''', unsafe_allow_html=True)
        
        exif = image.getexif()
        if exif != None:
            exif = {ExifTags.TAGS[k]: v
                    for k, v in image.getexif().items()
                    if k in ExifTags.TAGS}
            if exif != {}:
                image = image.rotate(rotation[exif.get('Orientation', 1)], expand=True)
        
        image_list.append(image)
        
        #width, height = image.size
        #width, height = int(width*300/height), 300
        #image = image.resize((width, height))
        
        #st.image(image)

st.image(image_list, width=232)

if st.button("Lancez la recherche"):

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
        
        st.balloons()
        
    else:
        
        st.error(f'Il manque {3-len(image_list)} photo(s). Veuillez en télécharger')
        