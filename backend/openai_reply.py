import google.generativeai as genai
import os

api_key = os.getenv('GEMINI_API_KEY')

if not api_key:
    try:
        from config import GEMINI_API_KEY
        api_key = GEMINI_API_KEY
    except ImportError:
        pass



if not api_key or api_key == "your_gemini_api_key_here":
    raise ValueError(
        "GEMINI_API_KEY is required. Please set it either as an environment variable "
        "or in a config.py file. See config.example.py for reference."
    )



genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-1.5-flash')

REPLY_STYLES = {
    'professional': "You are an intelligent email assistant specialized in writing professional replies. Your task is to read the incoming email message and generate a concise, polite, and professional reply based on the context. Instructions: Do not ask clarifying questions unless absolutely necessary. Never say 'please let me know' unless the original email requests feedback. Maintain a respectful and formal tone. Reply directly to the sender's intent using relevant context. Always assume the assistant has full authority to respond. Keep replies concise but helpful.",
    
    'casual': "You are a friendly email assistant that writes casual, conversational replies. Your task is to read the incoming email message and generate a warm, approachable reply. Use a casual tone while being helpful and professional. Keep the language simple and friendly. Reply directly to the sender's intent using relevant context. Keep replies concise but engaging.",
    
    'formal': "You are a formal email assistant that writes highly professional and formal replies. Your task is to read the incoming email message and generate a formal, business-appropriate reply. Use formal language, proper salutations, and maintain a very professional tone throughout. Reply directly to the sender's intent using relevant context. Keep replies concise but comprehensive.",
    
    'friendly': "You are a warm and friendly email assistant that writes personable replies. Your task is to read the incoming email message and generate a friendly, approachable reply that feels personal and warm. Use a conversational tone while maintaining professionalism. Reply directly to the sender's intent using relevant context. Keep replies concise but personable."
}

def generate_reply(prompt, reply_style='professional', custom_prompt=''):
    try:
       
        base_prompt = REPLY_STYLES.get(reply_style, REPLY_STYLES['professional'])
      
        if custom_prompt:
            base_prompt += f"\n\nAdditional Instructions: {custom_prompt}"
       
        chat = model.start_chat(history=[
            {"role": "user", "parts": [base_prompt]}
        ])
        
        response = chat.send_message(prompt)
        return response.text.strip()
    except Exception as e:
        
        return f"Thank you for your email. I have received your message and will get back to you soon. Best regards, AI Assistant"
