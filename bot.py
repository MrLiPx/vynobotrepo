import discord
from discord.ext import commands, tasks
import os
import asyncio
from dotenv import load_dotenv
import logging
import json
import random
import sys

# Load environment variables securely from .env file
load_dotenv()

# --- Logging Configuration ---
# Ensure logs directory exists
log_dir = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(log_dir, exist_ok=True)

# Main bot logger
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
                    handlers=[
                        logging.StreamHandler(sys.stdout), # Log to console
                        logging.FileHandler(os.path.join(log_dir, "bot_main.log"), encoding='utf-8') # Log to file
                    ])
log = logging.getLogger('bot.main')
log.info("Bot main process started.")

# --- Bot Intents ---
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
intents.guilds = True
intents.reactions = True
intents.voice_states = True
intents.emojis_and_stickers = True
intents.integrations = True
intents.webhooks = True # For webhook management
intents.invites = True # For invite tracking
intents.moderation = True # For moderation events

# --- Bot Initialization ---
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None) # Custom help command assumed

async def load_all_cogs_recursive():
    """Recursively loads all cogs from the ModulesPremium directory."""
    modules_premium_path = os.path.join(os.path.dirname(__file__), "ModulesPremium")
    if not os.path.exists(modules_premium_path):
        log.critical(f"ModulesPremium directory not found at: {modules_premium_path}. Cogs cannot be loaded.")
        return

    loaded_count = 0
    failed_count = 0
    log.info("Starting recursive cog loading process...")
    for root, dirs, files in os.walk(modules_premium_path):
        # Filter out __pycache__ directories to prevent issues
        dirs[:] = [d for d in dirs if d != '__pycache__']
        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                relative_path = os.path.relpath(os.path.join(root, file), os.path.dirname(__file__))
                module_name = relative_path.replace(os.sep, ".")[:-3] # Convert to Python import path
                try:
                    await bot.load_extension(module_name)
                    log.info(f"Successfully loaded: {module_name}")
                    loaded_count += 1
                except commands.ExtensionAlreadyLoaded:
                    log.debug(f"Extension already loaded, skipping: {module_name}")
                except Exception as e:
                    log.error(f"Failed to load {module_name}. Error: {type(e).__name__}: {e}")
                    failed_count += 1
    log.info(f"Cog loading complete. Loaded: {loaded_count}, Failed: {failed_count}.")

# --- Bot Events ---
@bot.event
async def on_ready():
    """Event: Bot is ready and connected to Discord."""
    log.info(f'Logged in as {bot.user} (ID: {bot.user.id})')
    log.info('------')
    log.info(f'Discord.py version: {discord.__version__}')
    log.info(f'Python version: {sys.version.split(" ")[0]}')
    log.info('------')
    await load_all_cogs_recursive()
    log.info('------')
    log.info('All cog loading attempts finalized.')
    log.info('Bot is now fully operational and serving commands across guilds.')
    # Set a default bot presence
    await bot.change_presence(activity=discord.Game(name="Managing your server"))

@bot.event
async def on_command_error(ctx, error):
    """Global error handler for commands."""
    if isinstance(error, commands.CommandNotFound):
        # await ctx.send("Sorry, that command doesn't exist. Use `!help` for a list of commands.")
        log.debug(f"Command not found: '{ctx.message.content}' by {ctx.author} (ID: {ctx.author.id}) in guild '{ctx.guild.name}' (ID: {ctx.guild.id})")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Missing arguments. Please check the command usage. Correct usage: `!{ctx.command.name} {ctx.command.signature}`")
        log.warning(f"Missing arguments for command {ctx.command.name} by {ctx.author}: {error}")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have the necessary permissions to use this command.")
        log.warning(f"User {ctx.author} missing permissions for command {ctx.command.name}.")
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send(f"I am missing permissions to execute this command. Please grant me: {', '.join(error.missing_permissions)}")
        log.error(f"Bot missing permissions for command {ctx.command.name}: {error.missing_permissions}")
    elif isinstance(error, commands.NoPrivateMessage):
        await ctx.send("This command cannot be used in private messages.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f"Invalid argument provided. Error: {error}")
        log.warning(f"Bad argument for command {ctx.command.name}: {error}")
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"This command is on cooldown. Please try again in {error.retry_after:.2f}s.")
        log.info(f"Command {ctx.command.name} on cooldown for {ctx.author}.")
    elif isinstance(error, commands.NotOwner):
        await ctx.send("This command can only be used by the bot owner.")
        log.warning(f"Non-owner {ctx.author} attempted to use owner-only command {ctx.command.name}.")
    else:
        log.exception(f"Unhandled command error in command {ctx.command} by {ctx.author}: {error}")
        await ctx.send("An unexpected error occurred while running this command. The development team has been notified.")


# --- Bot Commands ---
@bot.command()
async def ping(ctx):
    """Responds with the bot's latency."""
    latency_ms = round(bot.latency * 1000)
    await ctx.send(f'Pong! My latency is {latency_ms}ms.')
    log.info(f"Ping command called by {ctx.author}. Latency: {latency_ms}ms.")

@bot.command(name="reload_all_modules")
@commands.is_owner() # Only bot owner can use this command
async def reload_all_modules_command(ctx):
    """Reloads all loaded cogs (modules) from the ModulesPremium directory."""
    log.info(f"Reloading all modules initiated by owner {ctx.author} (ID: {ctx.author.id}).")
    initial_loaded_cogs = list(bot.extensions.keys())
    
    unloaded_count = 0
    failed_unload_count = 0
    for ext in initial_loaded_cogs:
        try:
            await bot.unload_extension(ext)
            log.info(f"Unloaded: {ext}")
            unloaded_count += 1
        except Exception as e:
            log.error(f"Failed to unload {ext}. Error: {type(e).__name__}: {e}")
            failed_unload_count += 1

    await load_all_cogs_recursive() # Re-load all modules
    
    await ctx.send(f"Module reload process completed. Unloaded: {unloaded_count}, Failed to unload: {failed_unload_count}. New load attempts logged to console.")
    log.info("All modules reload process completed.")

# --- Bot Runtime ---
token = os.getenv("DISCORD_BOT_TOKEN")
if token:
    try:
        # Pass the bot's working directory to cogs for config loading
        # The bot's root directory is where bot.py resides
        bot.repo_root_dir = os.path.dirname(os.path.abspath(__file__)) 
        asyncio.run(bot.run(token))
    except discord.LoginFailure:
        log.critical("Failed to log in. Invalid DISCORD_BOT_TOKEN provided. Please check your .env file.")
        print("CRITICAL ERROR: Failed to log in. Please ensure DISCORD_BOT_TOKEN is correct in your .env file.")
    except discord.ConnectionClosed as e:
        log.error(f"Discord connection closed: {e}", exc_info=True)
        print(f"ERROR: Discord connection closed unexpectedly: {e}")
    except Exception as e:
        log.critical(f"An unhandled critical error occurred during bot runtime: {e}", exc_info=True)
        print(f"CRITICAL ERROR: An unexpected error occurred: {e}")
else:
    log.critical("DISCORD_BOT_TOKEN environment variable not found.")
    print("CRITICAL ERROR: DISCORD_BOT_TOKEN environment variable not found. Please create a .env file in the root directory with DISCORD_BOT_TOKEN='YOUR_BOT_TOKEN_HERE'")
