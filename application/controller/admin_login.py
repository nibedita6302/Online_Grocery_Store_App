from flask import request, session, render_template, url_for, redirect
from flask import current_app as app
from application.model_users import *
from application.functions.alert import *

@app.route('/admin-login', methods=['GET','POST'])
def adminLogin(): 
	## display login page
    if request.method == 'GET':
        if 'admin' in session:			## if already logged in 
            session.pop('admin',None)	## logout automatically

        return render_template('admin/admin_login.html')
        
    ## login request
    elif request.method == 'POST':
        createAlert()
        result = request.form 						
        admin = Admin.query.filter_by(admin_id=result['admin_id']).first()
        print('admin',admin)
        if admin:							## if admin exist
            ## validation
            if result['password']=="":
                setAlert('Enter Password.','danger')
            elif admin.password == result['password']:
                ## set session for logged in admin
                session['admin'] = admin.admin_id
            else:
                setAlert('Invalid Password!','danger')
        else:
            setAlert('Invalid Admin ID!','danger')		

        if isAlert():					
            return render_template('admin/admin_login.html', alert=getAlert())	## show alert

        deleteAlert()						## if no setAlert then delete alert from session

        return redirect(url_for('adminControl', admin_id=admin.admin_id))	## logged in
