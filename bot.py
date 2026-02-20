# bot.py - Discord Vocabulary Bot (Daily Words + Flashcards)
# Mac-friendly, beginner-ready

import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
import random

# ========================
# Load Token
# ========================
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# ========================
# Bot Setup
# ========================
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ========================
# Vocabulary Lists (50+ words each)
# ========================
daily_words = {
    "Korean": [
        "사랑 (love)", "행복 (happiness)", "친구 (friend)", "음식 (food)", "학교 (school)",
        "집 (house)", "가족 (family)", "시간 (time)", "물 (water)", "사람 (person)",
        "생각 (thought)", "일 (work)", "언어 (language)", "책 (book)", "영화 (movie)",
        "노래 (song)", "차 (car/tea)", "날씨 (weather)", "도시 (city)", "음악 (music)",
        "문제 (problem)", "도움 (help)", "선물 (gift)", "꿈 (dream)", "희망 (hope)",
        "강아지 (puppy)", "고양이 (cat)", "길 (road)", "사진 (photo)", "게임 (game)",
        "운동 (exercise)", "꽃 (flower)", "색 (color)", "친절 (kindness)", "소리 (sound)",
        "바다 (sea)", "산 (mountain)", "강 (river)", "길거리 (street)", "시장 (market)",
        "음식점 (restaurant)", "공원 (park)", "쇼핑 (shopping)", "생일 (birthday)", "선생님 (teacher)",
        "학생 (student)", "회사 (company)", "돈 (money)", "사랑하다 (to love)", "먹다 (to eat)"
    ],
    "French": [
        "bonjour (hello)", "merci (thank you)", "amour (love)", "maison (house)", "ami (friend)",
        "famille (family)", "temps (time)", "eau (water)", "personne (person)", "travail (work)",
        "langue (language)", "livre (book)", "film (movie)", "chanson (song)", "voiture (car)",
        "thé (tea)", "météo (weather)", "ville (city)", "musique (music)", "problème (problem)",
        "aide (help)", "cadeau (gift)", "rêve (dream)", "espoir (hope)", "chien (dog)",
        "chat (cat)", "chemin (road)", "photo (photo)", "jeu (game)", "exercice (exercise)",
        "fleur (flower)", "couleur (color)", "gentillesse (kindness)", "son (sound)", "mer (sea)",
        "montagne (mountain)", "rivière (river)", "rue (street)", "marché (market)", "restaurant (restaurant)",
        "parc (park)", "shopping (shopping)", "anniversaire (birthday)", "professeur (teacher)", "étudiant (student)",
        "entreprise (company)", "argent (money)", "aimer (to love)", "manger (to eat)", "boire (to drink)"
    ],
    "German": [
        "haus (house)", "freund (friend)", "liebe (love)", "essen (food)", "schule (school)",
        "familie (family)", "zeit (time)", "wasser (water)", "person (person)", "arbeit (work)",
        "sprache (language)", "buch (book)", "film (movie)", "lied (song)", "auto (car)",
        "tee (tea)", "wetter (weather)", "stadt (city)", "musik (music)", "problem (problem)",
        "hilfe (help)", "geschenk (gift)", "traum (dream)", "hoffnung (hope)", "hund (dog)",
        "katze (cat)", "weg (road)", "foto (photo)", "spiel (game)", "übung (exercise)",
        "blume (flower)", "farbe (color)", "freundlichkeit (kindness)", "geräusch (sound)", "meer (sea)",
        "berg (mountain)", "fluss (river)", "straße (street)", "markt (market)", "restaurant (restaurant)",
        "park (park)", "einkaufen (shopping)", "geburtstag (birthday)", "lehrer (teacher)", "schüler (student)",
        "firma (company)", "geld (money)", "lieben (to love)", "essen (to eat)", "trinken (to drink)"
    ],
    "Spanish": [
        "amor (love)", "feliz (happy)", "casa (house)", "amigo (friend)", "familia (family)",
        "tiempo (time)", "agua (water)", "persona (person)", "trabajo (work)", "idioma (language)",
        "libro (book)", "película (movie)", "canción (song)", "coche (car)", "té (tea)",
        "clima (weather)", "ciudad (city)", "música (music)", "problema (problem)", "ayuda (help)",
        "regalo (gift)", "sueño (dream)", "esperanza (hope)", "perro (dog)", "gato (cat)",
        "camino (road)", "foto (photo)", "juego (game)", "ejercicio (exercise)", "flor (flower)",
        "color (color)", "amabilidad (kindness)", "sonido (sound)", "mar (sea)", "montaña (mountain)",
        "río (river)", "calle (street)", "mercado (market)", "restaurante (restaurant)", "parque (park)",
        "compras (shopping)", "cumpleaños (birthday)", "profesor (teacher)", "estudiante (student)", "empresa (company)",
        "dinero (money)", "amar (to love)", "comer (to eat)", "beber (to drink)", "leer (to read)"
    ],
    "Japanese": [
        "愛 (ai – love)", "幸せ (shiawase – happiness)", "友達 (tomodachi – friend)", "食べ物 (tabemono – food)", "学校 (gakkou – school)",
        "家 (ie – house)", "家族 (kazoku – family)", "時間 (jikan – time)", "水 (mizu – water)", "人 (hito – person)",
        "考え (kangae – thought)", "仕事 (shigoto – work)", "言語 (gengo – language)", "本 (hon – book)", "映画 (eiga – movie)",
        "歌 (uta – song)", "車 (kuruma – car)", "お茶 (ocha – tea)", "天気 (tenki – weather)", "都市 (toshi – city)",
        "音楽 (ongaku – music)", "問題 (mondai – problem)", "助け (tasuke – help)", "贈り物 (okurimono – gift)", "夢 (yume – dream)",
        "希望 (kibou – hope)", "犬 (inu – dog)", "猫 (neko – cat)", "道 (michi – road)", "写真 (shashin – photo)",
        "ゲーム (geemu – game)", "運動 (undou – exercise)", "花 (hana – flower)", "色 (iro – color)", "親切 (shinsetsu – kindness)",
        "音 (oto – sound)", "海 (umi – sea)", "山 (yama – mountain)", "川 (kawa – river)", "通り (toori – street)",
        "市場 (ichiba – market)", "レストラン (resutoran – restaurant)", "公園 (kouen – park)", "買い物 (kaimono – shopping)", "誕生日 (tanjoubi – birthday)",
        "先生 (sensei – teacher)", "学生 (gakusei – student)", "会社 (kaisha – company)", "お金 (okane – money)", "愛する (aisuru – to love)"
    ]
}

