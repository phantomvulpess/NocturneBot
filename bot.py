@bot.event
async def on_ready():
    print(f"{bot.user} is online!")  # debug log
    if not daily_word.is_running():   # start loop only if not already running
        daily_word.start()

import discord
from discord.ext import commands, tasks
import os
import random
from dotenv import load_dotenv

# Load .env for Discord token
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Setup intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

# --- 200+ Korean words with English translations ---
korean_words = [
    ("안녕하세요", "Hello"), ("사랑", "Love"), ("행복", "Happiness"), ("가족", "Family"),
    ("친구", "Friend"), ("음식", "Food"), ("학교", "School"), ("책", "Book"), ("물", "Water"),
    ("시간", "Time"), ("날씨", "Weather"), ("좋아요", "Good"), ("영화", "Movie"), ("음악", "Music"),
    ("집", "Home"), ("공부", "Study"), ("오늘", "Today"), ("내일", "Tomorrow"), ("어제", "Yesterday"),
    ("맛있다", "Delicious"), ("축하", "Congratulations"), ("감사", "Thanks"), ("친절", "Kindness"),
    ("재미있다", "Fun"), ("슬프다", "Sad"), ("기쁘다", "Glad"), ("생각", "Thought"), ("좋다", "Good"),
    ("싫다", "Dislike"), ("바쁘다", "Busy"), ("편하다", "Comfortable"), ("힘들다", "Hard"),
    ("쉬다", "Rest"), ("걷다", "Walk"), ("달리다", "Run"), ("사다", "Buy"), ("팔다", "Sell"),
    ("듣다", "Listen"), ("보다", "See"), ("만나다", "Meet"), ("일하다", "Work"), ("놀다", "Play"),
    ("공원", "Park"), ("시장", "Market"), ("카페", "Cafe"), ("음료", "Drink"), ("커피", "Coffee"),
    ("차", "Tea"), ("영어", "English"), ("한국어", "Korean"), ("게임", "Game"), ("여행", "Travel"),
    ("사진", "Photo"), ("운동", "Exercise"), ("의자", "Chair"), ("테이블", "Table"), ("창문", "Window"),
    ("문", "Door"), ("음식점", "Restaurant"), ("병원", "Hospital"), ("은행", "Bank"), ("우체국", "Post Office"),
    ("전화", "Phone"), ("편지", "Letter"), ("인터넷", "Internet"), ("컴퓨터", "Computer"), ("휴대폰", "Cell Phone"),
    ("노래", "Song"), ("바다", "Sea"), ("산", "Mountain"), ("강", "River"), ("숲", "Forest"),
    ("꽃", "Flower"), ("동물", "Animal"), ("고양이", "Cat"), ("강아지", "Dog"), ("새", "Bird"),
    ("하늘", "Sky"), ("해", "Sun"), ("달", "Moon"), ("별", "Star"), ("비", "Rain"),
    ("눈", "Snow"), ("바람", "Wind"), ("운전", "Drive"), ("차량", "Vehicle"), ("자전거", "Bicycle"),
    ("길", "Road"), ("옷", "Clothes"), ("모자", "Hat"), ("신발", "Shoes"), ("가방", "Bag"),
    ("화장품", "Cosmetics"), ("시계", "Watch"), ("열쇠", "Key"), ("문서", "Document"), ("편안함", "Comfort"),
    ("행사", "Event"), ("공연", "Performance"), ("박물관", "Museum"), ("미술관", "Art Gallery"),
    ("영화관", "Cinema"), ("쇼핑", "Shopping"), ("맛집", "Famous Restaurant"), ("레스토랑", "Restaurant"),
    ("호텔", "Hotel"), ("카페인", "Caffeine"), ("커뮤니티", "Community"), ("친구들", "Friends"),
    ("가족들", "Family Members"), ("취미", "Hobby"), ("게임기", "Console"), ("휴가", "Vacation"),
    ("주말", "Weekend"), ("평일", "Weekday"), ("뉴스", "News"), ("소셜미디어", "Social Media"),
    ("블로그", "Blog"), ("도서관", "Library"), ("강의", "Lecture"), ("시험", "Exam"),
    ("점수", "Score"), ("성공", "Success"), ("실패", "Failure"), ("도전", "Challenge"),
    ("꿈", "Dream"), ("목표", "Goal"), ("희망", "Hope"), ("기억", "Memory"), ("생일", "Birthday"),
    ("선물", "Gift"), ("축제", "Festival"), ("문화", "Culture"), ("전통", "Tradition"), ("역사", "History"),
    ("이야기", "Story"), ("감정", "Emotion"), ("표현", "Expression"), ("아이디어", "Idea"), ("의견", "Opinion"),
    ("대화", "Dialogue"), ("메시지", "Message"), ("정보", "Information"), ("계획", "Plan"), ("프로젝트", "Project"),
    ("활동", "Activity"), ("여행지", "Travel Destination"), ("관광", "Tourism"), ("교통", "Transportation"),
    ("버스", "Bus"), ("지하철", "Subway"), ("택시", "Taxi"), ("편지함", "Mailbox"), ("음료수", "Beverage"),
    ("간식", "Snack"), ("빵", "Bread"), ("과일", "Fruit"), ("야채", "Vegetable"), ("고기", "Meat")
]

