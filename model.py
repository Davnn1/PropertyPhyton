import pymysql
import logging


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
            if id is None:
                cursor.execute('SELECT * FROM properties')
            else:
                cursor.execute('SELECT * FROM properties WHERE id = %s', (id,))
                return cursor.fetchall()

            properties = cursor.fetchall()

            result = []
            for prop in properties:
                cursor.execute('SELECT name FROM property_galleries WHERE property_id = %s', (prop[0],))
                galleries = cursor.fetchall()
                if galleries:
                    # Mengambil gambar pertama dari setiap galeri
                    image = galleries[0][0]
                else:
                    image = None

                prop_dict = {
                    'id': prop[0],
                    'name': prop[1],
                    'address': prop[2],
                    'price': prop[4],
                    'description': prop[5],
                    'image': image
                }
                result.append(prop_dict)

            return result
        except Exception as e:
            logging.error(f"Error in read: {e}")
            return []
        finally:
            con.close()


    def insert(self, data):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute('INSERT INTO properties(name, address, category_id, price, description) VALUES(%s, %s, %s, %s, %s)',
                                (data['name'], data['address'], data['category_id'], data['price'], data['description'],))
            con.commit()
            inserted_id = cursor.lastrowid
            return ['Data Berhasil Disimpan', inserted_id]
        except:
            con.rollback()
            return 'Data Gagal Disimpan'

    def insertImage(self, id, name):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute('INSERT INTO property_galleries (property_id, name) VALUES(%s, %s)',
                                (id, name,))
            con.commit()
            return 'Data Berhasil Disimpan'
        except:
            con.rollback()
            return 'Data Gagal Disimpan'
            
    def readtransaction(self, username):
        con = self.connect()
        cursor = con.cursor()
        try:
            if username is None:
                cursor.execute('SELECT * FROM transactions')
            else:
                cursor.execute('SELECT * FROM transactions where user_name = %s', (username,))
            
            data = cursor.fetchall()
            print(f"Data from readtransaction: {data}")

            return data
        except Exception as e:
            print(f"Error in readtransaction: {e}")
            return ()
        finally:
            con.close()

    def read_transaction_by_id(self, id):
        con = self.connect()
        cursor = con.cursor()
        try:
            cursor.execute('SELECT * FROM transactions WHERE id = %s', (id,))
            data = cursor.fetchall()
            print(f"Data from read_transaction_by_id: {data}")
            return data
        except Exception as e:
            print(f"Error in read_transaction_by_id: {e}")
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
    
    def readusers(self, data):
        con = self.connect()
        cursor = con.cursor()
        try:
            cursor.execute('SELECT * FROM user')
            return cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            return ()
        finally:
            con.close()
    
       
    def delete_user_by_id(self, id):
        con = self.connect()
        cursor = con.cursor()
        try:
            cursor.execute('DELETE FROM user WHERE id = %s', (id,))
            con.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            con.rollback()
            return False
        finally:
            con.close()

    def read_user_by_id(self, id):
        con = self.connect()
        cursor = con.cursor()
        try:
            cursor.execute('SELECT * FROM user WHERE id = %s', (id,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            return ()
        finally:
            con.close()

    def update_user_by_id(self, id, data):
        con = self.connect()
        cursor = con.cursor()
        try:
            cursor.execute('UPDATE user SET fullname = %s, email = %s, username = %s, password = %s WHERE id = %s',
                        (data['fullname'], data['email'], data['username'], data['password'], id))
            con.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            con.rollback()
            return False
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

            return [result[0][3], result[0][5]]
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
            return True
        except:
            con.rollback()
            return False
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

    def getAllImage(self, id):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute('SELECT name FROM property_galleries WHERE property_id = %s', (id,))
            return [item[0] for item in cursor.fetchall()]
        except:
            return []
        finally:
            con.close()

    def deleteAllImage(self, id):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute('DELETE FROM property_galleries WHERE property_id = %s', (id,))
            con.commit()
            return 'All Image Removed'
        except:
            return 'Image Removing Failed'
        finally:
            con.close()

    def addTransaction(self, image_name, meet_date, username, property,):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute('INSERT INTO transactions(image_name, meet_date, user_name, property_id, property_name, property_address, category_id, total_price) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)',
                           (image_name, meet_date, username, property[0][0], property[0][1], property[0][2], property[0][3], property[0][4],))
            con.commit()
            return "Transaction successed!"
        except:
            con.rollback()
            return "Transaction Failed!"
        finally:
            con.close()

    def readdate(self, startdate, enddate, role, username, category):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            if role == "admin":
             if startdate == '' and enddate == '' and category == '0':
                 cursor.execute('SELECT * FROM transactions')
             elif startdate != '' and enddate == '' and category == '0':
                 cursor.execute('SELECT * FROM transactions WHERE created_at LIKE %s', ('%' + startdate + '%',))
             elif startdate == '' and enddate != '' and category == '0':
                 cursor.execute('SELECT * FROM transactions WHERE created_at LIKE %s', ('%' + enddate + '%',))
             elif startdate == '' and enddate == '' and category != '0':
                 cursor.execute('SELECT * FROM transactions WHERE category_id = %s', (category,))
             elif startdate != '' and enddate != '' and category == '0':
                 cursor.execute('SELECT * FROM transactions WHERE created_at BETWEEN %s AND %s', (startdate, enddate,))
             elif startdate == '' and enddate != '' and category != '0':
                 cursor.execute('SELECT * FROM transactions WHERE category_id = %s AND created_at LIKE %s', (category, enddate))
             elif startdate != '' and enddate == '' and category != '0':
                 cursor.execute('SELECT * FROM transactions WHERE category_id = %s AND created_at LIKE %s', (category, startdate))
             else:
                 cursor.execute('SELECT * FROM transactions WHERE created_at BETWEEN %s AND %s AND category_id = %s', (startdate, enddate, category))
            else:
             if startdate == '' and enddate == '' and category == '0':
                 cursor.execute('SELECT * FROM transactions WHERE user_name = %s', (username,))
             elif startdate != '' and enddate == '' and category == '0':
                 cursor.execute('SELECT * FROM transactions WHERE created_at LIKE %s AND user_name = %s', ('%' + startdate + '%', username,))
             elif startdate == '' and enddate != '' and category == '0':
                 cursor.execute('SELECT * FROM transactions WHERE created_at LIKE %s AND user_name = %s', ('%' + enddate + '%', username,))
             elif startdate == '' and enddate == '' and category != '0':
                 cursor.execute('SELECT * FROM transactions WHERE category_id = %s AND user_name = %s', (category, username,))
             elif startdate != '' and enddate != '' and category == '0':
                 cursor.execute('SELECT * FROM transactions WHERE created_at BETWEEN %s AND %s AND user_name = %s', (startdate, enddate, username,))
             elif startdate == '' and enddate != '' and category != '0':
                 cursor.execute('SELECT * FROM transactions WHERE category_id = %s AND created_at LIKE %s AND user_name = %s', (category, enddate, username,))
             elif startdate != '' and enddate == '' and category != '0':
                 cursor.execute('SELECT * FROM transactions WHERE category_id = %s AND created_at LIKE %s AND user_name = %s', (category, startdate, username,))
             else:
                 cursor.execute('SELECT * FROM transactions WHERE created_at BETWEEN %s AND %s AND category_id = %s AND user_name = %s', (startdate, enddate, category, username,))

            data = cursor.fetchall()
            print(f"Data from readtransaction: {data}")
            return data
        except:
            return ()
        finally:
            con.close()
            
    def update_status_transaction(self, id, new_status):
        con = self.connect()
        cursor = con.cursor()
        try:
            cursor.execute('UPDATE transactions SET status = %s WHERE id = %s', (new_status, id))
            con.commit()
            return True
        except Exception as e:
            print(f"Error in update_status_transaction: {e}")
            con.rollback()
            return False
        finally:
            con.close()
            
    def rejectStatus(self, id):
        con = self.connect()
        cursor = con.cursor()
        try:
            cursor.execute('UPDATE transactions SET status = "REJECTED" WHERE id = %s', (id))
            con.commit()
            return "Transaction Rejected"
        except Exception as e:
            print(f"Error in update_status_transaction: {e}")
            con.rollback()
            return "Transaction Reject Failed"
        finally:
            con.close()
            
    def readaccount(self, username):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            if username == None:
                cursor.execute('SELECT * FROM user')
            else:
                cursor.execute('SELECT * FROM user WHERE username = %s',(username,))
            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()
    
    