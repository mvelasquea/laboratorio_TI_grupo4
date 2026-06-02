const PRODUCTOS = [
  { id: 1, nombre: "Granola Andina", precio: 18, descripcion: "Granola natural con ingredientes andinos.", imagen: "img/granola.png" },
  { id: 2, nombre: "Chips de Camote", precio: 12, descripcion: "Snacks crujientes horneados, bajos en grasa.", imagen: "img/camote.png" },
  { id: 3, nombre: "Barra de Kiwicha", precio: 8, descripcion: "Barra energética rica en proteínas.", imagen: "img/kiwicha.png" },
  { id: 4, nombre: "Compost Orgánico", precio: 25, descripcion: "Abono natural ideal para plantas.", imagen: "img/compost.png" },
  { id: 5, nombre: "Jabón de Arcilla", precio: 15, descripcion: "Jabón artesanal con propiedades purificantes.", imagen: "img/jabon.png" },
  { id: 6, nombre: "Aceite de Maca", precio: 42, descripcion: "Aceite nutritivo ideal para piel y cabello.", imagen: "img/maca.png" },
  { id: 7, nombre: "Bolsa Reutilizable", precio: 20, descripcion: "Bolsa ecológica resistente.", imagen: "img/bolsa.png" },
  { id: 8, nombre: "Pajillas de Bambú", precio: 14, descripcion: "Alternativa reutilizable para bebidas.", imagen: "img/bambu.png" }
];

const Carrito = {
  key: "carrito_eco",
  obtener() { return JSON.parse(localStorage.getItem(this.key)) || []; },
  guardar(carrito) { localStorage.setItem(this.key, JSON.stringify(carrito)); },
  agregar(productoId, cantidad = 1) {
    let carrito = this.obtener();
    const producto = PRODUCTOS.find(p => p.id == productoId);
    if (!producto) return;
    const existe = carrito.find(item => item.id == productoId);
    if (existe) { existe.cantidad += cantidad; } 
    else { carrito.push({ id: producto.id, nombre: producto.nombre, precio: producto.precio, cantidad: cantidad }); }
    this.guardar(carrito);
    this.actualizarContador();
  },
  cambiarCantidad(productoId, cantidad) {
    let carrito = this.obtener();
    const item = carrito.find(i => i.id == productoId);
    if (!item) return;
    if (cantidad <= 0) { carrito = carrito.filter(i => i.id != productoId); } 
    else { item.cantidad = cantidad; }
    this.guardar(carrito);
    this.actualizarContador();
  },
  eliminar(productoId) {
    let carrito = this.obtener().filter(i => i.id != productoId);
    this.guardar(carrito);
    this.actualizarContador();
  },
  vaciar() { localStorage.removeItem(this.key); this.actualizarContador(); },
  totalItems() { return this.obtener().reduce((sum, i) => sum + i.cantidad, 0); },
  subtotal() { return this.obtener().reduce((sum, i) => sum + i.precio * i.cantidad, 0); },
  actualizarContador() {
    const badge = document.getElementById("cart-count");
    if (badge) {
      const total = this.totalItems();
      badge.textContent = total;
      badge.style.display = total > 0 ? "inline-block" : "none";
    }
  }
};
document.addEventListener("DOMContentLoaded", () => { Carrito.actualizarContador(); });