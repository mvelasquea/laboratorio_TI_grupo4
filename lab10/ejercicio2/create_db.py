import sqlite3
import os
import random

random.seed(42)

DB_PATH = os.path.join(os.path.dirname(__file__), "retailnova.db")

if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.executescript("""
CREATE TABLE productos (
    id INTEGER PRIMARY KEY, nombre TEXT, categoria TEXT, subcategoria TEXT,
    sku TEXT UNIQUE, precio_costo REAL, precio_venta REAL, proveedor_id INTEGER,
    peso_kg REAL, vida_util_dias INTEGER
);
CREATE TABLE tiendas (
    id INTEGER PRIMARY KEY, nombre TEXT, pais TEXT, ciudad TEXT,
    tipo TEXT, tamano TEXT, direccion TEXT, gerente TEXT, fecha_apertura DATE
);
CREATE TABLE proveedores (
    id INTEGER PRIMARY KEY, nombre TEXT, pais TEXT, ciudad TEXT,
    tiempo_entrega_dias INTEGER, confiabilidad_score REAL, telefono TEXT, email TEXT
);
CREATE TABLE inventarios (
    id INTEGER PRIMARY KEY, tienda_id INTEGER, producto_id INTEGER,
    stock_actual INTEGER, stock_minimo INTEGER, stock_maximo INTEGER,
    fecha_ultima_reposicion DATE
);
CREATE TABLE ventas (
    id INTEGER PRIMARY KEY, fecha DATE, tienda_id INTEGER, producto_id INTEGER,
    cantidad INTEGER, precio_unitario REAL, total REAL, metodo_pago TEXT
);
CREATE TABLE ordenes (
    id INTEGER PRIMARY KEY, fecha DATE, tienda_id INTEGER, proveedor_id INTEGER,
    estado TEXT, total REAL, fecha_estimada_entrega DATE
);
CREATE TABLE envios (
    id INTEGER PRIMARY KEY, orden_id INTEGER, transportista TEXT,
    origen TEXT, destino TEXT, estado TEXT, fecha_salida DATE,
    fecha_llegada DATE, costo_envio REAL
);
CREATE TABLE pronosticos (
    id INTEGER PRIMARY KEY, tienda_id INTEGER, producto_id INTEGER,
    fecha DATE, demanda_estimada INTEGER, demanda_real INTEGER, precision_val REAL
);
CREATE TABLE kpis (
    id INTEGER PRIMARY KEY, tienda_id INTEGER, mes INTEGER, anio INTEGER,
    tasa_rotura_stock REAL, tiempo_promedio_entrega REAL,
    costo_logistica REAL, precision_pronostico REAL,
    ventas_totales REAL, numero_ordenes INTEGER
);
""")

# 10 Productos
productos = [
    (1,'Laptop HP Pavilion 15','Electrónica','Computadoras','ELEC-001',450,699.99,1,2.1,1825),
    (2,'iPhone 15 Pro Max','Electrónica','Smartphones','ELEC-002',899,1199.99,2,0.23,1095),
    (3,'Samsung Galaxy S24','Electrónica','Smartphones','ELEC-003',650,899.99,2,0.19,1095),
    (4,'Audífonos Sony','Electrónica','Audio','ELEC-005',250,349.99,3,0.25,1825),
    (5,'PlayStation 5','Electrónica','Videojuegos','ELEC-007',400,499.99,4,4.5,2190),
    (6,'Camiseta Nike','Ropa','Hombres','ROPA-001',12,29.99,5,0.2,730),
    (7,'Jeans Levis','Ropa','Hombres','ROPA-002',25,59.99,5,0.8,1095),
    (8,'Coca-Cola 2L','Alimentos','Bebidas','ALIM-001',0.6,1.29,6,2,180),
    (9,'Leche Gloria','Alimentos','Lácteos','ALIM-002',0.6,1.19,6,0.42,30),
    (10,'Jabón Dove','Higiene','Cuidado','HIGI-001',0.8,2.49,6,0.15,1095),
]
c.executemany("INSERT INTO productos VALUES (?,?,?,?,?,?,?,?,?,?)", productos)

# 4 Tiendas
tiendas = [
    (1,'RetailNova Lima Centro','Perú','Lima','Física','Grande','Av. Principal 123','Carlos Mendoza','2018-01-15'),
    (2,'RetailNova Bogotá','Colombia','Bogotá','Física','Grande','Carrera 7 #45-67','Pedro Ramírez','2017-02-28'),
    (3,'RetailNova Santiago','Chile','Santiago','Física','Grande','Av. Libertador 1234','Roberto Díaz','2016-05-10'),
    (4,'RetailNova Online Latam','Perú','Lima','Online','Grande','Virtual','Digital Latam','2020-01-01'),
]
c.executemany("INSERT INTO tiendas VALUES (?,?,?,?,?,?,?,?,?)", tiendas)

