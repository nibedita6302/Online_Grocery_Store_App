from bcrypt import hashpw, gensalt, checkpw
from .data.models.inventory import *
from datetime import datetime
from re import compile

def hash_password(plain_pw):
    salt = gensalt()
    return hashpw(plain_pw.encode('utf-8'),salt)

def check_password(plain_pw, hash_pw):
    return checkpw(plain_pw.encode('utf-8'),hash_pw)

def search_category(string):
    string = string.lower().strip()
    product_list = []
    for s in string.split():
        item = '%'+s+'%'
        # print(item)
        category = Category.query.filter(Category.c_name.ilike(item)).all()
        # print(category)
        for c in category:
            p = c.products
            product_list.extend(p)
    # print(product_list)
    return product_list

def search_brand(string):
    string = string.lower().strip()
    product_list = []
    for s in string.split():
        item = '%'+s+'%'
        p = Products.query.filter(Products.brand.ilike(item)).all()
        product_list.extend(p)
    return product_list

def search_product(string):
    string = string.lower().strip()
    product_list = []
    for s in string.split():
        item = '%'+s+'%'
        p = Products.query.filter(Products.p_name.ilike(item)).all()
        product_list.extend(p)
    return product_list

def parseProductFromData(form):
    newForm = {key:form[key] for key in form if form[key] not in ['', 'undefined']}
    for i in newForm:
        if i in ['p_qty','price']:
            newForm[i]=float(newForm[i])
        elif i in ['c_id','stock','cn_id', 'requester']:
            newForm[i]=int(newForm[i])
        elif i in ['expieryDate','last_update_date','req_date']:
            newForm[i] = datetime.strptime(newForm['expieryDate'],f'%Y-%m-%d')
    
    return newForm

def is_alphanum_space(str):
    pattern = compile(r'[a-zA-Z0-9 ]*$')
    return pattern.match(str) is not None


def getCategorySale():
    data = {}
    category = Category.query.all()
    for c in category:
        prod = c.products
        if prod!=[]:
            total_sales = 0
            for p in prod:
                total_sales+=(p.stock-p.stock_remaining)*p.price
        data[c.c_name]=total_sales
    return data

def getPopularProduct():
    prod = Products.query.filter(Products.stock_remaining<Products.stock)\
            .order_by(Products.stock - Products.stock_remaining).all()
    return prod
