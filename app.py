import sqlite3
import uuid
from flask import Flask, render_template, request, url_for, flash, redirect, abort, session


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_products(query=None):
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    if query:
        products = [product for product in products if query.lower()
                    in product['name'].lower()]
    conn.close()
    return products


def get_product(product_id):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?',
                           (product_id,)).fetchone()
    conn.close()
    if product is None:
        abort(404)
    return product


def add_to_cart(product_id, quantity):
    conn = get_db_connection()
    product = get_product(product_id)
    name = product["name"]
    image = product["image"]
    price = product["price"]
    subTotal = quantity * price
    conn.cursor().execute("INSERT INTO cart (id, quantity, name, image, price, subTotal) VALUES ( ?, ?, ?, ?, ?, ?)",
                          (product_id, quantity, name, image, price, subTotal))
    conn.commit()
    conn.cursor().close()
    conn.close()


def delete_from_cart(product_id):
    conn = get_db_connection()
    conn.cursor().execute("DELETE FROM cart WHERE id = ?", (product_id,))
    conn.commit()
    conn.cursor().close()
    conn.close()


def get_cart():
    conn = get_db_connection()
    cart = conn.execute(
        "SELECT id, name, image, SUM(quantity), price, SUM(subTotal) FROM cart GROUP BY name").fetchall()
    conn.close()
    return cart


def clear_cart():
    conn = get_db_connection()
    conn.cursor().execute("DELETE FROM cart")
    conn.commit()
    conn.cursor().close()
    conn.close()


def create_order():
    conn = get_db_connection()
    cart = conn.execute("SELECT * FROM cart").fetchall()
    if (len(cart) > 0):
        order_id = str(uuid.uuid4())
        conn.cursor().execute("INSERT INTO orders (order_id, status, totalItems) VALUES( ?, ?, ?)",
                              (order_id, "Confirmed", len(cart)))
        for item in cart:
            conn.execute("INSERT INTO order_details (order_id, product_id, quantity, price) VALUES( ?, ?, ?, ?)",
                         (order_id, item["id"], item["quantity"], item["price"]))


app = Flask(__name__)


@app.route('/')
def products():
    products = get_products()
    productsLen = len(products)
    shoppingCart = []
    cartLen = len(shoppingCart)
    totItems, total, display = 0, 0, 0
    return render_template('index.html', products=products, shoppingCart=shoppingCart, productsLen=productsLen, cartLen=cartLen, total=total, totItems=totItems, display=display)


@app.route('/search')
def search():
    query = request.args.get('q')
    products = get_products(query)
    productsLen = len(products)
    shoppingCart = []
    cartLen = len(shoppingCart)
    totItems, total, display = 0, 0, 0
    return render_template('index.html', products=products, shoppingCart=shoppingCart, productsLen=productsLen, cartLen=cartLen, total=total, totItems=totItems, display=display)


@app.route('/about')
def about_us():
    return render_template('about.html')


@app.route('/<int:id>/')
def product(id):
    product = get_product(id)
    return render_template('product.html', product=product)


@app.route("/buy/")
def buy():
    shoppingCart = []
    cartLen = len(shoppingCart)
    totItems, total, display = 0, 0, 0
    qty = int(request.args.get('quantity'))
    id = int(request.args.get('id'))
    add_to_cart(id, qty)
    shoppingCart = get_cart()
    cartLen = len(shoppingCart)
    for i in range(cartLen):
        total += shoppingCart[i]["SUM(subTotal)"]
        totItems += shoppingCart[i]["SUM(quantity)"]
    products = get_products()
    productsLen = len(products)
    return render_template("index.html", products=products, shoppingCart=shoppingCart, productsLen=productsLen, cartLen=cartLen, total=total, totItems=totItems, display=display)


@app.route("/update/")
def update():
    shoppingCart = []
    cartLen = len(shoppingCart)
    totItems, total, display = 0, 0, 0
    qty = int(request.args.get('quantity'))
    id = int(request.args.get('id'))
    delete_from_cart(id)
    add_to_cart(id, qty)
    shoppingCart = get_cart()
    cartLen = len(shoppingCart)
    for i in range(cartLen):
        total += shoppingCart[i]["SUM(subTotal)"]
        totItems += shoppingCart[i]["SUM(quantity)"]
    return render_template("cart.html", shoppingCart=shoppingCart, cartLen=cartLen, total=total, totItems=totItems, display=display)


@app.route("/checkout/")
def checkout():
    create_order()
    clear_cart()
    return redirect('/confirm-order')


@app.route("/confirm-order", methods=['GET', 'POST'])
def confirm():
    if request.method == 'POST':
        print("Request Form Data:", request.form)
        orderConfirmed = True
        email = request.form.get('email')
        name = request.form.get('name')
        phone = request.form.get('phone')
        orderDetails = {'email': email, 'name': name, 'phone': phone}
        return render_template("order.html", orderConfirmed=orderConfirmed, orderDetails=orderDetails)
    else:
        return render_template("order.html")


@app.route("/remove/", methods=["GET"])
def remove():
    conn = get_db_connection()
    out = int(request.args.get("id"))
    delete_from_cart(out)
    totItems, total, display = 0, 0, 0
    shoppingCart = get_cart()
    cartLen = len(shoppingCart)
    for i in range(cartLen):
        total += shoppingCart[i]["SUM(subTotal)"]
        totItems += shoppingCart[i]["SUM(quantity)"]
    display = 1
    return render_template("cart.html", shoppingCart=shoppingCart, cartLen=cartLen, total=total, totItems=totItems, display=display)


@app.route("/cart/")
def cart():
    totItems, total, display = 0, 0, 0
    cart = get_cart()
    cartLen = len(cart)
    for i in range(cartLen):
        total += cart[i]["SUM(subTotal)"]
        totItems += cart[i]["SUM(quantity)"]
    return render_template("cart.html", shoppingCart=cart, cartLen=cartLen, total=total, totItems=totItems, display=display)
