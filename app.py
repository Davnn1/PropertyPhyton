from flask import Flask, render_template, request, flash, redirect, session
from model import Database
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = '@#$123456&*()'
folder_upload = app.config['UPLOAD_FOLDER'] = os.path.realpath('.')+'\\static\\uploads\\'
app.config['MAX_CONTENT_LENGTH'] = 5 *1024*1024 

db = Database()

@app.route('/')
def index():
  return render_template('index.html', homeActive=True)

@app.route('/about')
def about():
  return render_template('/pages/about-us.html', aboutActive=True)


@app.route('/contact')
def contact():
  return render_template('/pages/contacts.html', contactActive=True)

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    temp = db.checklogin(request.form)
    if not temp:
      flash('Username or Password are wrong')
      return redirect('/login')
    session['username'] = temp[0]
    session['role'] = temp[1]
    return redirect('/')
  return render_template('/pages/login.html', loginActive=True)


@app.route('/logout')
def logout():
  session.pop('username', None)
  return redirect('/')

@app.route('/register', methods =['GET', 'POST'])
def register():
  if request.method == 'POST':
    if request.form['password'] == request.form['confirm']:
        temp = db.adduser(request.form)                 
        flash(temp[0])
        return redirect(temp[1])
    else:
      flash('Password does not match')
      return redirect('/register')
  return render_template('/pages/register.html', registerActive=True)

@app.route('/insert', methods=['GET', 'POST'])
def insert():
    data = db.option()
    if request.method == 'POST':
        files = request.files.getlist('files')
        property_data = {
            'name': request.form['name'],
            'address': request.form['address'],
            'category_id': request.form['category_id'],
            'price': request.form['price'],
            'description': request.form['description']
        }
        
        try:
            result = db.insert(property_data)
            if isinstance(result, list):
                inserted_id = result[1]
                # Insert data gambar untuk setiap file yang diunggah
                for file in files:
                    filename = secure_filename(file.filename)
                    directory = folder_upload+filename
                    file.save(directory)
                    db.insertImage(inserted_id, filename)

                flash('Data Berhasil Disimpan')
                return redirect('/manage')
            flash(result)
            return redirect('/insert')
        except:
            flash('Data Tidak Bisa Diupload')
            return redirect('/insert')

    return render_template('/pages/insert.html', insertActive=True, data=data)


@app.route('/property')
def property():
  data = db.read(None)
  return render_template('/pages/property.html', propertyActive=True, data=data)

@app.route('/transaction')
def transaction():
  data = db.readtransaction(None)
  return render_template('/pages/transaction.html', propertyActive=True, data=data)

# admin
@app.route('/manage')
def manage():
  data = db.read(None)
  return render_template('/pages/manage.html',data=data)

@app.route('/manageuser')
def manageuser():
  data = db.readusers(None)
  return render_template('/pages/Datauser.html',data=data)

@app.route('/deleteuser/<int:id>')
def delete_user(id):
    
    success = db.delete_user_by_id(id)
    
    if success:
        return redirect('/manageuser')
    else:
        return "Failed to delete user"

@app.route('/edituser/<int:id>')
def edituser(id):
    session['id'] = id
    return redirect('/updateuser')

@app.route('/updateuser', methods=['GET', 'POST'])
def updateuser():
    id = session.get('id')
    data = db.read_user_by_id(id)

    if request.method == 'POST':
        if db.update_user_by_id(id, request.form):
            flash('Data Berhasil Diubah')
            session.pop('id', None)
            return redirect('/manageuser')
        else:
            flash('Data Gagal Diupdate')
            return redirect('/manageuser')

    return render_template('/pages/updateuser.html', data=data[0] if data else None)


@app.route('/delete/<int:id>')
def hapus(id):
    if db.delete(id):
        listImage = db.getAllImage(id)
        if isinstance(listImage, list):
            for image in listImage:
               directory = folder_upload+image
               os.remove(directory)
        db.deleteAllImage(id)
        flash('Data Berhasil Dihapus')
    else:
        flash('Data Gagal Dihapus')
       
    return redirect('/manage')

@app.route('/buy/<int:id>')
def buy(id):
    username = session['username']
    price = db.getPrice(id)
    flash(db.addTransaction(username, price, id))
    return redirect('/property')

@app.route('/update/<int:id>')
def edit(id):
  session['id'] = id
  return redirect('/update')

@app.route('/update', methods=['GET','POST'])
def update():
  id = session['id']
  data = db.read(id)
  option = db.option()
  if request.method == 'POST':
        files = request.files.getlist('files')
        property_data = {
            'name': request.form['name'],
            'address': request.form['address'],
            'category_id': request.form['category_id'],
            'price': request.form['price'],
            'description': request.form['description']
        }
        if db.edit(id, property_data):
            listImage = db.getAllImage(id)
            if isinstance(listImage, list):
                for image in listImage:
                   directory = folder_upload+image
                   os.remove(directory)
            db.deleteAllImage(id)

            for file in files:
                filename = secure_filename(file.filename)
                directory = folder_upload+filename
                file.save(directory)
                db.insertImage(id, filename)
                
            flash('Data Berhasil Diubah')
            session.pop('id', None)
            return redirect('/manage')
        else:
            flash('Data Gagal Diupdate')
            return redirect('/manage')
  return render_template('/pages/update.html', data=data, option=option)

if __name__ == '__main__':
    app.run(debug = True)
