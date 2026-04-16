import streamlit as st
import os
from api import note_generator, audio_generator,quiz_generator
from PIL import Image

st.title("Note Summary and Quiz Generator",anchor = False)
st.markdown("Upload upto 5 images to generate note summary and quiz questions")

st.divider()


with st.sidebar:
    st.header("Upload Control")
    images = st.file_uploader(
        "Upload upto 5 notes",
        type = ["jpeg", "jpg", "png"],
        accept_multiple_files = True
    )

    
    if images:
        if len(images) > 5:
            st.error("You can only upload upto 5 images")
        else:
            cols = st.columns(len(images))
            for i, image in enumerate(images):
                cols[i].image(image)

    
    difficulty = st.selectbox(
        "Select difficulty for the Quiz",
        ("Easy", "Medium", "Hard"),
        index = None
    )

    language = st.selectbox(
        "Select preferred language",
        ("English", "Bangla"),
        index = None
    )

    button = st.button("Upload to generate", type = "primary")
if button:
    if not images:
        st.error("No images uploaded yet")
    elif not difficulty:
        st.error("Select your difficulty level")
    else:
        #note 
        with st.container(border = True):
            st.subheader("Note Summary", anchor = False)
            
            #converting to pil images

            pil_images = [Image.open(image) for image in images]

            with st.spinner("Genearting note summary...", show_time = True):
                generated_note = note_generator(pil_images,language)
                st.markdown(generated_note)


        #audio transcript
        with st.container(border = True):
            st.subheader("Audio Transcription", anchor = False)
            
            with st.spinner("Genearting audio transcription...", show_time = True):

                generate_note_no_markdown = generated_note.replace("*","").replace("#","").replace("-"," ").replace("`"," ")

                audio = audio_generator(generate_note_no_markdown,language)
                st.audio(audio)
            


        #quiz
        with st.container(border = True):
            st.subheader(f"Quiz: Difficulty Level - {difficulty}", anchor = False)
            
            with st.spinner("Genearting quiz...", show_time = True):
                generated_quiz = quiz_generator(pil_images, difficulty,language)
                st.markdown(generated_quiz)
        