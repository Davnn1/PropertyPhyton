import pymysql

class Database:
    def connect(self):
        return pymysql.connect(host='localhost', user='root', password='', database='property_database', charset='utf8mb4')

    def option(self):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute('SELECT * FROM property_category')
            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close() 
    def read(self, id):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            if id == None:
                cursor.execute('SELECT * FROM properties')
            else:
                cursor.execute('SELECT * FROM properties where id = %s',(id,))
            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()

    def insert(self, data):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute('INSERT INTO properties(name, address, category_id, price, description) VALUES(%s, %s, %s, %s, %s)',
                                (data['name'], data['address'], data['category_id'], data['price'], data['description'],))
            con.commit()
            return 'Data Berhasil Disimpan'
        except:
            con.rollback()
            return 'Data Gagal Disimpan'
            
    def readtransaction(self, id):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            if id == None:
                cursor.execute('SELECT * FROM transactions')
            else:
                cursor.execute('SELECT * FROM transactions where id = %s',(id,))
            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()

    def adduser(self, data):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute('INSERT INTO user(fullname, email, username, password) VALUES(%s, %s, %s, %s)',
                                (data['fullname'], data['email'], data['username'], data['password'],))
            con.commit()
            return ["Register successed!",'/login']
        except:
            con.rollback()
            return ["Username has already taken, please try another!",'/register']
        finally:
            con.close()

    def checklogin(self, data):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute('SELECT * FROM user WHERE username = %s AND password = %s', (data['username'], data['password'],))
            result = cursor.fetchall()  

            if len(result) == 0:
                return False    

            return [result[0][2], result[0][4]]
        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            con.close()

    def delete(self, id):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute('DELETE FROM properties where id = %s', (id,))
            con.commit()
            return 'Data Berhasil Dihapus'
        except:
            con.rollback()
            return 'Data Gagal Dihapus'
        finally:
            con.close()
    
    def edit(self, id, data):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute('UPDATE properties SET name = %s, address = %s, category_id = %s, price = %s, description = %s where id = %s',
                                    (data['name'],data['address'],data['category_id'],data['price'],data['description'],id,))
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()