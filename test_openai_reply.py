import google.generativeai as genai

def generate_reply(prompt):
    return f"Thank you for your email. I have received your message and will get back to you soon. Best regards, AI Assistant"

# Original version (commented out due to rate limits)
# genai.configure(api_key="AIzaSyDKRqbPjjrCtexIbDKUg5GV73SgarME64k")
# model = genai.GenerativeModel('gemini-1.5-flash')
# chat = model.start_chat(history=[...])
# def generate_reply(prompt):
#     response = chat.send_message(prompt)
#     return response.text.strip() 