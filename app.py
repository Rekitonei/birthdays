#import os untuk mengakses sistem database
import os

#import SQL untuk mengunakan data SQL dalam python
from cs50 import SQL
#import tools untuk website
from flask import Flask,flash, jsonify, redirect, render_template, request, session

# mengatur nama aplikasi
app = Flask(__name__)

#dipakai untuk koneksi ke database
db = SQL("sqlite:///birthdays.db")

#http://127.0.0.1:5500/
@app.route("/", methods=["GET", "POST"])
#ketika route "/" dipanggil/diakses maka fungsi index() di eksekusi
def index():
    #jika request yang dilakukan oleh pengguna adalah post, makaeksekusi kode dalam if
    if request.method == "POST":

        #Access from data / membaca data yang di isikan pada from
        name = request.form.get("name") # ambil data dari input name
        month = request.form.get("month") # ambil data dari input month
        day = request.form.get("day") # ambil data dari input day

        #insert into database, masukan data name, month dan day ke database
        db.execute("INSERT INTO birthdays (name, month, day) VALUES(?,?,?)", name, month, day)

        #go back to Homepage, balik ke http://127.0.0.1:5500/
        return redirect("/")
    else:

        # ambil seluruh data dari tabel brithdayas, simpan di variebal birtdays
        birthdays = db.execute("SELECT * FROM birthdays")
        
        # salin isi variabel birthdays ke birthdays, lalu kirim ke index.html
        return render_template("index.html", birthdays=birthdays)

# rute untuk edit data, menggunakan parameter <id>
@app.route("/edit/<id>", methods=["GET", "POST"])
def edit_data(id):
    # mencari data sesuai ID, dan render ke edit.html
    if request.method == "GET":
       bday = db.execute("SELECT * from birthdays WHERE id = ?", id)[0]
       print(bday)
       return render_template("edit.html", bday=bday)   
    elif request.method == "POST":
        # baca form untuk mengetahui editan yang di lakukan user
        bday_name = request.form.get("name") # baca nama dari form
        bday_month = request.form.get("month") # baca month dari form
        bday_day = request.form.get("day") # baca day dari form
        # query untuk eksekusi edit data
        db.execute('UPDATE birthdays set name = ?, month = ?, day = ? where id = ?', bday_name, bday_month, bday_day, id)
        # kembali ke halaman home
        return redirect("/")        
@app.route("/delete/<id>", methods=["GET"])
def delete(id):
    db.execute("delete from birthdays where id = ?", id)
    return redirect("/")        