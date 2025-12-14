# This example requires the 'message_content' intent.
import discord
from config import TOKEN
import main as fusionbrain, base64

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')


    if message.content.startswith('$generate'):
        prompt = message.content[len('$generate '):]
        await message.channel.send(f'Generating image for prompt: {prompt}')

        api = fusionbrain.FusionBrainAPI('https://api-key.fusionbrain.ai/', fusionbrain.API_KEY, fusionbrain.API_SECRET)
        pipeline_id = api.get_pipeline()
        uuid = api.generate(prompt, pipeline_id)
        files = api.check_generation(uuid)

        encoded_string = files[0]
        decoded_data = base64.b64decode(encoded_string)

        with open('generated_image.png', 'wb') as f:
            f.write(decoded_data)

        await message.channel.send(file=discord.File('generated_image.png'))

client.run(TOKEN)
