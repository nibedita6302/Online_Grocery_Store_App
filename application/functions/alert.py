from flask import session

def createAlert():              ## create session to store alert msg
    session['alert'] = {'msg':None,'msg_type':None}

def setAlert(msg,msg_type):     ## set alert messgae and type
    session['alert']['msg'] = msg
    session['alert']['msg_type'] = msg_type

def getAlert():                 ## return alert from session
    return session['alert']

def deleteAlert():              ## remove alert from session
    session.pop('alert',None)

def isAlert():                  ## check if alert exist
    if 'alert' in session and not(session['alert']['msg'] is None):
        return True
    return False