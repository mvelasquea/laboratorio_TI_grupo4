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

# 15 Productos
productos = [
    (1,'Laptop HP Pavilion 15','Electrónica','Computadoras','ELEC-001',450,699.99,1,2.1,1825),
    (2,'iPhone 15 Pro Max','Electrónica','Smartphones','ELEC-002',899,1199.99,2,0.23,1095),
    (3,'Samsung Galaxy S24','Electrónica','Smartphones','ELEC-003',650,899.99,2,0.19,1095),
    (4,'Audífonos Sony WH-1000XM5','Electrónica','Audio','ELEC-005',250,349.99,3,0.25,1825),
    (5,'Smart TV LG 55','Electrónica','Televisores','ELEC-006',380,549.99,4,15.5,2555),
    (6,'PlayStation 5','Electrónica','Videojuegos','ELEC-007',400,499.99,5,4.5,2190),
    (7,'Camiseta Nike Dri-FIT','Ropa','Hombres','ROPA-001',12,29.99,7,0.2,730),
    (8,'Jeans Levis 501','Ropa','Hombres','ROPA-002',25,59.99,7,0.8,1095),
    (9,'Chaqueta North Face','Ropa','Unisex','ROPA-004',85,179.99,9,1.2,2190),
    (10,'Tenis Adidas Ultraboost','Ropa','Calzado','ROPA-005',75,149.99,10,0.6,1095),
    (11,'Arroz Faraón 1kg','Alimentos','Granos','ALIM-001',0.8,1.49,8,1,365),
    (12,'Coca-Cola 2L','Alimentos','Bebidas','ALIM-003',0.6,1.29,8,2,180),
    (13,'Leche Gloria 400ml','Alimentos','Lácteos','ALIM-005',0.6,1.19,8,0.42,30),
    (14,'Jabón Dove Original','Higiene','Cuidado Personal','HIGI-001',0.8,2.49,8,0.15,1095),
    (15,'Shampoo Pantene 400ml','Higiene','Cabello','HIGI-002',2.5,6.99,8,0.42,730),
]
c.executemany("INSERT INTO productos VALUES (?,?,?,?,?,?,?,?,?,?)", productos)

# 8 Tiendas
tiendas = [
    (1,'RetailNova Lima Centro','Perú','Lima','Física','Grande','Av. Principal 123','Carlos Mendoza','2018-01-15'),
    (2,'RetailNova Miraflores','Perú','Lima','Física','Mediana','Av. Larco 456','Ana Torres','2019-03-20'),
    (3,'RetailNova Bogotá Norte','Colombia','Bogotá','Física','Grande','Carrera 7 #45-67','Pedro Ramírez','2017-02-28'),
    (4,'RetailNova Santiago Centro','Chile','Santiago','Física','Grande','Av. Libertador 1234','Roberto Díaz','2016-05-10'),
    (5,'RetailNova Buenos Aires Norte','Argentina','Buenos Aires','Física','Grande','Av. Santa Fe 1234','Diego Martínez','2016-08-20'),
    (6,'RetailNova Ciudad de México','México','Ciudad de México','Física','Grande','Av. Reforma 3456','Alejandro Reyes','2015-03-15'),
    (7,'RetailNova São Paulo Centro','Brasil','São Paulo','Física','Grande','Av. Paulista 2345','Marcos Silva','2015-06-10'),
    (8,'RetailNova Online Latam','Perú','Lima','Online','Grande','Virtual','Digital Latam','2020-01-01'),
]
c.executemany("INSERT INTO tiendas VALUES (?,?,?,?,?,?,?,?,?)", tiendas)

# 6 Proveedores
proveedores = [
    (1,'TechSupply Corp','Estados Unidos','San José',7,95.5,'+1-408-555-0101','contact@techsupply.com'),
    (2,'Global Electronics','China','Shenzhen',15,92.3,'+86-755-555-0202','sales@globalelec.com'),
    (3,'AudioMax Solutions','Japón','Tokyo',12,97.8,'+81-3-555-0303','info@audiomax.jp'),
    (4,'GameZone Import','Estados Unidos','Los Ángeles',8,91.5,'+1-310-555-0505','wholesale@gamezone.com'),
    (5,'SportWorld Distribution','Estados Unidos','Portland',10,93.6,'+1-503-555-0909','sales@sportworld.com'),
    (6,'AgroIndustrial SAC','Perú','Lima',2,89.5,'+51-1-555-1919','ventas@agroindustrial.pe'),
]
c.executemany("INSERT INTO proveedores VALUES (?,?,?,?,?,?,?,?)", proveedores)

