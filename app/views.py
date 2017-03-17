from flask import Flask, render_template, redirect, url_for, request
from app import app
from tinydb import TinyDB, Query
from datetime import datetime
import qrcode

db = TinyDB('db.json')


#Index.
@app.route('/')
def index():
    
    posts = [x for x in db.all()]
    posts.reverse()
       
    return render_template("index.html",posts=posts)

#Adding Data to TinyDB
@app.route('/addqr', methods=['POST'])
def add_to_db():
    
    date_i = datetime.now().strftime("%Y-%m-%d")
    time_i = datetime.now().strftime("%H:%M:%S")
    u_date =datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    
    u_inf = request.form['usr']
    d_inf = request.form['msg']
    qr_inf = u_inf+' '+d_inf 
        
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=6,
        border=2,
    )    
    
    dir_name = 'app/static/'
    save_pic = u_date+'.png'
    
    qr.add_data(qr_inf+' '+save_pic)
    qr.make_image().save(dir_name+save_pic)
    
    db.insert({'name':u_inf,'document':d_inf,'qrcodepath':save_pic,'date':date_i,
               'time':time_i})
    
    return redirect(url_for('index'))

#deleting Individual Record Based on Document name and TIME(not date) it was created
@app.route('/delete/<entry_id>/<time_id>')
def delete_entry(entry_id, time_id):
    
    document_d = Query()
    found_d = db.get(document_d.document == entry_id and document_d.time == time_id).eid
    db.remove(eids=[found_d,])
    
    return redirect(url_for('index'))



#Deleting all DB Data
@app.route('/del', methods=['POST'])
def purge_db():
    
    db.purge()
    
    return redirect(url_for('index'))