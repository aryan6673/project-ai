import google.generativeai as genai

# Replace with your actual Gemini API key securely (use environment variables in production)
API_KEY = "AIzaSyCkFVihZnx6NfKyGq1O4PTx5A6yDnfg_To"

genai.configure(api_key=API_KEY)

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

chat_session = model.start_chat(history=[])

# Send the hacking simulator command first
init_command = "act like a cat ans say mew mew "
chat_session.send_message(init_command)  # AI will adopt this role

# Initial hacking-style message
print("SERVER BOOTING...\nACCESS GRANTED\nType your command:")

while True:  # Continuous chat loop
    try:
        user_input = input(">> ")  # Prompt in hacking style

        if user_input.lower() in ["exit", "quit"]:
            print("TERMINATING SESSION...\nGoodbye!")
            break

        response = chat_session.send_message(user_input)
        
        # Display response in a simulated code format
        print(f"[SYSTEM RESPONSE]\n```bash\n{response.text}\n```")

    except KeyboardInterrupt:
        print("\nTERMINATING SESSION...\nGoodbye!")
        break
