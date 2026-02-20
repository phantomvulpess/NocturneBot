import discord
from discord.ext import commands, tasks
import random
import os
from dotenv import load_dotenv

# Load bot token from .env or Railway/GitHub secrets
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Expanded high-frequency vocab lists for Korean and Spanish (100+ words each)
daily_words = {
    "Korean": [
        "안녕하세요 (hello)", "사랑 (love)", "감사합니다 (thank you)", "행복 (happiness)", "친구 (friend)",
        "집 (home)", "음식 (food)", "물 (water)", "학교 (school)", "책 (book)", "시간 (time)", "사람 (person)",
        "언어 (language)", "가족 (family)", "일 (work)", "음악 (music)", "영화 (movie)", "컴퓨터 (computer)",
        "노래 (song)", "꽃 (flower)", "밤 (night)", "아침 (morning)", "도시 (city)", "길 (road)", "바다 (sea)",
        "산 (mountain)", "하늘 (sky)", "생각 (thought)", "꿈 (dream)", "기억 (memory)", "마음 (mind)",
        "자연 (nature)", "운동 (exercise)", "여행 (travel)", "사진 (photo)", "게임 (game)", "문화 (culture)",
        "미래 (future)", "현재 (present)", "과거 (past)", "친절 (kindness)", "용기 (courage)", "평화 (peace)",
        "희망 (hope)", "자유 (freedom)", "기쁨 (joy)", "슬픔 (sadness)", "맛 (taste)", "냄새 (smell)", "소리 (sound)",
        "옷 (clothes)", "차 (car)", "버스 (bus)", "비행기 (plane)", "영화관 (cinema)", "공원 (park)", "시장 (market)",
        "가게 (store)", "음료 (drink)", "과일 (fruit)", "채소 (vegetable)", "친구들 (friends)", "선생님 (teacher)",
        "학생 (student)", "음악회 (concert)", "공연 (performance)", "축제 (festival)", "계절 (season)", "겨울 (winter)",
        "봄 (spring)", "여름 (summer)", "가을 (fall)", "병원 (hospital)", "약 (medicine)", "전화 (phone)",
        "컴퓨터게임 (computer game)", "인터넷 (internet)", "노트북 (laptop)", "사진기 (camera)", "책상 (desk)",
        "의자 (chair)", "침대 (bed)", "창문 (window)", "문 (door)", "거리 (street)", "건물 (building)",
        "공기 (air)", "불 (fire)", "물건 (thing)", "손 (hand)", "발 (foot)", "눈 (eye)", "귀 (ear)", "입 (mouth)"
    ],
    "Spanish": [
        "hola (hello)", "amor (love)", "gracias (thank you)", "felicidad (happiness)", "amigo (friend)",
        "casa (home)", "comida (food)", "agua (water)", "escuela (school)", "libro (book)", "tiempo (time)",
        "persona (person)", "lengua (language)", "familia (family)", "trabajo (work)", "música (music)",
        "película (movie)", "computadora (computer)", "canción (song)", "flor (flower)", "noche (night)",
        "mañana (morning)", "ciudad (city)", "camino (road)", "mar (sea)", "montaña (mountain)", "cielo (sky)",
        "pensamiento (thought)", "sueño (dream)", "recuerdo (memory)", "mente (mind)", "naturaleza (nature)",
        "ejercicio (exercise)", "viaje (travel)", "foto (photo)", "juego (game)", "cultura (culture)",
        "futuro (future)", "presente (present)", "pasado (past)", "amabilidad (kindness)", "valentía (courage)",
        "paz (peace)", "esperanza (hope)", "libertad (freedom)", "alegría (joy)", "tristeza (sadness)",
        "sabor (taste)", "olor (smell)", "sonido (sound)", "ropa (clothes)", "coche (car)", "autobús (bus)",
        "avión (plane)", "cine (cinema)", "parque (park)", "mercado (market)", "tienda (store)", "bebida (drink)",
        "fruta (fruit)", "verdura (vegetable)", "amigos (friends)", "profesor (teacher)", "estudiante (student)",
        "concierto (concert)", "espectáculo (performance)", "festival (festival)", "estación (season)", "invierno (winter)",
        "primavera (spring)", "verano (summer)", "otoño (fall)", "hospital (hospital)", "medicina (medicine)",
        "teléfono (phone)", "videojuego (video game)", "internet (internet)", "portátil (laptop)", "cámara (camera)",
        "escritorio (desk)", "silla (chair)", "cama (bed)", "ventana (window)", "puerta (door)", "calle (street)",
        "edificio (building)", "aire (air)", "fuego (fire)", "cosa (thing)", "mano (hand)", "pie (foot)", "ojo (eye)",
        "oreja (ear)", "boca (mouth)"
    ]
}

# Shuffle lists for flashcards
flashcards = {lang: daily_words[lang][:] for lang in daily_words}
for lang in flashcards:
    random.shuffle(flashcards[lang])

# Dictionary index trackers
indexes = {lang: 0 for lang in flashcards}

# Replace with your Discord channel ID
CHANNEL_ID = 1474450188914524251

@bot.event
async def on_ready():
    print(f'{bot.user} is online!')
    send_daily_word.start()

# Daily word task
@tasks.loop(hours=24)
async def send_daily_word():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        for lang in daily_words:
            word = random.choice(daily_words[lang])
            await channel.send(f"**Daily Word ({lang})**: {word}")

# Flashcard command
@bot.command()
async def flashcard(ctx, language: str):
    language = language.capitalize()
    if language not in flashcards:
        await ctx.send(f"Language not supported. Choose: {', '.join(flashcards.keys())}")
        return

    index = indexes[language]
    word = flashcards[language][index]
    indexes[language] = (index + 1) % len(flashcards[language])  # rotate endlessly
    await ctx.send(f"**Flashcard ({language})**: {word}")

bot.run(TOKEN)
