import PIL
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import pathlib as Path
import pandas as pd
import time


#upload image
import numpy as np
import base64
import requests
import json

CSS = """
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



        .overlay:target {

        }




        .block-container {
            background-color: #fff !important;
        }
        .css-qrbaxs {
            display: none;
        }

        .logo {
            display:flex;
            width: 100%;
            justify-content:center
        }
        .logo img {

            width:5rem !important;
            margin:auto;


        }




        body {
            color: #CEE5D0 !important;


        }


        .stApp {
        # background: #CEE5D0 !important;
        background-color:  #004029!important;


        }


"""

st.write(f'<style>{CSS}</style>', unsafe_allow_html=True)



file_ = open("logo.png", "rb")
contents = file_.read()
logo_url = base64.b64encode(contents).decode("utf-8")
file_.close()

st.markdown(
    f'<div class="clogo"><div class="logo"><img src="data:image/png;base64,{logo_url}"></div></div>',
    unsafe_allow_html=True,
)



components.html("""

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display&display=swap" rel="stylesheet">

<h1 class="title">GaïaCare</h1>
<div class='spacer'></div>

<div class='wrap'>



<div class='colcontain'>
<col1 class='col1'>
<p class='texte'> <span> 16 </span> </p>
<p class='texte'> maladies reconnus </p>

</col1>

<col1 class='col1'>
<p class='texte'><span> 98%  </span> </p>
<p class='texte'> de précisions </p>
</col1>


<col1 class='col1'>
<p class='texte'> <span>10</span> </p>
<p class='texte'> plantes </p>
</col1>
</div>

<div class='spacer'></div>


<p class='texte'> Lorem ipsum dolor sit amet.
Rem assumenda quasi qui laboriosam blanditiis aut nemo voluptatem aut autem
natus est ipsa sequi ab consequuntur modi ut earum animi. Id natus expedita
ea dolores magni est enim explicabo qui facilis totam.

 </p>

<p class='texte'> Uploadez une photo de vos plantes </p>

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
    font-size: 2rem;

}

.texte {
    font-family: 'Playfair Display', serif;
}

.col1 {
    width: 20%;
    flex-grow: 1;
    display: inline-block !important;

}

.item + .item {
      margin-left: 4%;

}
.colcontain {
        display: flex;

}


.wrap {
    #background-color:  #004029!important;
    background-color: #e7fee0 !important;
    max-width:90%;
    margin: auto;
    border-radius: 0.3rem;
    color: #004029;
    text-align: center;


}



.title  {
    padding-top: 0 !important;
    font-family: "Open Sans", sans-serif;
    font-size:3rem;
    font-weight: 500;
    color: #3F545B;
    padding: 1.25rem 0px 1rem;
    margin: 0px;
    line-height: 1.4;
    text-align:center;
    letter-spacing:0.2rem;

    }

</style>



    """,
                height=450)








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
    test_pic_array = test_pic_array.astype('uint8')
    #memorizing shape
    height, width, channel = test_pic_array.shape
    #reshape
    test_pic_array = test_pic_array.reshape(height * width * channel)
    # encoding to b64
    b64bytes = base64.b64encode(test_pic_array)
    #decoding to utf8 and turning to  string
    b64str = b64bytes.decode('utf8').replace("'", '"')
    image_dict = {
        'image': b64str,
        'height': height,
        'width': width,
        'channel': channel
    }
    headers = {'Content_Type': 'application/json'}
    newjson = json.dumps(image_dict)
    response = requests.post('https://dummy-gaia-api-ndgviyvkja-ew.a.run.app/predict_grad_cam',
        newjson,
        headers=headers).json()

    decoded = base64.b64decode(bytes(response['image'], 'utf-8'))
    decoded = np.frombuffer(decoded, dtype='float32')
    decoded = decoded.reshape(response['height'], response['width'], response['channel'])
    decoded = decoded.astype('uint8')


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

    fr = dico[response['class'].split('_')[0]]
    maladie = ' '.join(response['class'].split('_')[3:])

    if str('healthy') in str(response['class']).split('_') :
        components.html(f"""
        <div class='popup'>

        <div style='font-family: "Open Sans", sans-serif; color : #004029;
        font-size:2rem;'>La plante est <span style='color:green;'>saine.</span><br/>
        Il s'agit d'une feuille de {fr}.
        </div>
        </div>
               """)
    else:
        components.html(f"""
        <div class='popup'>
        <div style='font-family: "Open Sans", sans-serif; color : #004029;
        font-size:2rem;'>La plante est <span style='color:red;'>infectée.</span>
        Il s'agit d'une feuille de {fr}, infectée par le <span style='color:red;'>{maladie}.</span>
        </div></div>
        """,
                        height=100)
        col1, col2 = st.columns(2)

        col1.header("Zones inféctées")
        col1.image(decoded, use_column_width=True)

        col2.header("Image originale")
        col2.image(test_pic, use_column_width=True)





    st.write(str(response['class']))
