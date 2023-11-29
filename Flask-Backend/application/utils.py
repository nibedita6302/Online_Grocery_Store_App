from bcrypt import hashpw, gensalt, checkpw
from .data.models.inventory import *
from datetime import datetime

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
        print(item)
        category = Category.query.filter(Category.c_name.like(item)).all()
        print(category)
        for c in category:
            p = c.products
            product_list.extend(p)
    print(product_list)
    return product_list

def search_brand(string):
    string = string.lower().strip()
    product_list = []
    for s in string.split():
        item = '%'+s+'%'
        p = Products.query.filter(Products.brand.like(item)).all()
        product_list.extend(p)
    return product_list

def search_product(string):
    string = string.lower().strip()
    product_list = []
    for s in string.split():
        item = '%'+s+'%'
        p = Products.query.filter(Products.p_name.like(item)).all()
        product_list.extend(p)
    return product_list

def parseProductFromData(form):
    for i in form:
        if i in ['p_qty','price']:
            form[i]=float(form[i])
        elif i in ['c_id','stock']:
            form[i]=int(form[i])
        elif i=='expieryDate':
            form[i] = datetime.strptime(form['expieryDate'],f'%Y-%m-%d')
    return form
