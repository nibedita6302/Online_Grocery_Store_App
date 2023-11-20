import os
from flask import request, session, render_template, url_for, redirect
from flask import current_app as app
from application.model_items import *
from application.model_users import * 
from application.functions.alert import *

@app.route('/admin/editCategory/<int:id>', methods=['GET','POST'])
def editCategory(id):
    result = request.form
    # print(id)
    if 'method' in result and result['method']=='put':  ## if method is PUT => edit
        category = Category.query.get(id)
        if 'name' in result:
            category.category_name = result['name'].lower()
            db.session.commit()
            createAlert()
            setAlert('Category Updated!', 'success')
        else:
            return render_template('admin_applications/form_category.html', id=id, category=category) 

    elif 'method' in result and result['method']=='delete':     ## if method is DELETE => delete
        category = Category.query.get(id)
        # print(category)
        if category.product_count > 0: 
            createAlert()
            setAlert('Category has some products. Please delete products first.', 'danger')
            # print('in here')
        else:                               
            db.session.delete(category)
            db.session.commit()

            createAlert()
            setAlert('Category deleted!', 'success')
    else:                                               ## POST => create
        if 'name' in result:
            category = Category(category_name=result['name'])
            db.session.add(category)
            db.session.commit()
            createAlert()
            setAlert('Category Created!', 'success')  
        else:
            return render_template('admin_applications/form_category.html', id=id)                                 
              
    return redirect(url_for('adminControl',admin_id=session['admin']))



@app.route('/admin/editProduct/<int:id>', methods=["GET","POST"])
def editProduct(id):
    result = request.form
    # print(id)
    if 'method' in result and result['method']=='put':  ## if method is PUT => edit
        product = Products.query.get(id)
        category = Category.query.all()
        if 'name' in result:
            result = request.form

            product.product_name = result['name'].lower()
            product.description = result['description']
            ## image handling
            img = request.files['product_image']
            if img.filename != "":
                img_path = result['name'].lower()+'_'+str(product.product_id)+'.jpg'
                # print(img_path)
                img.save(os.path.join(app.config['UPLOAD_FOLDER'],'products',img_path))
                # print('saved')
                ## save to database
                product.image_path = img_path

            product.category_id = result['category']
            product.price = result['price']
            product.stock_count = result['stock']       ## stock update
            product.totalSale_count = 0                 ## sales reset
            product.minAmount = result['minAmount']
            product.units = result['unit']   
            product.seller = result['seller'].lower()         

            db.session.commit()
            createAlert()
            setAlert('Product Updated!', 'success')
        else:
            return render_template('admin_applications/form_product.html', id=id, product=product, category=category) 

    elif 'method' in result and result['method']=='delete':     ## if method is DELETE => delete
        product = Products.query.get(id)    
        category = Category.query.get(product.category_id)
        category.product_count -= 1  
        ## delete image for product
        if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'],'products',product.image_path)):
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'],'products',product.image_path))                        
            db.session.delete(product)
            db.session.commit()

        createAlert()
        setAlert('Product deleted!', 'success')
    else:                                               ## POST => create
        if 'name' in result:
            result = request.form

            try:
                ## save to database
                newProduct = Products(product_name=result['name'].lower(),description = result['description'], category_id = result['category'], price = result['price'], stock_count = result['stock'], minAmount = result['minAmount'], units = result['unit'] , seller = result['seller'].lower() )       

                db.session.add(newProduct)
                db.session.commit()
            except Exception as e:
                product = Products.query.order_by(Products.product_id.desc()).first()
                db.session.delete(product)
                print(e)
                # print('product deleted!!', product)
            else:
                product = Products.query.order_by(Products.product_id.desc()).first()
                ## image handling
                img = request.files['product_image']
                if img.filename != "":
                    img_path = result['name'].lower()+'_'+str(product.product_id)+'.jpg'
                    # print(img_path)
                    img.save(os.path.join(app.config['UPLOAD_FOLDER'],'products',img_path))
                    # print('saved')
                    product.image_path=img_path

                category = Category.query.get(result['category'])
                category.product_count+=1

                db.session.add(category)
            finally: 
                db.session.commit()
    
            createAlert()
            setAlert('New Product Created!', 'success')  
        else:
            category = Category.query.all()
            return render_template('admin_applications/form_product.html', id=id, category=category)                                 
              
    return redirect(url_for('adminControl',admin_id=session['admin']))
