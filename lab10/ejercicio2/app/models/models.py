from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.models.database import Base


class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    categoria = Column(String, nullable=False)
    subcategoria = Column(String, nullable=False)
    sku = Column(String, unique=True, nullable=False)
    precio_costo = Column(Float, nullable=False)
    precio_venta = Column(Float, nullable=False)
    proveedor_id = Column(Integer, ForeignKey("proveedores.id"))
    peso_kg = Column(Float)
    vida_util_dias = Column(Integer)


class Tienda(Base):
    __tablename__ = "tiendas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    pais = Column(String, nullable=False)
    ciudad = Column(String, nullable=False)
    tipo = Column(String, nullable=False)
    tamano = Column(String, nullable=False)
    direccion = Column(String)
    gerente = Column(String)
    fecha_apertura = Column(Date)


class Proveedor(Base):
    __tablename__ = "proveedores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    pais = Column(String, nullable=False)
    ciudad = Column(String, nullable=False)
    tiempo_entrega_dias = Column(Integer, nullable=False)
    confiabilidad_score = Column(Float, nullable=False)
    telefono = Column(String)
    email = Column(String)


class Inventario(Base):
    __tablename__ = "inventarios"

    id = Column(Integer, primary_key=True, index=True)
    tienda_id = Column(Integer, ForeignKey("tiendas.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    stock_actual = Column(Integer, nullable=False)
    stock_minimo = Column(Integer, nullable=False)
    stock_maximo = Column(Integer, nullable=False)
    fecha_ultima_reposicion = Column(Date)

    tienda = relationship("Tienda")
    producto = relationship("Producto")


class Venta(Base):
    __tablename__ = "ventas"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, nullable=False)
    tienda_id = Column(Integer, ForeignKey("tiendas.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)
    total = Column(Float, nullable=False)
    metodo_pago = Column(String)

    tienda = relationship("Tienda")
    producto = relationship("Producto")


class Orden(Base):
    __tablename__ = "ordenes"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, nullable=False)
    tienda_id = Column(Integer, ForeignKey("tiendas.id"), nullable=False)
    proveedor_id = Column(Integer, ForeignKey("proveedores.id"), nullable=False)
    estado = Column(String, nullable=False)
    total = Column(Float, nullable=False)
    fecha_estimada_entrega = Column(Date)

    tienda = relationship("Tienda")
    proveedor = relationship("Proveedor")


class Envio(Base):
    __tablename__ = "envios"

    id = Column(Integer, primary_key=True, index=True)
    orden_id = Column(Integer, ForeignKey("ordenes.id"), nullable=False)
    transportista = Column(String, nullable=False)
    origen = Column(String, nullable=False)
    destino = Column(String, nullable=False)
    estado = Column(String, nullable=False)
    fecha_salida = Column(Date)
    fecha_llegada = Column(Date)
    costo_envio = Column(Float)

    orden = relationship("Orden")


class Pronostico(Base):
    __tablename__ = "pronosticos"

    id = Column(Integer, primary_key=True, index=True)
    tienda_id = Column(Integer, ForeignKey("tiendas.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    fecha = Column(Date, nullable=False)
    demanda_estimada = Column(Integer, nullable=False)
    demanda_real = Column(Integer)
    precision = Column(Float)

    tienda = relationship("Tienda")
    producto = relationship("Producto")


class KPI(Base):
    __tablename__ = "kpis"

    id = Column(Integer, primary_key=True, index=True)
    tienda_id = Column(Integer, ForeignKey("tiendas.id"), nullable=False)
    mes = Column(Integer, nullable=False)
    anio = Column(Integer, nullable=False)
    tasa_rotura_stock = Column(Float)
    tiempo_promedio_entrega = Column(Float)
    costo_logistica = Column(Float)
    precision_pronostico = Column(Float)
    ventas_totales = Column(Float)
    numero_ordenes = Column(Integer)

    tienda = relationship("Tienda")
