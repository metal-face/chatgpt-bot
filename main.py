import asyncio
import uvicorn
import discord

from discord.ext import commands
from fastapi import FastAPI
from adapters.openai import client
from settings import DISCORD_BOT_TOKEN

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")


@bot.command(name="ask")
async def ask(ctx, *, question: str):
    await ctx.send("Let me think...")

    try:
        response = client.chat.completions.create(
            model="chatgpt-4o-latest", messages=[{"role": "developer", "content": question}]
        )

        answer = response.choices[0].message.content
    except Exception as error:
        answer = f"Sorry, something went wrong: {error}"

    await ctx.send(answer)


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "The ChatGPT Discord Bot Is Operational!"}


async def run_discord_bot():
    await bot.start(DISCORD_BOT_TOKEN)


async def run_fastapi():
    config = uvicorn.Config(app, host="0.0.0.0", port=80, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


async def main():
    await asyncio.gather(run_fastapi(), run_discord_bot())


if __name__ == "__main__":
    asyncio.run(main())
