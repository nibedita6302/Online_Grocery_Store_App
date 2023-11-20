import os
import matplotlib.pyplot as plt
from flask import request, session, render_template, url_for, redirect
from flask import current_app as app
from application.model_items import *
from application.model_users import * 
from application.functions.alert import *

@app.route('/admin/control-page/<int:admin_id>', methods=['GET', 'POST'])
def adminControl(admin_id):
    if 'admin' not in session:           ## check admin logged in
        session.pop('admin',None)
        return redirect(url_for('adminLogin'))
    
    if request.method == 'POST': 
        result = request.form

        if result['type'] == 'add':         ## if 'POST' request to 'add' product to cart
            subtotal = 0
            qty = int(result['qty'])
            p_id = int(result['product'])
            mycart = MyCart.query.get(session['cart_id'])
            prodExist = CartProduct.query.filter_by(product_id=p_id, cart_id=session['cart_id']).first()
            if prodExist:                   ## if product in cart - update
                # print('prodExist')
                prodExist.quantity_count += qty
            else:                           ## new product in cart - create (Cart-Product relation)
                cp = CartProduct(cart_id=session['cart_id'], product_id=p_id,quantity_count=qty)
                db.session.add(cp)

            for p in mycart.hasItems:       ## calculate subtotal of cart
                quantity = CartProduct.query.filter_by(product_id=p.product_id, cart_id=session['cart_id']).first().quantity_count
                subtotal += p.price*quantity
                # print(p,subtotal, quantity)
            mycart.subtotal = subtotal

            db.session.commit()

    ## for both 'GET' and 'POST' 
    categories = Category.query.all()
    if isAlert(): 
        temp = getAlert()
        deleteAlert()
        return render_template('admin_applications/admin_control.html', categories=categories, alert=temp)
    else:    
        return render_template('admin_applications/admin_control.html', categories=categories)


@app.route('/admin/logistics', methods=['GET'])
def logistics():
    ## get category sales pie chart
    q1 = db.session.query(
        Category.category_name,
        db.func.sum(Products.totalSale_count*Products.price).label('total_sales'),
    ).join(Products, Products.category_id == Category.category_id)

    q1 = q1.filter(Category.product_count!=0)
    q1 = q1.group_by(Category.category_id)
    category = q1.all()
    # print(category)

    name = [c.category_name.title() for c in category]
    sales = [float(c.total_sales) for c in category]

    plt.pie(sales, labels=name, autopct='%1.1f%%')
    plt.axis('equal')
    plot_path=os.path.join(app.config['UPLOAD_FOLDER'],'category_sales_plot.png')
    if os.path.exists(plot_path):
        os.remove(plot_path)
    plt.savefig(plot_path)

    ## get total sale per product
    q2 = db.session.query(
        Products.product_name,
        Products.seller,
        (Products.totalSale_count*Products.price).label('total_sales'),
        Category.category_name
    ).join(Category, Products.category_id == Category.category_id)
    q2 = q2.filter(((Products.totalSale_count*Products.price))!=0)
    products = q2.order_by(db.desc('total_sales')).limit(5).all()
    # print(products)

    return render_template('admin_applications/admin_logistics.html', products=products, plot_path='category_sales_plot.png')


