from datetime import timedelta, datetime
import hashlib
from model import db
import os
from model import (
    model_useraccount,
    model_level,
    model_page_setting,
    model_page,
    model_setting_crud,
    model_kampus,
)
from flask_wtf.csrf import CSRFProtect

import json

from helper import (
    fetch_level_user_options,
    fetch_kampus_super,
    fetch_level_user_Admin,
    fetch_kampus_admin,
    fetch_level_user_Super,
    fetch_active,
    fetch_kampus,
    fetch_status_user_options,
)
from column_ajax import columns_account, columns_level
from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    make_response,
    url_for,
    session,
    get_flashed_messages,
    render_template_string,
    flash,
    abort,
)
from sqlalchemy import or_, and_


from constant import (
    title_website,
    get_icon_url,
    login_screen,
    server,
    password_server,
    user_server,
    user_server,
    db1,
    
    dashboard_screen,
    column_useraccount,
    column_role,
    ajaxaccount,
    ajaxlevel,
    insertaccountcrud,
    insertlevelcrud,
    deleteaccountcrud,
    deletelevelcrud,
    updateaccountcrud,
    updatelevelcrud,
    getajaxaccount,
    getajaxlevel,
    page2,
    page1,
)

from form_field import (
    LoginForm,
    AccountForm,
    AccountUpdate,
    RoleForm,

)
from flask import Flask, request, jsonify, make_response
from datetime import datetime, timedelta
from controler import (
    account_bp,
    useraccount_bp,
    updateaccount,
    level_bp,
    levelaccount_bp,
    updatelevel
)

app = Flask(__name__)

app.config["SQLALCHEMY_BINDS"] = {
    "auls": f"mysql+pymysql://{user_server}:{password_server}@{server}/{db1}"
}
db.init_app(app)    


app.config["WTF_CSRF_ENABLED"] = False
app.config["WTF_CSRF_TIME_LIMIT"] = 3600  # in seconds
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.secret_key = "AULSKJ"

# ROUTE CONTROLER
app.register_blueprint(account_bp)
app.register_blueprint(useraccount_bp)
app.register_blueprint(updateaccount)


app.register_blueprint(level_bp)
app.register_blueprint(levelaccount_bp)
app.register_blueprint(updatelevel)

app.secret_key = os.urandom(24)  # untuk session / keamanan


@app.route("/logout")
def logout():

    # Create a response object first

    response = make_response(redirect(url_for("index")))

    uniqid = request.cookies.get("uniqID")

    if uniqid is not None:

        # Delete the cookies

        response.delete_cookie("uniqID")

        response.delete_cookie("lvlUser")
        
        response.delete_cookie("kampusID")

        response.delete_cookie("expiration_date")

    return response


@app.before_request
def before_request():

    uniqid = request.cookies.get("uniqID")

    expiration_date_str = request.cookies.get("expiration_date")

    if uniqid and expiration_date_str:

        try:

            expiration_date = datetime.strptime(
                expiration_date_str, "%Y-%m-%d %H:%M:%S"
            )

            if expiration_date < datetime.now():

                response = make_response(redirect(url_for("index")))

                response.delete_cookie("uniqID")
                response.delete_cookie("kampusID")
                response.delete_cookie("lvlUser")

                return response

        except (TypeError, ValueError):

            response = make_response(redirect(url_for("index")))

            response.delete_cookie("uniqID")
            response.delete_cookie("kampusID")
            response.delete_cookie("lvlUser")

            return response

    elif uniqid and not expiration_date_str:

        response = make_response(redirect(url_for("index")))

        response.delete_cookie("uniqID")
        response.delete_cookie("kampusID")
        response.delete_cookie("lvlUser")

        return response


