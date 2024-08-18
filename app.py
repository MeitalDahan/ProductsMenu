#Import libraries, to create a working framework.
#Import libraries, to create connection with sqlite db.
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import text
#Creating a database connection with flask app.
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

#Setting up creating sql queries for the site.db table with Python.
db = SQLAlchemy(app)
migrate = Migrate(app, db)
#Setting permissions for the product and price table.
class Products(db.Model):
    product_name = db.Column(db.String, unique=True, nullable=False, primary_key=True)
    price = db.Column(db.Integer, unique=True, nullable=False)

    def __str__(self):
        return f"Product name: {self.product_name}, price: {self.price}"

# flask db init
# flask db upgrade
# flask db migrate

@app.route('/')
def index():
    return render_template('add.html')

@app.route('/add_product', methods=['POST'])
def add_product():
    product_name = request.form['product_name']
    cost = request.form['cost']

    # my_prod = Products(product_name=product_name, price=cost)
    # db.session.add(my_prod)
#Creating a sql query for the products table.
    db.session.execute(text('insert into products (product_name, price) values (:product_name, :price)'), {'product_name': product_name, 'price': cost})
    db.session.commit()
#Reference to a url with a search extension.
    return redirect(url_for('search'))


@app.route('/search')
def search():
    query = request.args.get('query', '')
    results = db.session.execute(text('SELECT * FROM products WHERE product_name LIKE :query'), {'query': f'%{query}%'})

    return render_template('search.html', products=results)

if __name__ == '__main__':
    app.run(debug=True)
