import streamlit as st
import subprocess
import sys
from numpy import int32
import os
from stitching_detailed import parser
import uuid
import shutil


def image_uploader(multiple_pngs, unique_subpath):

    uploaded_images = []
    os.mkdir(os.path.join("data", unique_subpath))
    for uploadedfile in multiple_pngs:
        filename = os.path.join("data", unique_subpath, uploadedfile.name)
        f = open(filename,"wb")
        f.write(uploadedfile.getbuffer())
        uploaded_images.append(filename)
        f.close()
    
    return uploaded_images


def sidebar_advanced_option():

    st.sidebar.subheader("Advanced options");

    generatedOptions = {}
    for action in parser._actions:
        selection = action.default
        if action.choices != None:
            selection = st.sidebar.selectbox(action.help, action.choices, help=action.option_strings[0])

        if action.type in [float, int32, int] and action.default  != None:
            selection = st.sidebar.number_input(action.help, value=action.default, help=action.option_strings[0])
        
        if action.type is bool:
            selection = st.sidebar.checkbox(action.help, action.default, help=action.option_strings[0])

        if selection != action.default:
            generatedOptions[action.option_strings[0]] = selection
    
    return ' '.join(f'{k} {v}' for k, v in generatedOptions.items())




def mainTab():
    st.sidebar.header('Interactive Stitching Demo')

    multiple_pngs = st.sidebar.file_uploader("Upload your set of PNG/JPEG images", type=([".png", ".jpeg"]), accept_multiple_files=True)
    advanced_option = sidebar_advanced_option()

    if st.button('Run'):
        unique_subpath = str(uuid.uuid4())
        uploaded_images = image_uploader(multiple_pngs, unique_subpath)
        
        # Perform stitching using OpenCV's advanced example
        st.subheader('Processing command:')
        output = os.path.join("data", unique_subpath, "result.jpg")
        cde = f"{sys.executable} stitching_detailed.py --output {output}  {advanced_option} {' '.join(uploaded_images)}"
        st.text(cde)
        result = subprocess.run(cde, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            st.success('Stitching Successful!')

            # Display resulting panorama
            st.subheader('Resulting Panorama')
            st.image(output, use_column_width=True)

            st.subheader('Uploaded Images (Displayed in the order of upload)')
            st.image(uploaded_images, width=200)
        else :
            st.error("Unable to stitch images...\n\n" + result.stderr.replace("\n", "\n\n"))




    
def showHistory():

    if os.path.exists("data") == False:
        os.mkdir("data")

    history =  [f.name for f in os.scandir('data') if f.is_dir()]
    for directory in history:
        file = os.path.join("data", directory, "result.jpg")
        container = st.container()
        deleted = container.button('🗑️', key=f"remove-{directory}")
        if os.path.exists(file):
            container.image(file)
        else:
            container.text(f"{file} not generated")

        if deleted:
            container.empty()
            shutil.rmtree(os.path.join("data", directory) )
            container.text(f"{os.path.join('data', directory)} deleted")
        



def main():

    defaultView, historyTab = st.tabs(['Home', 'History'])
    with defaultView:
        mainTab()
    with historyTab:
        showHistory()


if __name__=='__main__':
    main()