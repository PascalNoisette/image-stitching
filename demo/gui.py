import streamlit as st
import subprocess
import sys
from numpy import int32
import os
import uuid
import shutil
from stitching.cli import stitch


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


def sidebar_advanced_option(advanced):


    if not advanced:
        return ' '

    parser = stitch.create_parser()

    generatedOptions = {}
    knownOptions = []
    for action in parser._actions:
        if action.dest in knownOptions:
            continue
        knownOptions.append(action.dest)
        selection = action.default

        if action.choices != None:
            selection = st.sidebar.selectbox(action.help, action.choices, help=action.option_strings[0])

        elif action.type in [float, int32, int] and action.default  != None:
            selection = st.sidebar.number_input(action.help, value=action.default, help=action.option_strings[0])
        
        elif action.type is bool or action.default is False or action.default is True:
            selection = st.sidebar.checkbox(action.help, action.default, help=action.option_strings[0])

        if selection != action.default:
            generatedOptions[action.option_strings[0]] = selection
            if action.default is False or action.default is True:
                generatedOptions[action.option_strings[0]] = " "
    
    return ' '.join(f'{k} {v}' for k, v in generatedOptions.items())




def mainTab():
    st.sidebar.header('Interactive Stitching Demo')

    multiple_pngs = st.sidebar.file_uploader("Upload your set of PNG/JPEG images", type=([".png", ".jpeg"]), accept_multiple_files=True)
    advanced = st.sidebar.checkbox("See all advanced options")
    advanced_option = sidebar_advanced_option(advanced)

    if st.button('Run'):
        unique_subpath = str(uuid.uuid4())
        uploaded_images = image_uploader(multiple_pngs, unique_subpath)
        
        # Perform stitching using OpenCV's advanced example
        st.subheader('Processing command:')
        output_dir = os.path.join("data", unique_subpath)
        output = os.path.join(output_dir, "result.jpg")
        cde = f"stitch  --verbose_dir {output_dir}/verbose --output {output}  {advanced_option} {' '.join(uploaded_images)}"
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
        columns = container.columns([1, 1, 1, 1, 1, 1])
        deleted = columns[0].button('🗑️', key=f"remove-{directory}")
        if not os.path.exists(file):
            file = os.path.join("data", directory, "verbose", "09_result.jpg")
        if os.path.exists(file):
            container.image(file)
            columns[1].download_button(data=open(file, "rb"), file_name=file, label="Download")
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