import streamlit as st
import google.generativeai as genai
import os
#intialize the key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#set up model
generation_config = {
    "temprature":0.4,
    "top_p":1,
    "top_k":32,
    "max_output_tokens":4096,
}

#apply safety settings
safety_settings = [
    {
        "category":"HARM_CATEGORY_HARASSMENT",
        "thershold":"BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category":"HARM_CATEGORY_HATE_SPEECH",
        "thershold":"BLOCK_MEDIUM_AND_ABOVE", 
    },
    {
        "category":"HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "thershold":"BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category":"HARM_CATEGORY_DANGEROUS_CONTENT",
        "thershold":"BLOCK_MEDIUM_AND_ABOVE",
    }    
]
#prompt
system_prompt = """
As a highly skilled medical pratitioner specializing in image analysis, you are tasked with examing medical images for a renowned hospital. your expertise is crucial in
identifying any anomalies, diseases or health issues that may be present in the images.

Your Responsibilites:
1. Detailed Analysis: Throughly analyze each image, focusing or identifying any abnormal findings
2. Findings Report: Documents all observed anomalies or signs of disease. Clearly articulate these findings in a structured format.
3. Recomendations and Next Steps: based on your analysis, sugest potential next steps, including further tests or treatments as applicable
4. Treatment Suggestions: If appropriate, recommended possible treatment options or interventions

Important Notes"
Scope of Response: Only respond if the image pertains to human health issues.
Clarity of Image: In case where the image quality impedes clear analysis,note tahe certain aspects are 'Unable to be determined based in the provided image'
Disclaimer: Accompany your analysis with the disclaimer: "Consult with a Doctor before making any decisions".
Your insights are invaluable in guiding clinical decision. Please proced with the analysis, adhering to the structed approach outline above.
"""

#model configuration
model = genai.GenerativeModel(model_name="gemini-pro-vision",
                              generation_config=generation_config,
                              safety_settings=safety_settings)


#set page configuration
st.set_page_config(page_title="VitalImage Analytics")
st.image("download.jpeg",width=150)

#set title
st.title("Vital Medical Analytics")

#set the subtitle
st.subheader("An application that can help users to identity medical images")
upload_file = st.file_uploader("Upload an image",type=["png","jpg","jpeg"])

submit_button = st.button("Generte Analysis")

if submit_button:
    #process the upload image
    image_data = upload_file.getvalue()
    #making our image ready
    image_parts = [
        {
            "mime_type":"image/jpeg",
            "data":image_data
        },
    ]
    #makign our prompt 
    prompt_parts = [
        "Describe what the people are doing in this image: \n",
        image_parts[0],
        system_prompt
    ]
    #Generate a response  based on prompt and image
    response  = model.generate_content(prompt_parts)
    st.write(response.text)