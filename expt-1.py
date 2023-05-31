from flask import Flask, render_template, request, redirect, session
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = client["mydatabase"]

admin_info = mydb["Admin_Info"]   # admin_info is the collection name of admin sign up data
book_data = mydb["Book_data"]   # book_data is the collection name of book data
user_info = mydb["User_Info"]   # user_info is the collection name of user sign up data
issued_book = mydb["Issued_Book"]   # issued_book is the collection name of user issued book data


app = Flask(__name__)
app.config['SECRET_KEY']= "jweghdfuyoweg78t8jksab"


########################################## Admin module
############################## Admin index
@app.route('/admin_index', methods=['GET', 'POST'])
def admin_index():

    return render_template("admin_index.html", **locals())

############################## Admin logged in
@app.route('/admin_logged_in', methods=['GET', 'POST'])
def admin_logged_in():

    return render_template("admin_logged_in.html", **locals())


############################## Admin sign up
@app.route('/admin_sign_up', methods=['GET', 'POST'])
def admin_sign_up():
    email_msg = ""
    pass_msg = ""
    if request.method == 'POST':
        admin_name = request.form["admin_name"]
        admin_email = request.form["admin_email"]
        admin_password = request.form["admin_password"]
        admin_password_2 = request.form["admin_psw-repeat"]

        if "@" not in admin_email:
            email_msg = "Email format is incorrect"
        else:
            if admin_password != admin_password_2:
                pass_msg = "Password did not match"
            else:
                admindict = {"admin_name": admin_name, "admin_email": admin_email, "admin_password": admin_password}
                admin_info.insert_one(admindict)
                return redirect('/admin_logged_in')


    return render_template("admin_sign_up.html", **locals())


############################## Admin log in
@app.route('/admin_log_in', methods=['GET', 'POST'])
def admin_log_in():
    email_msg = ""
    if request.method == 'POST':
        admin_email = request.form["admin_email"]
        admin_password = request.form["admin_password"]

        find = list(admin_info.find({"admin_email": admin_email, "admin_password": admin_password}))
        if bool(find):
            return redirect('/admin_logged_in')

    return render_template("admin_log_in.html", **locals())


##################### Admin add books
@app.route('/admin_add_books', methods=['GET', 'POST'])
def admin_add_books():
    if request.method == 'POST':
        book = request.form["book_name"]
        author = request.form["author"]
        type = request.form["book_type"]

        data_2 = {"book_name": book, "author": author, "book_type": type}
        book_data.insert_one(data_2)

    return render_template("admin_add_books.html", **locals())


##################### Admin remove book
@app.route('/admin_remove_book', methods=['GET', 'POST'])
def admin_remove_book():
    if request.method == 'POST':
        book = request.form["book_name"]
        author = request.form["author"]
        type = request.form["book_type"]

        data_2 = {"book_name": book, "author": author, "book_type": type}
        book_data.delete_one(data_2)

    return render_template("admin_remove_book.html", **locals())


########################### admin access available books
@app.route('/admin_avail_books', methods=['GET', 'POST'])
def admin_avail_books():
    list = []
    for t in book_data.find():
        list.append(t)
    return render_template("admin_avail_books.html", **locals())


########################### admin access issued books user_issue_book
@app.route('/admin_issued_book', methods=['GET', 'POST'])
def admin_issued_book():
    list_2 = []
    for s in issued_book.find():
        list_2.append(s)
    return render_template("admin_issued_book.html", **locals())



###############################    admin_user_information
@app.route('/admin_user_information', methods=['GET', 'POST'])
def admin_user_information():
    List_user_info = []
    for j in user_info.find():
        List_user_info.append(j)
    return render_template("admin_user_information.html", **locals())


########################### user will logout
@app.route('/admin_logout', methods = ['GET', 'POST'])
def admin_logout():
    session.clear()
    return redirect("/admin_index")


########################################## User module
############################## user unsigned index
@app.route('/index', methods=['GET', 'POST'])
def index():

    return render_template("index.html", **locals())


############################# user unsigned contact us
@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():

    return render_template("contact_us.html", **locals())


############################## user signed index
@app.route('/index_signed_in', methods=['GET', 'POST'])
def index_signed_in():
    if "name" in session.keys():
        name = session["name"]
    else:
        name = "unknown"
    return render_template("index_signed_in.html", **locals())


########################### USer Sign up
@app.route('/sign_up', methods=["GET", "POST"])
def sign_up():
    name_msg = ""
    email_msg = ""
    pass_msg = ""
    if request.method == 'POST':
        user_name = request.form["name"]
        user_mobile = request.form["mobile"]
        user_email = request.form["email"]
        user_city = request.form["city"]
        user_password = request.form["password"]
        user_password_2 = request.form["psw-repeat"]

        if (len(user_name))<8:
            name_msg = "Name must be 8 character"
        elif "@" not in user_email:
            email_msg = "Email format is incorrect"
        else:
            if user_password != user_password_2:
                pass_msg = "Password did not match"
            else:
                userdict = {"name": user_name, "mobile": user_mobile, "email": user_email, "city": user_city,
                            "password": user_password}
                user_info.insert_one(userdict)
                return redirect('/index_signed_in')


    return render_template("sign_up.html", **locals())

################################ USer sign in
@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        login_msg = ""
        user_email = request.form["email"]
        user_password = request.form["password"]

        find = list(user_info.find({"email": user_email, "password": user_password}))
        if bool(find):
            #session["name"] = request.form["name"]
            return redirect("/index_signed_in")
        else:
            login_msg = "Incorrect input"
            return redirect("/sign_in")

    return render_template("sign_in.html", **locals())


############################# user signed contact us
@app.route('/signed_in_contact_us', methods=['GET', 'POST'])
def signed_in_contact_us():

    return render_template("signed_in_contact_us.html", **locals())


############### user access available books and will get Issue button pressing it, user_confirm_issue will come
@app.route('/user_avail_books', methods=['GET', 'POST'])
def user_avail_books():
    list = []
    for t in book_data.find():
        list.append(t)
    return render_template("user_avail_books.html", **locals())


########################### user confirm issue books
@app.route('/user_confirm_issue', methods=['GET', 'POST'])
def user_confirm_issue():
    if request.method == 'POST':
        check_msg = ""
        book = request.form["con_book_name"]
        author = request.form["con_author"]
        type = request.form["con_book_type"]

        find = list(book_data.find({"book_name": book, "author": author, "book_type": type}))
        if bool(find):
            data_3 = {"con_book_name": book, "con_author": author, "con_book_type": type}
            issued_book.insert_one(data_3)
        else:
            check_msg = "Incorrect input"


    return render_template("user_confirm_issue.html", **locals())


########################### user access issued books user_issue_book
@app.route('/user_issued_book', methods=['GET', 'POST'])
def user_issued_book():
    list_2 = []
    for s in issued_book.find():
        list_2.append(s)
    return render_template("user_issued_book.html", **locals())


########################### user will logout
@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    session.clear()
    return redirect("/index")

if __name__ == '__main__':
    app.run()