@app.route("/", methods=["GET", "POST"])
def index():

    ICON = get_icon_url()

    titlez = title_website

    uniqid = request.cookies.get("uniqID")

    if uniqid is not None:

        user = model_useraccount.query.filter(model_useraccount.id_account == uniqid).first()

        if user is not None:

            return redirect(url_for("dashboard"))

    else:
        message = None
        login_form = LoginForm()
        if request.method == "POST":

            if "submit_login" in request.form and login_form.validate_on_submit():

                user_account = login_form.email.data

                password = login_form.password.data

                md5_hash = hashlib.md5(password.encode()).hexdigest()

                user = model_useraccount.query.filter_by(email=user_account).first()

                if user is not None:

                    if user.password == md5_hash:

                        resp = make_response(redirect(url_for("dashboard")))

                        expiration_date = datetime.now() + timedelta(days=30)

                        resp.set_cookie(
                            "uniqID", str(user.id_account), expires=expiration_date
                        )

                        resp.set_cookie(
                            "lvlUser", str(user.level_user), expires=expiration_date
                        )

                        resp.set_cookie(
                            "kampusID", str(user.kode_kampus), expires=expiration_date
                        )

                        resp.set_cookie(
                            "expiration_date",
                            expiration_date.strftime("%Y-%m-%d %H:%M:%S"),
                            expires=expiration_date,
                        )

                        return resp

                    else:

                        message = "Password atau Username Salah!!"

                        flash(message, "error")

                        return redirect(url_for("index"))

                else:

                    message = "Password atau Username Salah!!"

                    flash(message, "error")

                    return redirect(url_for("index"))
                
                
                

    html_content = render_template(login_screen, title=titlez, ICONIMAGES=ICON)

    response = make_response(html_content)

    response.headers["Cache-Control"] = "no-store, must-revalidate, no-store"

    response.headers["Pragma"] = "no-cache"

    response.headers["Expires"] = "0"

    return response


@app.route("/dashboard")
def dashboard():
    leveling = request.cookies.get("lvlUser")
    uniqid = request.cookies.get("uniqID")

    if not uniqid:
        return redirect(url_for("logout"))

    if not leveling:
        return redirect(url_for("logout"))

    leveling = str(leveling)

    if leveling in ["1", "2"]:
        # redirect agar URL berubah ke /CreateAccount
        return redirect(url_for("CreateAccount"))

    elif leveling == "3":
        return redirect(url_for("Materi"))

    else:
        return jsonify({"msg": "Role tidak dikenal", "cookies": request.cookies})


@app.route("/LevelUser", methods=["GET", "POST"])
def LevelUser():
    uniqid = request.cookies.get("uniqID")
    ICON = get_icon_url()
    titlez = title_website

    if uniqid is None:
        return redirect(url_for("logout"))  # kalau cookie hilang, redirect ke login

    cardtitle = "Data Level User"

    form = RoleForm()

    count_id_sidebar = 1
    levels = model_level.query.all()
    accountid = model_useraccount.query.filter(model_useraccount.id_account == uniqid).first()
    # ambil setting page untuk user yg login
    page_setting = model_page_setting.query.filter_by(
        id_account=accountid.id_account
    ).first()
    page_check = page_setting.page2

    if int(page_check) != 2:
        return logout()
    else:
        crud = model_setting_crud.query.filter_by(
            id_account=accountid.id_account
        ).first()
        create = int(crud.create_setting)  # convert ke int karena db.Enum simpan string
        update = int(crud.update_setting)  # convert ke int karena db.Enum simpan string
        delete = int(crud.delete_setting)  # convert ke int karena db.Enum simpan string
        tabel = int(crud.table_setting)  # convert ke int karena db.Enum simpan string

        sidebar_items = []
        modified_data = []

        # data user
        for level in levels:

            modified_level = [
                count_id_sidebar,
                level.name_level,
            ]
            modified_data.append(modified_level)
            count_id_sidebar += 1

        # ambil semua page
        all_pages = model_page.query.all()

        # mapping setting ke page
        if page_setting:
            for page in all_pages:
                flag = getattr(page_setting, f"page{page.id_page}", None)
                if flag == "2":  # show
                    sidebar_items.append(
                        {
                            "name_page": page.name_page,
                            "icon_page": page.icon_page,
                            "url_page": page.url_page,
                        }
                    )
        else:
            # fallback kalau belum ada setting → tampilkan semua
            for page in all_pages:
                sidebar_items.append(
                    {
                        "name_page": page.name_page,
                        "icon_page": page.icon_page,
                        "url_page": page.url_page,
                    }
                )

        # form input
        form_input = [
            {"label": "Name", "input_type": "text", "name": "name_level"},
        ]

        form_edit = [
            {
                "label": "Name",
                "input_type": "text",
                "name": "name_level",
                "value": level.name_level,
            },
        ]

        html_content = render_template(
            dashboard_screen,
            title=titlez,
            columns=columns_level,  # kirim sebagai JSON
            ICONIMAGES=ICON,
            sidebar_items=sidebar_items,
            column_names=column_role,
            data_list=form_input,
            data_list1=form_edit,
            form=form,
            form1=form,
            insert_ui=create,
            tabel_ui=tabel,
            update_ui=update,
            delete_ui=delete,
            users=modified_data,
            cardtitle=cardtitle,
            page=page2,
            ajax_post=ajaxlevel,
            get_ajax=getajaxlevel,
            insertaccount=insertlevelcrud,
            accountedelete=deletelevelcrud,
            updateaccount=updatelevelcrud,
        )

        response = make_response(html_content)
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        return response


