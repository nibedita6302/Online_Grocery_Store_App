from bcrypt import hashpw, gensalt, checkpw
from .data.models.inventory import *

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
        brand = Brands.query.filter(Brands.b_name.like(item)).all()
        for b in brand:
            p = b.products
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