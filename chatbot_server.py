import logging
import os
import google.generativeai as genai

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Configure Server logger
logging.basicConfig(
format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
level = logging.INFO,

)

# Initialize Google Generative AI client
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
model = genai.GenerativeModel('gemini-pro')

#Command Handlers
#----------------------------------------------------------------

#Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello. Whats on your mind?")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Use the /ask command followed by your question to generate a response.")

#Ask (Prompt)
async def answer_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = update.message.text.split('/ask ')[1]
    try:

        response = model.generate_content(question)

        logging.info(f"Generated response: {response.text}")

        await update.message.reply_text(response.text)

    except Exception as e:
        logging.error(f"Error generating response: {e}")
        await update.message.reply_text("An error occurred while generating a response.")
    
                                    
#----------------------------------------------------------------
#Main Loop
def main():

    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    #Basic Handlers
    application.add_handler(CommandHandler('start', start)) 
    application.add_handler(CommandHandler('help', help_command))

    #Advanced Handlers
    application.add_handler(CommandHandler('ask', answer_command))

    



    application.run_polling()

if __name__ == '__main__':
    main()