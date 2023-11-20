from flask import request, session, render_template, url_for, redirect
from flask import current_app as app
from application.model_users import *
from application.model_items import *
from application.functions.alert import *

@app.route('/customer-login', methods=['GET','POST'])
def customerLogin(): 
	## display login page
	if request.method == 'GET':
		if 'customer' in session:			## if already logged in 
			session.pop('customer',None)	## logout automatically

		# print('Signed In','customer' in session)
		return render_template('customer/user_login.html')
		
	## login request 
	elif request.method == 'POST':
		createAlert()
		result = request.form 						
		user = Customer.query.filter_by(mobile_number=result['mobile']).first()
		# print('user',user)
		if user:							## if user exist
			## validation
			if user.password == result['password']:
				## set session for logged in user
				session['customer'] = user.customer_id
				session['cart_id'] = MyCart.query.filter_by(customer_id=user.customer_id).first().cart_id
			else:
				setAlert('Invalid Password! Don\'t remember your password? Click Forgot Password.','danger')
		else:
			setAlert('Mobile number Not Registered! Don\'t have an account? Sign Up Now!','danger')		
		
		if isAlert():					
			return render_template('customer/user_login.html', alert=getAlert())	## show alert
		
		deleteAlert()						## if no setAlert then delete alert from session

		return redirect(url_for('homePage', user_id=int(user.customer_id)))	## logged in

@app.route('/forgot-password', methods=['GET','POST'])
def changePassword():
	## display page
	if request.method == 'GET':
		return render_template('customer/user_forgot_password.html')
	
	if request.method == 'POST':
		createAlert()
		result = request.form
		user = Customer.query.filter_by(mobile_number=result['mobile']).first()
		if user:
			## validation
			if result['NewPaswrd']==result['ConfirmPaswrd']:
				session['customer'] = user.customer_id
				user.password = result['NewPaswrd']
				db.session.commit()
			else:
				setAlert('Confirm Password doesnot match.','danger')
				return render_template('customer/user_forgot_password.html', alert=getAlert())
		else:
			setAlert('Mobile number Not Registered! Don\'t have an account? Sign Up Now!','danger')
			return render_template('customer/user_forgot_password.html', alert=getAlert())
		
		setAlert('New Password Saved! Sign In Again','success')	##success
		if 'customer' in session:			## customer logged out
			session.pop('customer',None)

		return render_template('customer/user_forgot_password.html', alert=getAlert())

	
@app.route('/customer-signup', methods=['GET','POST'])
def customerSignup():
	if request.method == 'GET':
		if 'customer' in session:
			session.pop('customer',None)		## logout current user
		# print('Signed In','customer' in session)
		return render_template('customer/user_signup.html')

	elif request.method == 'POST':
		createAlert()	
		result = request.form
		exist = Customer.query.filter_by(mobile_number=result['mobile']).first()
		## validation
		if exist: 			## mobile number should be unique
			setAlert('An account with same mobile number exists! Try Logging.','danger')
		elif len(result['mobile'])!=10 or not result['mobile'].isnumeric():
			setAlert('Invalid Mobile Number','danger')
		elif result['password']!=result['confirm_password'] :
			setAlert('Confirm password not matched.','danger')
		else:				## validation success
			## create new customer
			user = Customer(first_name=result['fname'],last_name=result['lname'], mobile_number=result['mobile'],address=result['address'], password=result['password'])
			db.session.add(user)
			db.session.commit()
			try:
				## create new cart form customer
				user = Customer.query.filter_by(mobile_number=result['mobile']).first()
				# print(user.customer_id)
				cart = MyCart(customer_id=user.customer_id)
				db.session.add(cart)
				setAlert('Succesfully Registered!','success')
			except Exception as e:
				print(e)
				db.session.rollback()
				db.session.delete(user)
				setAlert('Unknown Error! Try again.', 'danger')
			finally:
				db.session.commit()

		return render_template('customer/user_signup.html', alert=getAlert())	## show alert
	
	


