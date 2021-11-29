import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import pathlib as Path

#upload image
import numpy as np
import base64
import requests
import json




st.set_option('public_filetypes', 'jpg, csv, png, jpeg')


components.html(
    """

<div class='wrap' style='background:#fff;'>
<div class='logo'></div>
<h1 class='title'>GaïaCare</h1>

<p class='texte'> Uploadez une photo de vos plantes </p>

<div class='colcontain'>
<col1 class='col1'>
<p class='texte'> 35</span> </p>
<p class='texte'> Uploadez une photo de vos plantes </p>

</col1>

<col1 class='col1'>
<p class='texte'> <span>35</span> </p>
<p class='texte'> Uploadez une photo de vos plantes </p>
</col1>


<col1 class='col1'>
<p class='texte'> <span>35</span> </p>
<p class='texte'> Uploadez une photo de vos plantes </p>
</col1>
</div>
</div>


<style>
.logo {
    background-image:url('logo.png');
    width:100%;

}
.texte {
    font-family: "Source Sans Pro", sans-serif;

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
    font-family: "Source Sans Pro", sans-serif;
    font-size:4rem;
    font-weight: 700;
    color: #3F545B;
    padding: 1.25rem 0px 1rem;
    margin: 0px;
    line-height: 1.4;
    text-align:center;
    }

</style>



    """,
    height=300,
)



CSS = """


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
    requests.post('https://dummy-gaia-api-ndgviyvkja-ew.a.run.app/predict/',
                json.dumps(image_dict),
                headers=headers)
    #fastAPI.py POST code to add on VS Code





    st.markdown(
        'Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...'
    )
'''


'''