@app.route("/CreateAccount", methods=["GET", "POST"])
def CreateAccount():
    uniqid = request.cookies.get("uniqID")
    ICON = get_icon_url()
    titlez = title_website

    if uniqid is None:
        return redirect(url_for("logout"))  # kalau cookie hilang, redirect ke login

    leveling = request.cookies.get("levelUser")
    cardtitle = "Data User"

    form = AccountForm()
    form1 = AccountUpdate()
    if str(leveling) == "1":
        LEVEL_USER_OPTIONS = fetch_level_user_options()
        KAMPUS_USER_OTIONS = fetch_kampus_super()
        users = model_useraccount.query.all()
    else:
        id_kampus = model_useraccount.query.filter_by(id_account=uniqid).first()
        kampusID = id_kampus.kode_kampus
        LEVEL_USER_OPTIONS = fetch_level_user_Admin()
        KAMPUS_USER_OTIONS = fetch_kampus_admin(kampusID)
        users = model_useraccount.query.filter_by(kode_kampus=kampusID).all()

    STATUS_OPTIONS = [("No Active", 1), ("Active", 2)]
    count_id_sidebar = 1

    accountid = model_useraccount.query.filter(model_useraccount.id_account == uniqid).first()
    # ambil setting page untuk user yg login
    page_setting = model_page_setting.query.filter_by(
        id_account=accountid.id_account
    ).first()
    page_check = page_setting.page1

    if int(page_check) != 2:
        return logout()
    else:
        crud = model_setting_crud.query.filter_by(
            id_account=accountid.id_account
        ).first()
        create = int(crud.create_setting)  # convert ke int karena db.Enum simpan string
        update = int(crud.update_setting)  # convert ke int karena db.Enum simpan string
        delete = int(crud.delete_setting)  # convert ke int karena db.Enum simpan string
        tabel = int(crud.table_setting)  # convert ke int karena db.Enum simpan string

        sidebar_items = []
        modified_data = []

        # data user
        for user in users:
            nama_type = fetch_level_user_Super(user.level_user)
            nama_type_display = nama_type[0][0] if nama_type else "Unknown"

            active_flag = fetch_active(user.flag_active)
            active_type_display = active_flag[0][0] if active_flag else "Unknown"

            kampus_client = fetch_kampus(user.kode_kampus)
            kampus_type_display = kampus_client[0][0] if kampus_client else "Unknown"

            modified_user = [
                count_id_sidebar,
                user.nama_lengkap,
                user.email,
                "*******",
                nama_type_display,
                kampus_type_display,
                active_type_display,
                user.create_by,
                user.last_sign,
                user.id_account,
            ]
            modified_data.append(modified_user)
            count_id_sidebar += 1

        # ambil semua page
        all_pages = model_page.query.all()

        # mapping setting ke page
        if page_setting:
            for page in all_pages:
                flag = getattr(page_setting, f"page{page.id_page}", None)
                if flag == "2":  # show
                    sidebar_items.append(
                        {
                            "name_page": page.name_page,
                            "icon_page": page.icon_page,
                            "url_page": page.url_page,
                        }
                    )
        else:
            # fallback kalau belum ada setting → tampilkan semua
            for page in all_pages:
                sidebar_items.append(
                    {
                        "name_page": page.name_page,
                        "icon_page": page.icon_page,
                        "url_page": page.url_page,
                    }
                )

        # form input
        form_input = [
            {"label": "Nama Lengkap", "input_type": "text", "name": "nama_lengkap"},
            {"label": "Email", "input_type": "email", "name": "email"},
            {"label": "Password", "input_type": "password", "name": "password"},
            {
                "label": "Level User",
                "input_type": "select",
                "name": "level_user",
                "value": LEVEL_USER_OPTIONS,
                "options": LEVEL_USER_OPTIONS,
            },
            {
                "label": "Kampus",
                "input_type": "select",
                "name": "kode_kampus",
                "value": KAMPUS_USER_OTIONS,
                "options": KAMPUS_USER_OTIONS,
            },
            {
                "label": "Status",
                "input_type": "select",
                "name": "flag_active",
                "value": None,  # misalnya nanti diisi user.flag_active
                "options": STATUS_OPTIONS,
            },
        ]

        form_edit = [
            {"label": "Name", "input_type": "text", "name": "nama_lengkap", "value": user.nama_lengkap},
            {
                "label": "Password",
                "input_type": "password",
                "name": "password",
                "value": "",
            },
            {
                "label": "Level User",
                "input_type": "select",
                "name": "level_user",
                "value": str(user.level_user),
                "options": LEVEL_USER_OPTIONS,
            },
            {
                "label": "Kampus",
                "input_type": "select",
                "name": "kode_kampus",
                "value": str(user.kode_kampus),
                "options": KAMPUS_USER_OTIONS,
            },
            {
                "label": "Status",
                "input_type": "select",
                "name": "flag_active",
                "value": str(user.flag_active),
                "options": STATUS_OPTIONS,
            },
        ]

        html_content = render_template(
            dashboard_screen,
            title=titlez,
            columns=columns_account,  # kirim sebagai JSON
            ICONIMAGES=ICON,
            sidebar_items=sidebar_items,
            column_names=column_useraccount,
            LEVEL_USER_OPTIONS=LEVEL_USER_OPTIONS,
            KAMPUS_USER_OTIONS=KAMPUS_USER_OTIONS,
            data_list=form_input,
            data_list1=form_edit,
            form=form,
            form1=form1,
            insert_ui=create,
            tabel_ui=tabel,
            update_ui=update,
            delete_ui=delete,
            users=modified_data,
            leveling=leveling,
            cardtitle=cardtitle,
            page=page1,
            ajax_post=ajaxaccount,
            get_ajax=getajaxaccount,
            insertaccount=insertaccountcrud,
            accountedelete=deleteaccountcrud,
            updateaccount=updateaccountcrud,
        )

        response = make_response(html_content)
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        return response


