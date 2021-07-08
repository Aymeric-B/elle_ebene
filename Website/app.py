import streamlit as st
from collections import Counter
from PIL import Image, ExifTags
import sys
sys.path.insert(0, '..')
from elle_ebene.predict import prediction

# Count most frequent value in a list
def most_frequent(liste):
    count_occurence = Counter(liste)
    return count_occurence.most_common(1)[0][0]

# Page formatting
st.set_page_config(layout="wide")
st.markdown(f"""<style>
                .reportview-container .main .block-container{{
                    padding-top: 5px}}
                .reportview-container .css-yleahc {{
                    padding-top:20px}}
                </style>""", unsafe_allow_html=True)

# Display title and logo
logo = Image.open('Website/logo.png')
st.image(logo, output_format='PNG')
st.markdown("""# Découvrez le type de votre chevelure""")

# Prepare image uploading
result = ''
image_list = []
rotation = {1: 0, 3: 180, 6: 270, 8: 90}
visage = ['face', 'profil', 'dos']
titres =[f'Photo de {side}' for side in visage]
commentaires = ["Prenez une photo de votre visage bien encadré par vos cheveux",
               "N'attachez pas vos cheveux",
               "Présentez bien toute l'envergure de vos cheveux"]

# Upload images in sidebar
st.sidebar.markdown("""## Téléchargez vos photos :""")
for i in range(3):
    
    uploaded_file = st.sidebar.file_uploader(titres[i],type=['png', 'jpg', 'jpeg'],
                                     key=titres[i], help=f"{commentaires[i]}")
    
    if uploaded_file is not None:
        
        image = Image.open(uploaded_file)
        
        # Hide filename on UI
        st.markdown('''<style>.uploadedFile {display: none}<style>''', unsafe_allow_html=True)
        
        # Prepare images to be displayed according to photo EXIF data
        exif = image.getexif()
        if exif != None:
            exif = {ExifTags.TAGS[k]: v
                    for k, v in image.getexif().items()
                    if k in ExifTags.TAGS}
            if exif != {}:
                image = image.rotate(rotation[exif.get('Orientation', 1)], expand=True)
        
        image_list.append(image)

# Display bottom sidebar information
basdepage = Image.open('Website/basdepage.png')
st.sidebar.image(basdepage, output_format='PNG')
st.sidebar.write("    -> [Notre site](https://elleebene.com/)")

# Launch prediction
if st.button("Lancez la recherche"):

    if len(image_list) == 3:

        # Prediction on each image and vote
        result_list = [prediction(image) for image in image_list]
        res = most_frequent(result_list)
        
        # Display preparation
        if res == 0:
            result = "type 3"
        else:
            result = "type 4"
        chevelure = "Votre chevelure est de " + result
          
        # Display result
        if sum(result_list) == 0 or sum(result_list) == 3:
            st.success(chevelure)   
        else:
            st.warning(chevelure)
        
    else:
        
        st.error(f'Il manque {3-len(image_list)} photo(s). Veuillez en télécharger')

# Display uploaded images
st.image(image_list, width=312)

if len(image_list) == 3 and result != '':
    # Display hair segmentation types
    typologie = Image.open('Website/curls_large.jpeg')
    st.image(typologie, output_format='JPEG')

