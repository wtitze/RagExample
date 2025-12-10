from pymongo import MongoClient

uri = "mongodb+srv://webUser:9yW6dCxE8wXgnwS@cluster0.s6rcev7.mongodb.net/?retryWrites=true&w=majority&authSource=admin"
client = MongoClient(uri)

try:
    client.admin.command("ping")
    print("CONNESSIONE OK")
except Exception as e:
    print("ERRORE:", e)