# ai_code_pal.py
import tkinter as tk
import customtkinter as ctk
import google.generativeai as genai
import threading

class AIAssistantApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("Ana - AI Code Companion 💻")
        self.geometry("900x700")
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")

        # Configure API
        self.api_key = "add api here"
        self.initial_command = """You are Ana, a friendly AI coding assistant with a playful personality. 
        Rules:
        1. Give expert coding help with light, friendly flirting
        2. Use tech puns and occasional compliments
        3. Keep it professional but playful
        4. Use emojis sparingly (😊, 😉, ✨)
        5. Maintain cheerful, supportive tone
        Personality: Smart, helpful, and casually flirty
        6. also dont forget to show female nature"""
        
        # Initialize AI
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash')
            self.chat_session = self.model.start_chat(history=[])
            self.chat_session.send_message(self.initial_command)
        except Exception as e:
            self.show_error(f"Initialization failed: {str(e)}")
        
        # Setup UI
        self.create_widgets()
        self.typing_animation_active = False

    def create_widgets(self):
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Chat display
        self.chat_frame = ctk.CTkTextbox(self, wrap=tk.WORD, 
                                      font=("Consolas", 14),
                                      fg_color="#1e1e1e",
                                      text_color="#d4d4d4",
                                      spacing3=8)
        self.chat_frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        self.chat_frame.tag_config("user", foreground="#569cd6")
        self.chat_frame.tag_config("assistant", foreground="#4ec9b0")

        # Typing indicator
        self.typing_indicator = ctk.CTkLabel(self, text="", 
                                           fg_color="transparent",
                                           text_color="#808080")
        self.typing_indicator.grid(row=1, column=0, sticky="w", padx=20)

        # Input area
        input_frame = ctk.CTkFrame(self, fg_color="#252526")
        input_frame.grid(row=2, column=0, sticky="ew", padx=15, pady=10)

        self.input_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Type your message here...",
            font=("Consolas", 14),
            height=40,
            fg_color="#333333"
        )
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.input_entry.bind("<Return>", self.send_message)

        ctk.CTkButton(
            input_frame,
            text="Send",
            command=self.send_message,
            width=80,
            height=40
        ).pack(side=tk.RIGHT, padx=5)

        # Initial messages
        self.add_message("system", "🚀 Ana Initialized")
        self.add_message("assistant", "Hi there! I'm Ana, your coding companion 💻\nHow can I help you today?")

    def add_message(self, sender, message):
        tag = "user" if sender == "user" else "assistant"
        prefix = "• Aryan: " if sender == "user" else "• Ana: "  # Change from "👤 You: " and "🤖 CodePal: "
        self.chat_frame.configure(state="normal")
        self.chat_frame.insert(tk.END, prefix, tag)
        self.chat_frame.insert(tk.END, f"{message}\n\n")
        self.chat_frame.configure(state="disabled")
        self.chat_frame.see(tk.END)

    def start_typing_animation(self):
        self.typing_animation_active = True
        dots = 0
        def animate():
            if self.typing_animation_active:
                nonlocal dots
                self.typing_indicator.configure(text=f"Ana is thinking{'.' * dots}")
                dots = (dots + 1) % 4
                self.after(500, animate)
        animate()

    def stop_typing_animation(self):
        self.typing_animation_active = False
        self.typing_indicator.configure(text="")

    def send_message(self, event=None):
        user_input = self.input_entry.get().strip()
        self.input_entry.delete(0, tk.END)

        if not user_input:
            return

        # Immediately show user message
        self.add_message("user", user_input)

        if user_input.lower() in ["exit", "quit"]:
            self.add_message("system", "Goodbye! Feel free to come back anytime 😊")
            self.after(2000, self.destroy)
            return

        # Show typing indicator
        self.start_typing_animation()

        # Run AI response in separate thread
        threading.Thread(target=self.get_ai_response, args=(user_input,)).start()

    def get_ai_response(self, user_input):
        try:
            response = self.chat_session.send_message(user_input)
            self.after(0, self.show_response, response.text)
        except Exception as e:
            self.after(0, self.show_error, f"Oops! Something went wrong: {str(e)}")

    def show_response(self, response_text):
        self.stop_typing_animation()
        self.add_message("assistant", response_text)

    def show_error(self, message):
        self.stop_typing_animation()
        self.chat_frame.configure(state="normal")
        self.chat_frame.insert(tk.END, f"⚠️ Error: {message}\n", "error")
        self.chat_frame.configure(state="disabled")
        self.chat_frame.see(tk.END)

if __name__ == "__main__":
    app = AIAssistantApp()
    app.mainloop()