spanish_words = [
    ("hola", "hello"), ("amor", "love"), ("felicidad", "happiness"), ("familia", "family"),
    ("amigo", "friend"), ("comida", "food"), ("escuela", "school"), ("libro", "book"), ("agua", "water"),
    ("tiempo", "time"), ("clima", "weather"), ("bueno", "good"), ("película", "movie"), ("música", "music"),
    ("casa", "house"), ("estudiar", "study"), ("hoy", "today"), ("mañana", "tomorrow"), ("ayer", "yesterday"),
    ("delicioso", "delicious"), ("felicidades", "congratulations"), ("gracias", "thanks"), ("amable", "kind"),
    ("divertido", "fun"), ("triste", "sad"), ("alegre", "happy"), ("pensar", "think"), ("bien", "good"),
    ("mal", "bad"), ("ocupado", "busy"), ("cómodo", "comfortable"), ("difícil", "difficult"), ("descansar", "rest"),
    ("caminar", "walk"), ("correr", "run"), ("comprar", "buy"), ("vender", "sell"), ("escuchar", "listen"),
    ("ver", "see"), ("encontrar", "meet/find"), ("trabajar", "work"), ("jugar", "play"), ("parque", "park"),
    ("mercado", "market"), ("café", "cafe"), ("bebida", "drink"), ("té", "tea"), ("inglés", "english"),
    ("español", "spanish"), ("juego", "game"), ("viajar", "travel"), ("foto", "photo"), ("deporte", "sport"),
    ("silla", "chair"), ("mesa", "table"), ("ventana", "window"), ("puerta", "door"), ("restaurante", "restaurant"),
    ("hospital", "hospital"), ("banco", "bank"), ("correo", "post office"), ("teléfono", "phone"), ("carta", "letter"),
    ("internet", "internet"), ("computadora", "computer"), ("celular", "cell phone"), ("canción", "song"), ("pelota", "ball"),
    ("mar", "sea"), ("montaña", "mountain"), ("río", "river"), ("bosque", "forest"), ("flor", "flower"),
    ("animal", "animal"), ("gato", "cat"), ("perro", "dog"), ("pájaro", "bird"), ("cielo", "sky"),
    ("sol", "sun"), ("luna", "moon"), ("estrella", "star"), ("lluvia", "rain"), ("nieve", "snow"),
    ("viento", "wind"), ("conducir", "drive"), ("vehículo", "vehicle"), ("bicicleta", "bicycle"), ("camino", "road"),
    ("ropa", "clothes"), ("sombrero", "hat"), ("zapato", "shoe"), ("bolsa", "bag"), ("cosmético", "cosmetics"),
    ("reloj", "watch"), ("llave", "key"), ("documento", "document"), ("comodidad", "comfort"), ("evento", "event"),
    ("concierto", "concert"), ("museo", "museum"), ("galería", "art gallery"), ("cine", "cinema"), ("compras", "shopping"),
    ("restaurante", "restaurant"), ("hotel", "hotel"), ("cafeína", "caffeine"), ("comunidad", "community"), ("amigos", "friends"),
    ("familiares", "family members"), ("pasatiempo", "hobby"), ("consola", "console"), ("vacaciones", "vacation"),
    ("fin de semana", "weekend"), ("día laboral", "weekday"), ("noticias", "news"), ("redes sociales", "social media"),
    ("blog", "blog"), ("biblioteca", "library"), ("clase", "class"), ("examen", "exam"), ("nota", "score"),
    ("éxito", "success"), ("fracaso", "failure"), ("reto", "challenge"), ("sueño", "dream"), ("meta", "goal"),
    ("esperanza", "hope"), ("memoria", "memory"), ("cumpleaños", "birthday"), ("regalo", "gift"), ("festival", "festival"),
    ("cultura", "culture"), ("tradición", "tradition"), ("historia", "history"), ("cuento", "story"), ("emoción", "emotion"),
    ("expresión", "expression"), ("idea", "idea"), ("opinión", "opinion"), ("diálogo", "dialogue"), ("mensaje", "message"),
    ("información", "information"), ("plan", "plan"), ("proyecto", "project"), ("actividad", "activity"), ("viaje", "trip")
]

# --- Shuffle flashcards
korean_flashcards = korean_words.copy()
spanish_flashcards = spanish_words.copy()
random.shuffle(korean_flashcards)
random.shuffle(spanish_flashcards)

# --- Debug: see messages ---
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    print(f"Message received: {message.content}")
    await bot.process_commands(message)

# --- Flashcard Command ---
@bot.command()
async def flashcard(ctx, lang: str):
    if lang.lower() == "korean":
        word, eng = korean_flashcards.pop(0)
        korean_flashcards.append((word, eng))
    elif lang.lower() == "spanish":
        word, eng = spanish_flashcards.pop(0)
        spanish_flashcards.append((word, eng))
    else:
        await ctx.send("Supported languages: korean, spanish")
        return
    await ctx.send(f"**Flashcard ({lang.title()})**: {word} — {eng}")

# --- Daily Word ---
@tasks.loop(hours=24)
async def daily_word():
    await bot.wait_until_ready()
    channel_id = 1474450188914524251
    channel = bot.get_channel(channel_id)
    if channel is None:
        print("Daily word channel not found")
        return
    word_ko, eng_ko = random.choice(korean_words)
    word_es, eng_es = random.choice(spanish_words)
    await channel.send(f"**Daily Word Korean**: {word_ko} — {eng_ko}\n**Daily Word Spanish**: {word_es} — {eng_es}")


bot.run(TOKEN)
