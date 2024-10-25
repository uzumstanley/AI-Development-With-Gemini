import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv, find_dotenv

def ask_and_get_answer(prompt, img):
    # creating a GenerativeModel instance using the Gemini-Pro-Vision model
    model = genai.GenerativeModel('gemini-pro-vision')

    # generate a text response based on the prompt and image
    response = model.generate_content([prompt, img])

    return response.text

# This function converts a Streamlit image upload object (st_image) into a PIL (Python Imaging Lib) Image object.
def st_image_to_pil(st_image):
    import io
    from PIL import Image

    # getting the image data from the BytesIO object.
    image_data = st_image.read()

    # converting the image data to a PIL Image object.
    pil_image = Image.open(io.BytesIO(image_data))
    return pil_image


# defining application entry point
if __name__ == '__main__':
    # loading the environment variables from the .env file that contains the Google API key.
    load_dotenv(find_dotenv(), override=True)

    # configuring the generative AI model to use the GOOGLE_API_KEY for authentication.
    genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))

    # displaying the Gemini logo and subheader.
    st.image('gemini.png') 
    st.subheader('Talking With an Image ✨')

    # creating a file upload widget for the user to select an image.
    img = st.file_uploader('Select an Image: ', type=['jpg', 'jpeg', 'png', 'gif'])

    # if the user has selected an image, I am displaying it and allowing the user to ask questions about it.
    if img:
        st.image(img, caption='Talk with this image.')

        # displaying a text input for the prompt.
        prompt = st.text_area('Ask a question about this image: ')

        # if the user has entered a question, we go ahead and make the API call to Gemini.
        if prompt:
            # converting the st.file_uploader object to a PIL image object
            pil_image = st_image_to_pil(img)

            # creating a spinner
            with st.spinner('Running ...'):
                # calling ask_and_get_answer().
                answer = ask_and_get_answer(prompt, pil_image)

                # displaying the answer in a text area widget.
                st.text_area('Gemini Answer: ', value=answer)

            # adding a divider to separate the current answer from the previous ones.
            st.divider()

            # creating a key in the session state called 'history'.
            # the corresponding value will be all the previous questions and answers.
            if 'history' not in st.session_state:
                st.session_state.history = ''

            # concatenating the current question with its answer.
            value = f'Q: {prompt} \n\n A: {answer}'

            # adding this value before the existing history.
            st.session_state.history = f'{value} \n\n {"-" * 100} \n\n {st.session_state.history}'

            # saving the chat history from the session state into a variable.
            h = st.session_state.history

            # displaying a text area for the chat history.
            st.text_area(label='Chat History', value=h, height=400, key='history')

# Run the app: streamlit run ./gemini_talk_with_a_photo.py