# 120 Inventarios (8 tiendas x 15 productos)
inventarios = []
id_inv = 1
for tienda_id in range(1, 9):
    for prod_id in range(1, 16):
        stock_min = random.randint(5, 20)
        stock_max = stock_min * 5
        stock_act = random.randint(max(1, stock_min - 5), stock_max)
        inventarios.append((id_inv, tienda_id, prod_id, stock_act, stock_min, stock_max, '2024-11-20'))
        id_inv += 1
c.executemany("INSERT INTO inventarios VALUES (?,?,?,?,?,?,?)", inventarios)

# ~100 Ventas
ventas = []
id_venta = 1
for dia in range(1, 16):
    fecha = f'2024-11-{dia:02d}'
    for _ in range(random.randint(4, 8)):
        tienda_id = random.randint(1, 8)
        prod_id = random.randint(1, 15)
        cantidad = random.randint(1, 5)
        precio = round(random.uniform(1, 300), 2)
        total = round(cantidad * precio, 2)
        metodo = random.choice(['Efectivo', 'Tarjeta Crédito', 'Tarjeta Débito'])
        ventas.append((id_venta, fecha, tienda_id, prod_id, cantidad, precio, total, metodo))
        id_venta += 1
c.executemany("INSERT INTO ventas VALUES (?,?,?,?,?,?,?,?)", ventas)

# ~40 Órdenes
ordenes = []
id_ord = 1
for dia in range(1, 16):
    fecha = f'2024-11-{dia:02d}'
    for _ in range(random.randint(1, 3)):
        tienda_id = random.randint(1, 8)
        prov_id = random.randint(1, 6)
        estado = random.choice(['Entregado', 'Enviado', 'Pendiente'])
        total = round(random.uniform(500, 15000), 2)
        fecha_ent = f'2024-11-{min(dia + random.randint(3, 10), 28):02d}'
        ordenes.append((id_ord, fecha, tienda_id, prov_id, estado, total, fecha_ent))
        id_ord += 1
c.executemany("INSERT INTO ordenes VALUES (?,?,?,?,?,?,?)", ordenes)

# ~40 Envíos
envios = []
id_env = 1
for ord_id in range(1, id_ord):
    transportista = random.choice(['FedEx', 'DHL', 'UPS', 'Servientrega'])
    origen = random.choice(['San José, USA', 'Shenzhen, China', 'Lima, Perú', 'Bogotá, Colombia'])
    destino = random.choice(['Lima, Perú', 'Bogotá, Colombia', 'Santiago, Chile', 'Buenos Aires, Argentina'])
    estado = random.choice(['Entregado', 'En Transito', 'Pendiente'])
    fecha_sal = f'2024-11-{random.randint(1, 15):02d}'
    fecha_lleg = f'2024-11-{random.randint(8, 28):02d}' if estado == 'Entregado' else None
    costo = round(random.uniform(20, 500), 2)
    envios.append((id_env, ord_id, transportista, origen, destino, estado, fecha_sal, fecha_lleg, costo))
    id_env += 1
c.executemany("INSERT INTO envios VALUES (?,?,?,?,?,?,?,?,?)", envios)

# 120 Pronósticos (8 tiendas x 15 productos)
pronosticos = []
id_pr = 1
for tienda_id in range(1, 9):
    for prod_id in range(1, 16):
        estimada = random.randint(10, 80)
        real = estimada + random.randint(-10, 10)
        prec = round(100 - abs(estimada - real) / estimada * 100, 1)
        pronosticos.append((id_pr, tienda_id, prod_id, '2024-11-15', estimada, max(0, real), prec))
        id_pr += 1
c.executemany("INSERT INTO pronosticos VALUES (?,?,?,?,?,?,?)", pronosticos)

# 8 KPIs
kpis = []
for tienda_id in range(1, 9):
    ventas_t = round(random.uniform(20000, 60000), 2)
    ordenes_t = random.randint(50, 150)
    rotura = round(random.uniform(2, 6), 2)
    entrega = round(random.uniform(4, 8), 1)
    costo = round(random.uniform(800, 2000), 2)
    precision = round(random.uniform(88, 97), 1)
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
    print(f'{t}: {count} registros')
print(f'\nTotal: {total} registros')
conn.close()
