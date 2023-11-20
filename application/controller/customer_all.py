from decimal import Decimal
from flask import request, session, render_template, url_for, redirect
from flask import current_app as app
from application.model_items import *
from application.model_users import * 
from application.functions.alert import *
from application.functions.add import addToCart

@app.route('/home/<int:user_id>', methods=['GET', 'POST'])
def homePage(user_id):
    if 'customer' not in session:           ## check customer logged in
        session.pop('customer',None)
        return redirect(url_for('customerLogin'))
    
    if request.method == 'POST':  
        result = request.form

        if result['type'] == 'add':         ## if 'POST' request to 'add' product to cart
            addToCart(result)

    ## for both 'GET' and 'POST'
    categories = Category.query.all()
    return render_template('customer_applications/user_home.html', categories=categories)


@app.route('/home/<int:user_id>/cart/<int:cart_id>', methods=['GET'])
def my_Cart(user_id, cart_id): 
    mycart = MyCart.query.get(cart_id)
    shoppingList = mycart.hasItems
    # print('shoppingList',shoppingList)

    p_count = []                ## quantity for every product in cart
    for p in shoppingList:
        count = CartProduct.query.filter_by(cart_id=cart_id, product_id=p.product_id).first().quantity_count
        if (p.stock_count-p.totalSale_count) < count:
            print((p.stock_count-p.totalSale_count),count)
            createAlert()
            setAlert('Some product are out of stock!', 'danger')
        p_count.append(count)

    # print(p_count)
    if isAlert(): 
        temp = getAlert()
        deleteAlert()
        return render_template('customer_applications/user_mycart.html', shoppingList = shoppingList, p_count=p_count, subtotal=mycart.subtotal, alert=temp)
    
    return render_template('customer_applications/user_mycart.html', shoppingList = shoppingList, p_count=p_count, subtotal=mycart.subtotal)


@app.route('/home/<int:user_id>/cart/<int:cart_id>', methods=['POST'])
def my_Cart_post(user_id, cart_id): 
    result = request.form
    ## adding products from search page
    if result['method'] == 'post':          ## if 'POST' request -> new product in cart
        # print('incart')
        addToCart(result)

    elif result['method'] == 'put':          ## if 'PUT' request -> update cart 
        qty = int(result['qty'])
        p_id = int(result['product'])
        mycart = MyCart.query.filter_by(customer_id=user_id).first()
        prodExist = CartProduct.query.filter_by(product_id=p_id, cart_id=mycart.cart_id).first()
        
        prodExist.quantity_count = qty      ## set updated quantity for product

        subtotal = 0                        ## calculate new subtotal
        for p in mycart.hasItems:
            # print(p)
            if p.product_id == p_id:        ## new product quantity
                # print('in')
                subtotal += p.price*qty
            else:                           ## rest product
                quantity = CartProduct.query.filter_by(product_id=p.product_id, cart_id=cart_id).first().quantity_count
                subtotal += p.price*quantity
            # print('subtotal',subtotal)
        
        mycart.subtotal = subtotal
        db.session.commit()
    
    elif result['method'] == 'delete':          ## if 'POST' request from delete cart products 
        p_id = int(result['product'])
        price = Decimal(result['price'])
        mycart = MyCart.query.filter_by(customer_id=user_id).first()
        prodExist = CartProduct.query.filter_by(product_id=p_id, cart_id=mycart.cart_id).first()

        mycart.subtotal -= price            ## remove price from subtotal

        db.session.delete(prodExist)
        db.session.commit()

    return redirect(url_for('my_Cart', user_id=user_id, cart_id=cart_id))


@app.route('/my-profile/<int:user_id>', methods=['GET', 'POST'])
def myProfile(user_id): 
    user = Customer.query.get(user_id)

    if request.method == 'GET':
        return render_template('customer/user_profile.html', user=user)
    
    if request.method == 'POST':            ## edit profile
        result = request.form
        
        if result['type'] == 'profile':   ## if 'POST' request from profile - updates
            createAlert()	
            exist = Customer.query.filter_by(mobile_number=result['mobile']).first()
            # print(exist,user.mobile_number)
            ## validation
            if exist and exist.mobile_number != user.mobile_number:     ## if new mobile exist
                setAlert('An account with same mobile number exists! Try Logging.','danger')
            elif len(result['mobile'])!=10 or not result['mobile'].isnumeric():
                setAlert('Invalid Mobile Number','danger')
            else:
                ## validation success 
                user.first_name = result['fname']
                user.last_name = result['lname']
                user.mobile_number = result['mobile']
                user.address = result['address']

                db.session.commit()
                setAlert('Succesfully changed profile information!','success')

            return render_template('customer/user_profile.html', alert=getAlert(), user=user)	
 
@app.route('/home/<int:user_id>/my-orders', methods=['GET']) 
def myOrders(user_id):
    bought = []
    orders = Orders.query.filter_by(customer_id=user_id).order_by(Orders.order_id.desc()).all()
    # print(orders)
    for o in orders:
        tran = Transaction.query.filter_by(order_id=o.order_id).all()
        bought.append((o,tran)) 

    return render_template('customer_applications/user_orders.html', bought=bought)
