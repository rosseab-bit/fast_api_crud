from database import SessionLocal
from models import Producto

db = SessionLocal()

productos = [
    Producto(nombre="Notebook Lenovo i5", precio=850000, stock=10),
    Producto(nombre="Mouse Logitech G203", precio=12000, stock=25),
    Producto(nombre="Teclado Redragon Kumara", precio=18000, stock=5),
    Producto(nombre="Monitor Samsung 24\"", precio=150000, stock=7),
    Producto(nombre="Disco SSD Kingston 480GB", precio=36000, stock=20),
    Producto(nombre="Memoria RAM 8GB DDR4", precio=22000, stock=30),
    Producto(nombre="Placa de video RTX 4060", precio=550000, stock=3),
    Producto(nombre="Silla Gamer Cougar", precio=130000, stock=2),
    Producto(nombre="Auriculares HyperX Cloud II", precio=24000, stock=15),
    Producto(nombre="Webcam Logitech C920", precio=49000, stock=0),
]

db.add_all(productos)
db.commit()
db.close()
