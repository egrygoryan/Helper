import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    filters,
    ContextTypes,
    MessageHandler)
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from Agents.Agent import get_agent_executor


load_dotenv()
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_API_KEY"]=str(os.getenv('LANGSMITH_API_KEY'))
os.environ["LANGCHAIN_PROJECT"]="MY_DEMO"

BOT_TOKEN = os.getenv("BOT_TOKEN")
chat_history = []

# Commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello, I'm here to help you")

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # #add human message to list for tracking/history purpose
    agent_executor = get_agent_executor()
    #add human messages to history
    chat_history.append(HumanMessage(content=update.message.text))
    response = agent_executor.invoke({"input": {update.message.text},
                                      "chat_history": chat_history})
    #add ai responses to history
    chat_history.append(AIMessage(content=response["output"]))

    await update.message.reply_text(response["output"])

if __name__ == '__main__':
    #build and run bot
    app = Application.builder().token(BOT_TOKEN).build()
    #add handlers to bot
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))
    app.run_polling(poll_interval=3)