# ========================
# Flashcard tracking
# ========================
flashcard_index = {lang: 0 for lang in daily_words}

# Shuffle each language list at startup
for lang in daily_words:
    random.shuffle(daily_words[lang])

# ========================
# Bot Events
# ========================
@bot.event
async def on_ready():
    print(f"{bot.user} is online!")
    send_daily_word.start()  # Start daily word loop

# ========================
# Daily Word Task (every 24h)
# ========================
@tasks.loop(hours=24)
async def send_daily_word():
    # Replace with your Discord channel ID
    channel = bot.get_channel(1474450188914524251)  # e.g., 123456789012345678
    if channel is None:
        print("Error: Channel not found. Check YOUR_CHANNEL_ID and permissions.")
        return

    lang = random.choice(list(daily_words.keys()))
    word = random.choice(daily_words[lang])
    await channel.send(f"**Daily Word ({lang})**: {word}")

# ========================
# Flashcard Command
# ========================
@bot.command()
async def flashcard(ctx, language):
    language = language.capitalize()
    if language in daily_words:
        index = flashcard_index[language]
        word = daily_words[language][index]
        await ctx.send(f"**Flashcard ({language})**: {word}")
        flashcard_index[language] = (index + 1) % len(daily_words[language])
    else:
        await ctx.send("Language not found. Options: Korean, French, German, Spanish, Japanese")

# ========================
# Run Bot
# ========================
bot.run(TOKEN)
