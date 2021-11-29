import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import pathlib as Path

#upload image
import numpy as np
import base64
import requests
import json


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

<div class='wrap' style='background:#fff;'>


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
<p class='texte'> Lorem ipsum dolor sit amet.
Rem assumenda quasi qui laboriosam blanditiis aut nemo voluptatem aut autem
natus est ipsa sequi ab consequuntur modi ut earum animi. Id natus expedita
ea dolores magni est enim explicabo qui facilis totam.

 </p>
<div class='spacer'></div>

<p class='texte'> Uploadez une photo de vos plantes </p>

<div class='spacer'></div>

</div>


<style>
.spacer {
    height: 2rem;
    display: block;
    width:100%;
}
.col1 span {
    font-size: 3rem;

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
      margin-left: 2%;

}
.colcontain {
        display: flex;

}

.wrap {
    background-color: #fff !important;
    border-radius: 5px;
    color: #3F545B;
    text-align: center;

}

.title  {
    padding-top: 0 !important;
    font-family: "Source Sans Pro", sans-serif;
    font-size:2rem;
    font-weight: 700;
    color: #3F545B;
    padding: 1.25rem 0px 1rem;
    margin: 0px;
    line-height: 1.4;
    text-align:center;
    }

</style>



    """,
                height=300)



CSS = """


.logo {
      display:flex;
    width: 100%;
    justify-content:center
}
.logo img {

    width:4rem !important;
    margin:auto;


}

.wrap {
    background-color: #fff !important;
}


body {
    color: #CEE5D0 !important;


}


.stApp {
    background: #CEE5D0 !important;

}

"""

st.write(f'<style>{CSS}</style>', unsafe_allow_html=True)





st.set_option('deprecation.showfileUploaderEncoding', False)

uploaded_file = st.file_uploader("", type=['png','jpeg','jpg'])


if uploaded_file is not None:
    #open image and convert to RGB
    test_pic = Image.open(
        uploaded_file
    ).convert('RGB')
    #turn to array
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
    response = requests.post('https://dummy-gaia-api-ndgviyvkja-ew.a.run.app/predict',
                json.dumps(image_dict),
                headers=headers)

    st.write(

       str(response.json()) )


'''


'''
