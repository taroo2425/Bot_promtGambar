# This example requires the 'message_content' intent.
import asyncio
import discord
from config import TOKEN
import main as fusionbrain, base64
import os


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
    
    if message.content.startswith('$start') or message.content.startswith('$help'):
        async with message.channel.typing():
            help_embed = discord.Embed(
                title="🤖 FusionBrain Bot",
                description="Bot AI image generator menggunakan Fusion Brain API",
                color=discord.Color.blue()
            )
            help_embed.add_field(
                name="📝 Perintah Tersedia:",
                value=(
                    "`$start` atau `$help` - Tampilkan bantuan ini\n"
                    "`$hello` - Sapaan sederhana\n"
                    "`$generate <prompt>` - Generate gambar dari prompt"
                ),
                inline=False
            )
            help_embed.add_field(
                name="📖 Cara Menggunakan:",
                value=(
                    "Gunakan `$generate` diikuti dengan deskripsi gambar yang ingin Anda buat.\n\n"
                    "**Contoh:**\n"
                    "`$generate beautiful sunset over mountains`"
                ),
                inline=False
            )
            help_embed.add_field(
                name="⚙️ Fitur:",
                value=(
                    "✅ Generate gambar AI berkualitas tinggi\n"
                    "✅ Simpan hasil sebagai file PNG\n"
                    "✅ Support prompt bahasa Indonesia"
                ),
                inline=False
            )
            help_embed.set_footer(text="Gunakan perintah dengan prefix $ untuk mengaktifkan bot")
            await message.channel.send(embed=help_embed)
    
    if message.content.startswith('$hello'):
        async with message.channel.typing():
            await message.channel.send('Hello!')

    if message.content.startswith('$generate'):
        prompt = message.content[len('$generate '):].strip()

        if not prompt:
            await message.channel.send("❗ Masukkan prompt setelah `$generate`")
            return

        # 1️⃣ kirim pesan status
        status_message = await message.channel.send("🧠 Sedang membuat gambar...")

        try:
            loop = asyncio.get_running_loop()

            # 2️⃣ jalankan FusionBrain di thread (anti freeze)
            def generate_image():
                api = fusionbrain.FusionBrainAPI(
                    'https://api-key.fusionbrain.ai/',
                    fusionbrain.API_KEY,
                    fusionbrain.API_SECRET
                )
                pipeline_id = api.get_pipeline()
                uuid = api.generate(prompt, pipeline_id)
                files = api.check_generation(uuid)
                return uuid, files

            uuid, files = await loop.run_in_executor(None, generate_image)

            # 3️⃣ simpan gambar sementara
            image_data = base64.b64decode(files[0])
            filename = f"generated_{uuid}.png"

            with open(filename, "wb") as f:
                f.write(image_data)

            # 4️⃣ kirim gambar
            await message.channel.send(file=discord.File(filename))

            # 5️⃣ hapus pesan status
            await status_message.delete()

            # 6️⃣ hapus file lokal
            os.remove(filename)

        except Exception as e:
            await status_message.edit(content=f"❌ Gagal membuat gambar:\n`{e}`")

client.run(TOKEN)
