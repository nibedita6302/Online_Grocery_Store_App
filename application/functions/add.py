from flask import session
from application.model_items import MyCart, CartProduct
from application.database import db

def addToCart(result):
    subtotal = 0 
    qty = int(result['qty'])
    p_id = int(result['product'])
    mycart = MyCart.query.get(session['cart_id'])
    prodExist = CartProduct.query.filter_by(product_id=p_id, cart_id=session['cart_id']).first()
    if prodExist:                       ## if product exist update
        # print('prodExist')
        prodExist.quantity_count += qty
    else:                               ## if product doesnot exist in cart - create
        cp = CartProduct(cart_id=session['cart_id'], product_id=p_id,quantity_count=qty)
        db.session.add(cp)
        # print('added',cp)

    for p in mycart.hasItems:           ## calculating subtotal of cart
        quantity = CartProduct.query.filter_by(product_id=p.product_id, cart_id=session['cart_id']).first().quantity_count
        subtotal += p.price*quantity
        print(p,subtotal, quantity)
    mycart.subtotal = subtotal
 
    db.session.commit()
