import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import pathlib as Path
import numpy as np
import base64
import requests
import json
from gaiacare_front.predict import Predict
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import array_to_img

import walis_net as hc
import datetime
st.set_page_config(layout='wide')


padding = 0
st.markdown(f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style> """, unsafe_allow_html=True)


#LOADING MODEL
@st.cache(allow_output_mutation=True)
def retrieve_model():
    PATH_MODEL = 'walid_VGG16-lr0-0001_datagen.h5'
    model = load_model(PATH_MODEL)
    return model

model = retrieve_model()


CSS = """
    .css-12gp8ed {
        color: #3F545B;
        height: 2rem;

    }
    .css-12gp8ed a{
        display: none;
    }
    .spacer {
        height: 1.8rem;
        display: block;
        width:100%;
    }

     .title  {
    padding-top: 0 !important;
    font-family: "Open Sans", sans-serif;
    font-size:3rem;
    font-weight: 500;
    color: #3F545B;
    margin: 0px;
    line-height: 1.4;
    text-align:center;
    letter-spacing:0.2rem;

    }

    .titlec {
    background-color: rgba(143, 193, 180, 0.4);
    width: 17rem;
    margin:auto;
    #border-radius: 0.2rem;
    }

    .exg6vvm0 {
    font-family: 'Playfair Display', serif;
    width: 80%;
    margin: auto; }

    .stImage img{
    display: inline-block;
    }

    .popup {
    width: 40%;
    margin: 0 auto;
    background: #000;
    padding: 35px;
    border: 2px solid #fff;
    border-radius: 20px/50px;
    background-clip: padding-box;
    text-align: center;
        }


    .css-qrbaxs {
    display: none;
    }

    .logo {
    display:flex;
    width: 100%;
    justify-content:center;
    padding-top: 2rem;
    }

    .logo img {
    width:5rem !important;
    margin:auto;}

    .css-fis6aj {
        display: none;}


    body {
    color: #CEE5D0 !important;}




    .stApp {
    # background: #CEE5D0 !important;
    # background-color:  #004029!important;
    background-color: #3F545B;
    #background-color: #fff;}

    .block-container {
    background-color: #fff !important;
    margin-top: 4rem !important;
    margin-left:20% !important;
    margin-right:20% !important;
    padding-left: 0 !important;
    padding-right: 0 !important;
    border-radius: 0.2rem;
        }
    .css-18e3th9{
        width: 80%;
    }
    .navbar-collapse {
        display: none;
    }

    :root {
    --menu_background: #000 !important;

    }

    .navbar-mainbg {
        background-color: #000 !important;
    }

    .css-po3vlj {
    background-color: rgb(240, 242, 246);
    margin-bottom: 2rem;
    }




"""

st.write(f'<style>{CSS}</style>', unsafe_allow_html=True)



file_ = open("logo.png", "rb")
contents = file_.read()
logo_url = base64.b64encode(contents).decode("utf-8")
file_.close()

st.markdown(
    f'<div class="titlec"><div class="logo"><img src="data:image/png;base64,{logo_url}"></div></div>',
    unsafe_allow_html=True,
)



st.markdown("""

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display&display=swap" rel="stylesheet">

<div class='titlec'>
<h1 class="title">GaïaCare</h1>
</div>

<div class='spacer'></div>
<div class='spacer'></div>



""", unsafe_allow_html=True)

















#TOPBAR







#make it look nice from the start


# specify the primary menu definition
menu_data = [
    {'icon': "fa fa-home", 'label':"Accueil"},
    {'icon': "fa fa-heartbeat", 'label':"Diagnostic"},
    {'icon':"fa fa-cut",'label':"Segmentation"},
    {'icon': "fa fa-users", 'label':"A propos"}]

over_theme = {'txc_inactive': '#FFFFFF', 'menu_background' : '#3F545B'}
menu_id = hc.nav_bar(
    menu_definition=menu_data,
    override_theme=over_theme,
    #home_name='Home',
    hide_streamlit_markers=True, #will show the st hamburger as well as the navbar now!
    sticky_nav=False, #at the top or not
    sticky_mode='pinned', #jumpy or not-jumpy, but sticky or pinned
)

if menu_id == 'Accueil':


    components.html("""
        <div class='wrap'>
        <div class='spacer'></div>

      <p class='texte'> GaiaCare est une plateforme de diagnostic instantané
        qui vous aide dans la culture de vos plantes.
        </p>

        <div class='colcontain'>
        <col1 class='col1'>
        <p class='texte'> <span> 16 </span> </p>
        <p class='texte'> maladies reconnues </p>

        </col1>

        <col1 class='col1'>
        <p class='texte'><span> 98%  </span> </p>
        <p class='texte'> de précision </p>
        </col1>


        <col1 class='col1'>
        <p class='texte'> <span>10</span> </p>
        <p class='texte'> plantes différentes</p>
        </col1>
        </div>



        <p class='texte'>  Avec 98% de précision  l'application
        reconnait plus de 16 maladies différentes
        sur 10 espèces de plantes alimentaires. Un partenaire idéal pour
        tout les agriculteurs.
        </p>


        <div class='spacer'></div>


        </div>
        </div>

        <style>
        .spacer {
            height: 1.5rem;
            display: block;
            width:100%;
        }

    .col1 span {
            font-size: 2rem; }

        .texte {
            font-family: 'Playfair Display', serif;}

        .col1 {
            width: 30%;
            flex-grow: 1;
            display: inline-block !important;}

        .item + .item {
            margin-left: 4%;}

        .colcontain {
        display: flex;
        padding-left: 15%;
        padding-right: 15%;
        }


        .wrap {
        #background-color:  #004029!important;
        #background-color: #e7fee0 !important;
        background-color: rgba(143, 193, 180, 0.4);

        border-radius: 0.3rem;
        color: #3F545B;
        text-align: center;

        padding-left: 5%;
        padding-right: 5%;
        width:70%;
        margin: auto;
            }



        </style>



            """,
                        height=450)


if menu_id == 'Diagnostic':
    components.html("""
    <div class='wrap'>
    <div class='spacer'></div>



    <p class='texte' style='padding:1rem;'> En une photo et
    un clique, prenez connaissance
    de la santé de vos plantes, et bénéficiez d’un diagnostic
    en l’espace de quelques secondes. Il vous suffit juste de transverser
    une photo claire d’une feuille de votre plante et d’attendre le résultat
    quelques secondes. C’est aussi simple que ça!</p>

    <div class='spacer'></div>



    </div>
    </div>

    <style>
    .spacer {
        height: 1.5rem;
        display: block;
        width:100%;
    }

  .col1 span {
        font-size: 2rem; }

    .texte {
        font-family: 'Playfair Display', serif;}

    .col1 {
        width: 20%;
        flex-grow: 1;
        display: inline-block !important;}

    .item + .item {
        margin-left: 4%;}

    .colcontain {
            display: flex;}


    .wrap {
        #background-color:  #004029!important;
        #background-color: #e7fee0 !important;
        background-color: rgba(143, 193, 180, 0.4);

        border-radius: 0.3rem;
        color: #3F545B;
        text-align: center;

        padding-left: 5%;
        padding-right: 5%;
        width:70%;
        margin: auto;

        }



    </style>



        """,
                    height=200)


    #PREDICTION


    st.set_option('deprecation.showfileUploaderEncoding', False)

    uploaded_file = st.file_uploader("", type=['png','jpeg','jpg'])


    if uploaded_file is not None:

        #open image and convert to RGB
        test_pic = Image.open(
            uploaded_file
        ).convert('RGB')
        #turn to array
        test_pic = test_pic.resize((256,256))

        test_pic_array = np.array(test_pic)
        #switch to U-Int 8
        #test_pic_array = test_pic_array.astype('uint8')
        #memorizing shape
        #height, width, channel = test_pic_array.shape
        #reshape
        #test_pic_array = test_pic_array.reshape(height * width * channel)
        # encoding to b64
        #b64bytes = base64.b64encode(test_pic_array)
        #decoding to utf8 and turning to  string
        #b64str = b64bytes.decode('utf8').replace("'", '"')
        #image_dict = {
        #    'image': b64str,
        #    'height': height,
        #    'width': width,
        #    'channel': channel
        #}
        #headers = {'Content_Type': 'application/json'}

        #newjson = json.dumps(image_dict)
        #response = requests.post('https://dummy-gaia-api-ndgviyvkja-ew.a.run.app/predict_grad_cam',
        #    newjson,
        #    headers=headers).json()

        #decoded = base64.b64decode(bytes(response['image'], 'utf-8'))
        #decoded = np.frombuffer(decoded, dtype='float32')
        #decoded = decoded.reshape(response['height'], response['width'], response['channel'])
        #decoded = decoded.astype('uint8')
        #model = tf.keras.models.load_model('h5_fabien_vgg16_solution1_800-1000.h5')



        #predict
        predictor = Predict(model)
        prediction = array_to_img(predictor.predict_grad_cam(test_pic_array))
        predicted_class = predictor.predict_class(test_pic_array)


        dico = {
            'Tomato':'tomate',
            'Potato':'patate',
            'Strawberry':'fraise',
            'Squash': 'courgette',
            'Soybean': 'soja',
            'Raspberry': 'framboise',
            'Pepper,': 'poivron',
            'Peach': 'pêche',
            'Orange': 'orange',
            'Grape': 'raisin',
            'Corn': 'maïs',
            'Cherry': 'cerise',
            'Blueberry': 'myrtille',
            'Apple': 'pomme' }

        fr = dico[predicted_class.split('_')[0]]
        maladie = ' '.join(predicted_class.split('_')[3:])

        if str('healthy') in str(predicted_class).split('_'):
            components.html(f"""
            <div class='popup'>

            <div style='font-family: "Playfair Display", serif;color: #3F545B;text-align:center;font-size:1.5rem;'>La plante est <span style='color:green;'>saine.</span><br/>
            Il s'agit d'une feuille de {fr}.
            </div>
            </div>
                """)

            st.markdown(
                "<div style='font-family: Playfair Display, serif;color: #3F545B;text-align:center;;'>Image originale</div>",
                unsafe_allow_html=True)
            st.image(test_pic, use_column_width=True)

        else:
            components.html(f"""
            <div class='popup'>
            <div style='font-family: "Playfair Display", serif;color: #3F545B;text-align:center;font-size:1.5rem;'>La plante est <span style='color:red;'>infectée.</span>
            Il s'agit d'une feuille de {fr}, infectée par le <span style='color:red;'>{maladie}.</span>
            </div></div>
            """,
                            height=100)
            col1, col2 = st.columns(2)

            col1.markdown("<div style='font-family: Playfair Display, serif;color: #3F545B;text-align:center;font-size:1.5;'>Zones infectées</div>", unsafe_allow_html=True)
            col1.image(prediction, use_column_width=True)

            col2.markdown(
                "<div style='font-family: Playfair Display, serif;color: #3F545B;text-align:center;font-size:1.5;'>Image originale</div>",
                unsafe_allow_html=True)
            col2.image(test_pic, use_column_width=True)





        st.write(str(predicted_class))





#HTML CSS



if menu_id == 'A propos':


    components.html("""
        <div class='wrap'>
        <div class='spacer'></div>





        <p class='texte'>  GaiaCare est le fruit d’une coopération de quatre Data Scientists -
        Yassin Gofti, Fabien Prado, Walid Marouf et Cyril Warde - qui avaient à coeur de créer une application à la fois
        innovente et utile socialement.
        </p>


        <div class='spacer'></div>


        </div>
        </div>

        <style>
        .spacer {
            height: 1.5rem;
            display: block;
            width:100%;
        }

    .col1 span {
            font-size: 2rem; }

        .texte {
            font-family: 'Playfair Display', serif;}

        .col1 {
            width: 30%;
            flex-grow: 1;
            display: inline-block !important;}

        .item + .item {
            margin-left: 4%;}

        .colcontain {
        display: flex;
        padding-left: 15%;
        padding-right: 15%;
        }


        .wrap {
        #background-color:  #004029!important;
        #background-color: #e7fee0 !important;
        background-color: rgba(143, 193, 180, 0.4);

        border-radius: 0.3rem;
        color: #3F545B;
        text-align: center;

        padding-left: 5%;
        padding-right: 5%;
        width:70%;
        margin: auto;
            }



        </style>



            """,
                        height=450)
