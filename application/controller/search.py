from flask import request, render_template, redirect, url_for
from flask import current_app as app
from application.model_items import Products, Category
from application.functions.alert import *
from application.database import db 

@app.route('/searchBar/<string:user>', methods=['GET','POST'])
def searchBar(user, type=None):
    if request.method == 'GET':
        if user == 'customer':
            return redirect(url_for('homePage', user_id=session['customer']))
        else:
            return redirect(url_for('adminControl'))
         
    result = request.form
    productSet= [] 
    categorySet = []
    ## searching products
    for item in result['searchItems'].split():
        item = '%'+item.lower()+'%'
        # print(item)
        c = Category.query.filter(Category.category_name.like(item)).all()
        p = Products.query.filter(Products.product_name.like(item)).all()
        s = Products.query.filter(Products.seller.like(item)).all()
        if user == 'customer':
            productSet += (p+s)
            for c_ in c:
                productSet += c_.hasProducts  
        else:
            productSet += (p+s)
            categorySet += c

    productSet = list(set(productSet))          ## set of all searched products
    # print(productSet, categorySet, c)
    
    ## remain in search page 
    ## set of searched products sent to html
    if user == 'customer':
        return render_template('customer_applications/user_search.html', pSet=productSet) 
    else:
        return render_template('admin_applications/admin_search.html', pSet=productSet, cSet=categorySet) 

    