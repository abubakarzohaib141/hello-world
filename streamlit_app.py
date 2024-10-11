import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI

# Set up the Gemini API
gemini_api_key = 'AIzaSyBaSe5UbPtTApn6m4JT7lT5JgyRtVd2pXk'  # Replace with your Gemini API key
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=gemini_api_key)

# Create a prompt template for generating task instructions
prompt = PromptTemplate.from_template("""
You are a helpful assistant. Based on the user's query, generate a simple response with the model name and a direct link to search for it on Facebook Marketplace. Include the budget in the link if specified.
User Query: {user_input}
Generate the response:
""")

# Set up the LangChain chain with the Gemini API
chain = LLMChain(llm=llm, prompt=prompt)

# Streamlit app UI
st.title("Car Search Link Generator with Budget")
st.write("Get a direct link to search for cars on Facebook Marketplace based on model and optional budget.")

# User input for car brand, model, and budget
car_brand_model = st.text_input("Enter car brand and model (e.g., 'Rangerover 2024'):")
budget = st.text_input("Enter your budget (optional, e.g., '50000' for £50,000):")

# Generate response and link when the button is clicked
if st.button("Generate Link"):
    if car_brand_model:
        # Generate instructions using Gemini API with the car model and budget
        user_input = f"Generate a link for {car_brand_model} under £{budget} on Facebook Marketplace" if budget else f"Generate a link for {car_brand_model} on Facebook Marketplace"
        
        # Get the response from Gemini API (you can modify this as needed)
        response = chain.run(user_input=user_input)
        
        # Construct the Facebook Marketplace search link, ensuring it's limited to vehicles
        fb_marketplace_url = f"https://www.facebook.com/marketplace/category/vehicles?query={car_brand_model.replace(' ', '%20')}&location=United%20Kingdom"
        
        # Add budget filter to the URL if provided
        if budget:
            fb_marketplace_url += f"&minPrice=0&maxPrice={budget}"
        
        # Display the model name and the direct link
        st.write(f"**Model Name:** {car_brand_model}")
        st.write(f"**Direct Link:** [Search for {car_brand_model} cars in the UK on Facebook Marketplace]({fb_marketplace_url})")
        
        if budget:
            st.write(f"**Budget:** Under £{budget}")
    else:
        st.write("Please enter a car brand and model.")