# AJAX ROUTE {Fungsi penarikan Data}

@app.route("/ajaxLevel", methods=["POST", "GET"])
def ajaxLevel():
    try:
        if request.method == "POST":
            draw = int(request.form.get("draw", 1))
            row = int(request.form.get("start", 0))
            rowperpage = int(request.form.get("length", 10))
            searchValue = request.form.get("search[value]", "")

            totalRecords = model_level.query.count()

            if searchValue:
                query = model_level.query.filter(
                    model_level.name_level.like(f"%{searchValue}%"),
                )
                totalRecordwithFilter = query.count()
                produklist = (
                    query.order_by(model_level.id_level.desc())
                    .offset(row)
                    .limit(rowperpage)
                    .all()
                )
            else:
                totalRecordwithFilter = totalRecords
                produklist = (
                    model_level.query.order_by(model_level.id_level.desc())
                    .offset(row)
                    .limit(rowperpage)
                    .all()
                )

            data = []
            count_id_sidebar = row + 1

            for produk in produklist:

                data.append(
                    {
                        "No": count_id_sidebar,
                        "name_level": produk.name_level if produk.name_level else "-",
                        "id": produk.id_level,
                    }
                )
                count_id_sidebar += 1

            response = {
                "draw": draw,
                "iTotalRecords": totalRecords,
                "iTotalDisplayRecords": totalRecordwithFilter,
                "aaData": data,
            }
            return jsonify(response)

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)})


