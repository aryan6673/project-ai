import google.generativeai as genai

# Replace "YOUR_API_KEY" with your actual Gemini API key.
# WARNING: Hardcoding your API key directly in the script is not recommended for security reasons.
#          Consider using environment variables for sensitive information.
API_KEY = "AIzaSyCkFVihZnx6NfKyGq1O4PTx5A6yDnfg_To"  # <---- REPLACE WITH YOUR ACTUAL API KEY

genai.configure(api_key=API_KEY)

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
)

# Create the chat session OUTSIDE the loop to preserve history.
chat_session = model.start_chat(history=[])


for i in range(100):  # Corrected for loop syntax
    a = input("--> ")

    response = chat_session.send_message(a)

    print(response.text)
