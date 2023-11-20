from decimal import Decimal
from datetime import date
from flask import session, render_template, url_for, redirect
from flask import current_app as app
from application.model_items import *
from application.model_users import * 
from application.functions.alert import *


@app.route('/home/<int:user_id>/payment', methods=['GET'])
def placeOrder(user_id):
    cart_id = int(session['cart_id'])
    mycart = MyCart.query.filter_by(customer_id=user_id).first()
    inCart = CartProduct.query.filter_by(cart_id=cart_id).all()

    ## create new order
    ## payement for product includeing delivery charges (50)
    if inCart!=[]:
        order = Orders(customer_id=user_id, totalOrderAmount=mycart.subtotal+Decimal(50.00), bought_date=date.today())
        db.session.add(order)
        db.session.commit()
    else: 
        createAlert()
        setAlert('Cart Empty!!', 'danger')
        return redirect(url_for('my_Cart', user_id=session['customer'], cart_id=session['cart_id']))


    order_id = Orders.query.filter_by(customer_id=user_id).order_by(Orders.order_id.desc()).first().order_id           ## get the latest order id

    mycart.subtotal = 0                 ## cart subtotal set to 0

    for p in inCart:
        product = Products.query.get(p.product_id)
        product.totalSale_count += p.quantity_count        ## update sale (count) per product

        if product.totalSale_count > product.stock_count:
            raise ValueError('Total Sale > Stock Count')

        ## cost per product for user's order only
        price = p.quantity_count * product.price
        tran = Transaction(order_id=order_id, product_id = product.product_id,  product_name=product.product_name, product_price=product.price, seller=product.seller, product_count=p.quantity_count, totalProductAmount = price)

        db.session.add(product)
        db.session.add(tran)
    
    for i in inCart:                                    ## delete all products ordered from cart
        db.session.delete(i)

    db.session.commit()

    ord = Orders.query.filter_by(order_id=order_id).first()     ## get total order amount
    total = ord.totalOrderAmount
    # print(total)    

    return render_template('customer_applications/user_payment.html', totalPrice = total)