@app.route("/ajaxAccount", methods=["POST", "GET"])
def ajaxAccount():
    try:
        if request.method == "POST":
            draw = int(request.form.get("draw", 1))
            row = int(request.form.get("start", 0))
            rowperpage = int(request.form.get("length", 10))
            searchValue = request.form.get("search[value]", "")

            # Ambil websiteID dari cookie
            kampusID = request.cookies.get("kampusID")
            levelUser = request.cookies.get("levelUser")

            kampusID = int(kampusID) if kampusID and kampusID.isdigit() else None
            levelUser = int(levelUser) if levelUser and levelUser.isdigit() else None

            # Super Admin = id 1 (semua website), Admin biasa = filter website
            if levelUser == 1:
                base_query = model_useraccount.query
            else:
                base_query = model_useraccount.query.filter(
                    model_useraccount.kode_kampus == kampusID
                )

            # total semua record (tanpa search)
            totalRecords = base_query.count()

            # mulai query
            query = base_query
            if searchValue:
                query = query.filter(
                    or_(
                        model_useraccount.nama_lengkap.like(f"%{searchValue}%"),
                        model_useraccount.email.like(f"%{searchValue}%"),
                    )
                )

            totalRecordwithFilter = query.count()

            produklist = (
                query.order_by(model_useraccount.id_account.desc())
                .offset(row)
                .limit(rowperpage)
                .all()
            )

            data = []
            count_id_sidebar = row + 1
            for produk in produklist:
                role = model_level.query.filter_by(id_level=produk.level_user).first()
                kampus = model_kampus.query.filter_by(
                    id_kampus=produk.kode_kampus
                ).first()

                status = "Active" if produk.flag_active == 2 else "No Active"
                level_name = role.name_level if role else "-"
                kampus_name = kampus.name_kampus if kampus else "-"

                data.append(
                    {
                        "No": count_id_sidebar,
                        "nama_lengkap": (
                            produk.nama_lengkap if produk.nama_lengkap else "-"
                        ),
                        "email": produk.email,
                        "password": "*********",
                        "level_user": level_name,
                        "kode_kampus": kampus_name,
                        "status": status,
                        "create_by": str(produk.create_by) if produk.create_by else "-",
                        "last_sign": str(produk.last_sign) if produk.last_sign else "-",
                        "id": produk.id_account,
                    }
                )
                count_id_sidebar += 1

            response = {
                "draw": draw,
                "iTotalRecords": totalRecords,
                "iTotalDisplayRecords": totalRecordwithFilter,
                "aaData": data,
            }
            return jsonify(response)

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)})


# GET AJAX ROUTE {Fungsi untuk Edit Data}


@app.route("/get_level_data", methods=["GET"])
def get_level_data():
    level_id = request.args.get("id", type=int)
    if not level_id:
        return jsonify({"error": "Account ID is required"}), 400

    leveldb = db.session.get(model_level, level_id)
    if leveldb is None:
        return jsonify({"error": "Account not found"}), 404

    # ambil level dari cookies login user, bukan dari account target
    role_data = {
        "name_level": leveldb.name_level,
    }

    return jsonify(role_data)

@app.route("/get_account_data", methods=["GET"])
def get_account_data():
    account_id = request.args.get("id", type=int)
    if not account_id:
        return jsonify({"error": "Account ID is required"}), 400

    accountdb = db.session.get(model_useraccount, account_id)
    if accountdb is None:
        return jsonify({"error": "Account not found"}), 404

    # ambil level dari cookies login user, bukan dari account target
    leveling = request.cookies.get("lvlUser", type=int)

    if leveling == 1:  # Super admin
        level_option = [
            {"value": str(id_level), "label": nama_level}
            for nama_level, id_level in fetch_level_user_options()
        ]

        kampus_option = [
            {"value": str(id_kampus), "label": name_kampus}
            for name_kampus, id_kampus in fetch_kampus_super()
        ]

    elif leveling == 2:  # Admin
        level_option = [
            {"value": str(id_level), "label": nama_level}
            for nama_level, id_level in fetch_level_user_Admin()
        ]

        kampus_option = [
            {"value": str(id_kampus), "label": nama_kampus}
            for nama_kampus, id_kampus in fetch_kampus_admin(accountdb.kode_kampus)
        ]
    else:
        return jsonify({"error": "Unauthorized"}), 403

    status_option = [
        {"value": str(id_status), "label": nama_status}
        for id_status, nama_status in fetch_status_user_options()
    ]

    role_data = {
        "nama_lengkap": accountdb.nama_lengkap,
        "password": accountdb.password,
        "level_user": accountdb.level_user,
        "flag_active": accountdb.flag_active,
        "kode_kampus": accountdb.kode_kampus,
        "FlagLevel": level_option,
        "FlagActive": status_option,
        "FlagKampus": kampus_option,
    }

    return jsonify(role_data)


# --- Jalankan Flask ---
if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000, debug=True)