# 4 Proveedores
proveedores = [
    (1,'TechSupply Corp','USA','San José',7,95.5,'+1-408-555-0101','contact@techsupply.com'),
    (2,'Global Electronics','China','Shenzhen',15,92.3,'+86-755-555-0202','sales@globalelec.com'),
    (3,'AudioMax Solutions','Japón','Tokyo',12,97.8,'+81-3-555-0303','info@audiomax.jp'),
    (4,'AgroIndustrial SAC','Perú','Lima',2,89.5,'+51-1-555-1919','ventas@agroindustrial.pe'),
]
c.executemany("INSERT INTO proveedores VALUES (?,?,?,?,?,?,?,?)", proveedores)

# 40 Inventarios (4 tiendas x 10 productos)
inventarios = []
id_inv = 1
for tienda_id in range(1, 5):
    for prod_id in range(1, 11):
        stock_min = random.randint(5, 15)
        stock_max = stock_min * 4
        stock_act = random.randint(max(1, stock_min - 4), stock_max)
        inventarios.append((id_inv, tienda_id, prod_id, stock_act, stock_min, stock_max, '2024-11-20'))
        id_inv += 1
c.executemany("INSERT INTO inventarios VALUES (?,?,?,?,?,?,?)", inventarios)

# 30 Ventas
ventas = []
id_venta = 1
for dia in range(1, 11):
    fecha = f'2024-11-{dia:02d}'
    for _ in range(random.randint(2, 4)):
        tienda_id = random.randint(1, 4)
        prod_id = random.randint(1, 10)
        cantidad = random.randint(1, 3)
        precio = round(random.uniform(1, 200), 2)
        total = round(cantidad * precio, 2)
        metodo = random.choice(['Efectivo', 'Tarjeta Crédito', 'Tarjeta Débito'])
        ventas.append((id_venta, fecha, tienda_id, prod_id, cantidad, precio, total, metodo))
        id_venta += 1
c.executemany("INSERT INTO ventas VALUES (?,?,?,?,?,?,?,?)", ventas)

# 15 Órdenes
ordenes = []
id_ord = 1
for dia in range(1, 11):
    fecha = f'2024-11-{dia:02d}'
    for _ in range(1):
        tienda_id = random.randint(1, 4)
        prov_id = random.randint(1, 4)
        estado = random.choice(['Entregado', 'Enviado', 'Pendiente'])
        total = round(random.uniform(500, 10000), 2)
        fecha_ent = f'2024-11-{min(dia + random.randint(3, 8), 28):02d}'
        ordenes.append((id_ord, fecha, tienda_id, prov_id, estado, total, fecha_ent))
        id_ord += 1
c.executemany("INSERT INTO ordenes VALUES (?,?,?,?,?,?,?)", ordenes)

# 15 Envíos
envios = []
id_env = 1
for ord_id in range(1, id_ord):
    transportista = random.choice(['FedEx', 'DHL', 'UPS', 'Servientrega'])
    origen = random.choice(['San José, USA', 'Shenzhen, China', 'Lima, Perú'])
    destino = random.choice(['Lima, Perú', 'Bogotá, Colombia', 'Santiago, Chile'])
    estado = random.choice(['Entregado', 'En Transito', 'Pendiente'])
    fecha_sal = f'2024-11-{random.randint(1, 10):02d}'
    fecha_lleg = f'2024-11-{random.randint(5, 28):02d}' if estado == 'Entregado' else None
    costo = round(random.uniform(20, 400), 2)
    envios.append((id_env, ord_id, transportista, origen, destino, estado, fecha_sal, fecha_lleg, costo))
    id_env += 1
c.executemany("INSERT INTO envios VALUES (?,?,?,?,?,?,?,?,?)", envios)

# 40 Pronósticos (4 tiendas x 10 productos)
pronosticos = []
id_pr = 1
for tienda_id in range(1, 5):
    for prod_id in range(1, 11):
        estimada = random.randint(10, 60)
        real = estimada + random.randint(-8, 8)
        prec = round(100 - abs(estimada - real) / estimada * 100, 1)
        pronosticos.append((id_pr, tienda_id, prod_id, '2024-11-15', estimada, max(0, real), prec))
        id_pr += 1
c.executemany("INSERT INTO pronosticos VALUES (?,?,?,?,?,?,?)", pronosticos)

# 4 KPIs
kpis = []
for tienda_id in range(1, 5):
    ventas_t = round(random.uniform(15000, 50000), 2)
    ordenes_t = random.randint(30, 100)
    rotura = round(random.uniform(2, 5), 2)
    entrega = round(random.uniform(4, 7), 1)
    costo = round(random.uniform(600, 1500), 2)
    precision = round(random.uniform(89, 96), 1)
    kpis.append((tienda_id, tienda_id, 11, 2024, rotura, entrega, costo, precision, ventas_t, ordenes_t))
c.executemany("INSERT INTO kpis VALUES (?,?,?,?,?,?,?,?,?,?)", kpis)

conn.commit()
conn.close()

# Verificar
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
cur.execute('SELECT name FROM sqlite_master WHERE type=?', ('table',))
tables = [r[0] for r in cur.fetchall()]
total = 0
for t in tables:
    cur.execute(f'SELECT COUNT(*) FROM [{t}]')
    count = cur.fetchone()[0]
    total += count
    print(f'{t}: {count}')
print(f'\nTotal: {total} registros')
conn.close()
