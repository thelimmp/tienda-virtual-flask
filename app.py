from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = '2'

# Ampliación de productos (10 productos)
productos = [
    {"id": 1, "nombre": "Laptop Gamer", "precio": 1299.99, "imagen": "laptop.png", "categoria": "Tecnología"},
    {"id": 2, "nombre": "Smartphone Pro", "precio": 799.99, "imagen": "telefono.png", "categoria": "Tecnología"},
    {"id": 3, "nombre": "Tablet HD", "precio": 349.99, "imagen": "tablet.png", "categoria": "Tecnología"},
    {"id": 4, "nombre": "Auriculares Inalámbricos", "precio": 149.99, "imagen": "auriculares.png", "categoria": "Audio"},
    {"id": 5, "nombre": "Smartwatch", "precio": 199.99, "imagen": "smartwatch.png", "categoria": "Tecnología"},
    {"id": 6, "nombre": "Teclado Mecánico", "precio": 89.99, "imagen": "teclado.png", "categoria": "Periféricos"},
    {"id": 7, "nombre": "Mouse Gaming", "precio": 59.99, "imagen": "mouse.png", "categoria": "Periféricos"},
    {"id": 8, "nombre": "Monitor 4K", "precio": 499.99, "imagen": "monitor.png", "categoria": "Tecnología"},
    {"id": 9, "nombre": "Altavoz Bluetooth", "precio": 129.99, "imagen": "altavoz.png", "categoria": "Audio"},
    {"id": 10, "nombre": "Cargador Rápido", "precio": 29.99, "imagen": "cargador.png", "categoria": "Accesorios"}
]

@app.route('/')
def index():
    categorias = list(set([p['categoria'] for p in productos]))
    return render_template('index.html', productos=productos, categorias=categorias)

@app.route('/categoria/<nombre_categoria>')
def filtrar_por_categoria(nombre_categoria):
    productos_filtrados = [p for p in productos if p['categoria'] == nombre_categoria]
    categorias = list(set([p['categoria'] for p in productos]))
    return render_template('index.html', productos=productos_filtrados, categorias=categorias, categoria_seleccionada=nombre_categoria)


@app.route('/agregar_al_carrito/<int:producto_id>')
@app.route('/agregar_al_carrito/<int:producto_id>')
def agregar_al_carrito(producto_id):
    if 'carrito' not in session:
        session['carrito'] = []
    
    # Buscar si el producto ya está en el carrito
    producto_en_carrito = next((item for item in session['carrito'] if item['id'] == producto_id), None)
    
    if producto_en_carrito:
        # Asegurarse que existe la propiedad cantidad
        if 'cantidad' not in producto_en_carrito:
            producto_en_carrito['cantidad'] = 0
        producto_en_carrito['cantidad'] += 1
    else:
        producto = next((p for p in productos if p['id'] == producto_id), None)
        if producto:
            producto_con_cantidad = producto.copy()
            producto_con_cantidad['cantidad'] = 1  # Inicializar cantidad
            session['carrito'].append(producto_con_cantidad)
    
    session.modified = True
    return redirect(url_for('index'))

@app.route('/actualizar_carrito', methods=['POST'])
@app.route('/actualizar_carrito', methods=['POST'])
def actualizar_carrito():
    if 'carrito' not in session:
        return jsonify({'success': False, 'error': 'Carrito no existe'})

    data = request.get_json()
    producto_id = data.get('producto_id')
    accion = data.get('accion')

    for index, item in enumerate(session['carrito']):
        if item['id'] == producto_id:
            if accion == 'incrementar':
                session['carrito'][index]['cantidad'] += 1
            elif accion == 'decrementar':
                if session['carrito'][index]['cantidad'] > 1:
                    session['carrito'][index]['cantidad'] -= 1
                else:
                    session['carrito'].pop(index)
            elif accion == 'eliminar':
                session['carrito'].pop(index)

            session.modified = True
            return jsonify({
                'success': True,
                'carrito_count': sum(item['cantidad'] for item in session['carrito']),
                'total': calcular_total()
            })

    return jsonify({'success': False, 'error': 'Producto no encontrado'})


def calcular_total():
    if 'carrito' not in session:
        return 0.0
    
    total = 0.0
    for item in session['carrito']:
        # Asegurarse que el item tiene 'precio' y 'cantidad'
        if 'precio' in item and 'cantidad' in item:
            total += item['precio'] * item['cantidad']
    return total

@app.route('/carrito')
def ver_carrito():
    carrito = session.get('carrito', [])
    total = calcular_total()
    return render_template('carrito.html', carrito=carrito, total=total)

if __name__ == '__main__':
    app.run(debug=True)