
import os
import discord
import moviepy.editor as mp


def run_discord_bot():
    TOKEN = os.getenv("DISCORD_TOKEN")
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f"{client.user} has connected to Discord!")
    
    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        author = message.author
        # user_message = str(message.content)
        # channel = str(message.channel)
        attachment = message.attachments[0] if len(message.attachments) > 0 else None
        if attachment and attachment.filename.endswith('.webm'):
            webm_filename = attachment.filename
            mp4_filename = webm_filename.replace('.webm', '.mp4')
            await attachment.save(webm_filename)

            video_clip = mp.VideoFileClip(webm_filename)
            video_clip.write_videofile(mp4_filename, codec="libx264")
            video_clip.close()
            await message.delete()

            await message.channel.send(f"<@{author.id}> sent:",file=discord.File(mp4_filename))

            os.remove(webm_filename)
            os.remove(mp4_filename)
        
    client.run(TOKEN)
