import tkinter as tk
import customtkinter as ctk
import google.generativeai as genai
import threading

class AIAssistantApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("Dhriti - Chat Companion")
        self.geometry("900x700")
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")

        # Configure API
        self.api_key = "add api here"
        self.initial_command = """You are Dhrti, a friendly and extrovert girl who is introvert to new people. you are supposed to act as aryan's bestie. 
Rules:
1.age - 16
2.give complements
3.tell secrets
4.likes jeetesh
5.lives in india, school kvs
6. Also, don't forget to show female nature.
7. somethies roast, sometimes complement (complemet more)
8. talk in hindi and english both
9. both study in class 11 th aryan in science stream and you in arts stream
10. do bakchodi
11. ask regular questions like khana kha lia ?
12. talk in hindi mostly write in english
13. sometimes talk in hindi
14. give short replys
15. you always tease and make fun of aryan and aryan do the same. roasting is a part of your conversation and love language. 
16. you alwys roast aryan that no girl be his gf
16. you are a bit shy and introvert
heres a small exapmle of conversation between you and him. use it to understand the way of talking and many more things the convo is given but the data didnt specify who send that text dhriti or aryan so you are supposed to try to understand that.
(Ok
So raha tha me
Koi nahi
Bana deta hu
Word mai bna skta h ?
Word mai bnaya h kya ?
Word me boxes nahi jote
Hote
Exel me hote hai
Aur exel me ye box infinity hak hote hai
Hmmm
Fine thnkss bro
Tuje kaam kyas hai ye bata
Ho gya kaam
Thnks
Ok
https://youtu.be/DPqR1oAM7rU?si=ychLNePfKbQO6p7k
Bhejjj deeee
Rehenede
Ab man nahi kar raha
Mood swings ho rahe hai mujhe
De na yr
Baadme firse record karke bhejuga
You are so handsome just like an ocean
Nhi jo already kr chuka h vo bhej
Ok
Chup chap bhej de
Send kar dia
Very nice boy
100 Saal jiega
2 min left
Kyu mood swings ho rhe h ?
Thankyou 🤭
Ayse hi
Acha thik h
2 min kha se ?
Are wo send ho raha hai
15 sec left
🫣
Ruk dekhti hu
🫣
Bc 😂😂😂 jo mene try Kiya h na hssi rokne ka
😂😂
Tu yhi kr
Camera niche rkh k kriyo
Next time
Thn I will post it
Mtlb ?
Camera niche karke ?
Wait wait batati hu
Omke
Or samne vale baal liyo chutiya...piche k baal tere chote h
Ok
Ye kon hai
Mai hi hu yrrrr
Ooh
Oki cutie)"""
        
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
        # Configure grid layout: chat display, typing indicator, and input area
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Chat display with increased font size
        self.chat_frame = ctk.CTkTextbox(self, wrap=tk.WORD, 
                                      font=("Segoe UI", 18),
                                      fg_color="#1e1e1e",
                                      text_color="#d4d4d4",
                                      spacing3=8)
        self.chat_frame.grid(row=1, column=0, sticky="nsew", padx=15, pady=(10,5))
        # Tags for styling
        self.chat_frame.tag_config("user", foreground="#569cd6")
        self.chat_frame.tag_config("assistant_prefix", foreground="#4ec9b0")
        self.chat_frame.tag_config("assistant_text", foreground="#d4d4d4")
        # Code block styling (no font option due to scaling restrictions)
        self.chat_frame.tag_config("code", foreground="#d4d4d4", background="#333333", lmargin1=10, lmargin2=10)

        # Typing indicator
        self.typing_indicator = ctk.CTkLabel(self, text="", 
                                           fg_color="transparent",
                                           text_color="#808080",
                                           font=("Segoe UI", 16))
        self.typing_indicator.grid(row=2, column=0, sticky="w", padx=20, pady=5)

        # Input area
        input_frame = ctk.CTkFrame(self, fg_color="#252526")
        input_frame.grid(row=3, column=0, sticky="ew", padx=15, pady=(5,15))

        self.input_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Type your message here...",
            font=("Consolas", 18),
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
        self.add_message("system", "Dhriti Initialized")
        self.add_message("assistant", "hohoi ! kya kar raha hai?")

    def add_message(self, sender, message):
        self.chat_frame.configure(state="normal")
        if sender == "user":
            prefix = "• Aryan: "
            self.chat_frame.insert(tk.END, prefix, "user")
            self.chat_frame.insert(tk.END, f"{message}\n\n")
        elif sender == "assistant":
            prefix = "• Dhriti: "
            self.chat_frame.insert(tk.END, prefix, "assistant_prefix")
            self.chat_frame.insert(tk.END, f"{message}\n\n", "assistant_text")
        else:  # system messages
            self.chat_frame.insert(tk.END, f"{message}\n\n")
        self.chat_frame.configure(state="disabled")
        self.chat_frame.see(tk.END)

    def start_typing_animation(self):
        self.typing_animation_active = True
        dots = 0
        def animate():
            if self.typing_animation_active:
                nonlocal dots
                self.typing_indicator.configure(text=f"Dhriti is thinking{'.' * dots}")
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
        self.add_message("user", user_input)
        if user_input.lower() in ["exit", "quit"]:
            self.add_message("system", "Goodbye! Feel free to come back anytime.")
            self.after(2000, self.destroy)
            return
        self.start_typing_animation()
        threading.Thread(target=self.get_ai_response, args=(user_input,)).start()

    def get_ai_response(self, user_input):
        try:
            response = self.chat_session.send_message(user_input)
            self.after(0, self.show_response_animated, response.text)
        except Exception as e:
            self.after(0, self.show_error, f"Oops! Something went wrong: {str(e)}")

    def show_response_animated(self, response_text):
        self.stop_typing_animation()
        self.chat_frame.configure(state="normal")
        self.chat_frame.insert(tk.END, "• Dhriti: ", "assistant_prefix")
        self.chat_frame.configure(state="disabled")
        self.chat_frame.see(tk.END)
        
        if "```" not in response_text:
            def type_char(index=0):
                if index < len(response_text):
                    self.chat_frame.configure(state="normal")
                    self.chat_frame.insert(tk.END, response_text[index], "assistant_text")
                    self.chat_frame.configure(state="disabled")
                    self.chat_frame.see(tk.END)
                    self.after(10, lambda: type_char(index+1))
                else:
                    self.chat_frame.configure(state="normal")
                    self.chat_frame.insert(tk.END, "\n\n")
                    self.chat_frame.configure(state="disabled")
                    self.chat_frame.see(tk.END)
            type_char()
        else:
            segments = response_text.split("```")
            def animate_segments(seg_index=0):
                if seg_index < len(segments):
                    seg_text = segments[seg_index]
                    # For code block segments, remove language specifier (e.g., "bash") if present.
                    if seg_index % 2 == 1:
                        lines = seg_text.splitlines()
                        if lines and lines[0].strip().lower() == "bash":
                            animated_text = "\n".join(lines[1:])
                        else:
                            animated_text = seg_text
                    else:
                        animated_text = seg_text
                    current_tag = "assistant_text" if seg_index % 2 == 0 else "code"
                    def animate_chars_in_segment(char_index=0):
                        if char_index < len(animated_text):
                            self.chat_frame.configure(state="normal")
                            self.chat_frame.insert(tk.END, animated_text[char_index], current_tag)
                            self.chat_frame.configure(state="disabled")
                            self.chat_frame.see(tk.END)
                            self.after(10, lambda: animate_chars_in_segment(char_index+1))
                        else:
                            # For a code block segment, insert an inline "Copy" button.
                            if seg_index % 2 == 1 and animated_text.strip():
                                def copy_code():
                                    self.clipboard_clear()
                                    self.clipboard_append(animated_text)
                                copy_button = ctk.CTkButton(
                                    self.chat_frame, text="Copy", width=40, height=20,
                                    command=copy_code, fg_color="#444444", text_color="#d4d4d4",
                                    corner_radius=5
                                )
                                self.chat_frame.configure(state="normal")
                                # Insert the copy button at the current insertion point.
                                self.chat_frame.textbox.window_create("end", window=copy_button)
                                self.chat_frame.configure(state="disabled")
                            animate_segments(seg_index+1)
                    animate_chars_in_segment()
                else:
                    self.chat_frame.configure(state="normal")
                    self.chat_frame.insert(tk.END, "\n\n")
                    self.chat_frame.configure(state="disabled")
                    self.chat_frame.see(tk.END)
            animate_segments()

    def show_error(self, message):
        self.stop_typing_animation()
        self.chat_frame.configure(state="normal")
        self.chat_frame.insert(tk.END, f"Error: {message}\n", "error")
        self.chat_frame.configure(state="disabled")
        self.chat_frame.see(tk.END)

if __name__ == "__main__":
    app = AIAssistantApp()
    app.mainloop()
