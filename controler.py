import hashlib
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from model import db
from helper import delete_record, create_record,update_record
from werkzeug.security import generate_password_hash
from datetime import datetime
import re
import traceback
from flask import (
    Blueprint,
    jsonify,
    request,
    Flask,
    redirect,
    url_for,
    flash,
    render_template,
    current_app,
    session,
    make_response,
)

from model import db, model_useraccount, model_level,model_page,model_page_setting,model_setting_crud,model_kampus

from form_field import RoleForm, AccountUpdate, KampusForm, PageForm
from constant import Dashboard, Leveluser, Kampus, Sidebarpage

account_bp = Blueprint("account_bp", __name__, url_prefix="/account")
useraccount_bp = Blueprint("useraccount", __name__)
updateaccount = Blueprint("userupdate", __name__)


level_bp = Blueprint("level_bp", __name__, url_prefix="/level")
levelaccount_bp = Blueprint("levelaccount", __name__)
updatelevel = Blueprint("levelupdate", __name__)

kampus_bp = Blueprint("kampus_bp", __name__, url_prefix="/kampus")
kampusaccount_bp = Blueprint("kampusaccount",  __name__ )
updatekampus = Blueprint("kampusupdate", __name__)

sidebar_bp = Blueprint("sidebar_bp", __name__, url_prefix="/sidebar")
sidebaraccount_bp = Blueprint("sidebaraccount", __name__)
updatesidebar = Blueprint("sidebarupadate", __name__)

update_page = Blueprint("update_page", __name__)
update_crud = Blueprint("update_crud", __name__)


@update_crud.route("/updateCRUD", methods=["POST"])
def updateCRUD():
    user_id = request.form.get("user")  # karena name="user" di form HTML
    selected_settings = request.form.getlist(
        "settings[]"
    )  # contoh: ["create","update"]

    if not user_id:
        return jsonify({"success": False, "error": "User tidak dipilih"})

    setting = model_setting_crud.query.filter_by(id_account=user_id).first()
    if not setting:
        return jsonify({"success": False, "error": "Setting user belum ada di DB"})

    # Default semua jadi 1 (tidak aktif)
    crud_data = {
        "create_setting": "1",
        "update_setting": "1",
        "delete_setting": "1",
        "table_setting": "1",
    }

    # Checklist yang dipilih diubah jadi 2 (aktif)
    if "create" in selected_settings:
        crud_data["create_setting"] = "2"
    if "update" in selected_settings:
        crud_data["update_setting"] = "2"
    if "delete" in selected_settings:
        crud_data["delete_setting"] = "2"
    if "table" in selected_settings:
        crud_data["table_setting"] = "2"

    # Update field model sesuai crud_data
    for key, value in crud_data.items():
        setattr(setting, key, value)

    db.session.commit()

    return jsonify({"success": True, "message": "CRUD setting berhasil diperbarui"})


@update_page.route("/updatePageSetting", methods=["POST"])
def update_page_setting():
    user_id = request.form.get("user")
    selected_pages = request.form.getlist("pages[]")  # contoh: ["page1","page3"]

    if not user_id:
        return jsonify({"success": False, "error": "User tidak dipilih"})

    setting = model_page_setting.query.filter_by(id_account=user_id).first()

    if not setting:
        return jsonify({"success": False, "error": "Setting user belum ada di DB"})

    # Default semua ke "1" (tidak dipilih)
    pages_data = {f"page{i}": "1" for i in range(1, 12)}

    # Checklist yang dipilih diubah jadi "2"
    for p in selected_pages:
        if p in pages_data:
            pages_data[p] = "2"

    # Update field di model
    for key, value in pages_data.items():
        setattr(setting, key, value)

    db.session.commit()

    return jsonify({"success": True, "message": "Setting halaman berhasil diupdate"})


@sidebar_bp.route("/delete/<int:record_id>", methods=["POST"])
def delete_sidebar(record_id):
    result = delete_record(model_page, record_id)
    if result.get("success"):
        return jsonify({"status": "success", "message": result.get("message")})
    else:
        return jsonify({"status": "error", "message": result.get("error")}), 400


@sidebaraccount_bp.route("/sidebaraccount/create", methods=["POST"])
def sidebaraccount():
    try:
        # Ambil data dari form (HTML form)
        name_pageuser = request.form.get("name_page")
        icon_pageuser = request.form.get("icon_page")
        url_pageuser = request.form.get("url_page")

        # ✅ Cek apakah email sudah ada
        existing_user = model_page.query.filter_by(name_page=name_pageuser).first()
        if existing_user:
            print("❌ Name Page sudah terdaftar:", name_pageuser)
            flash("Name Website sudah terdaftar!", "warning")
            return redirect(url_for(Sidebarpage))

        # Data yang mau diinsert
        data = {
            "name_page": name_pageuser,
            "icon_page": icon_pageuser,
            "url_page": url_pageuser,
            
        }

        print("📌 DATA SEBELUM INSERT:", data)

        # Insert ke DB via helper
        result = create_record(model_page, **data)
        print("📌 RESULT INSERT:", result)

        if result["success"]:
            flash("Level berhasil dibuat!", "success")
            return redirect(url_for(Sidebarpage))
        else:
            flash(f"Gagal: {result['error']}", "danger")
            return redirect(url_for(Sidebarpage))

    except Exception as e:
        import traceback

        traceback.print_exc()  # biar error detail muncul di terminal
        flash(f"Error: {str(e)}", "danger")
        return redirect(url_for(Sidebarpage))


@updatesidebar.route(
    "/sidebarupadate/<int:id_page>", methods=["POST"], endpoint="sidebarupadate"
)
def sidebarupadate(id_page):
    try:
        form = PageForm()
        sidebardb = model_page.query.filter_by(id_page=id_page).first()

        if not sidebardb:
            return jsonify({"success": False, "error": "Page tidak ditemukan"}), 404

        if form.validate_on_submit():
            update_data = {}

            # Cek apakah name_level diganti
            if form.name_page.data != sidebardb.name_page:
                # Pastikan name_level belum dipakai level lain
                existing = model_page.query.filter_by(
                    name_page = form.name_page.data
                ).first()
                if existing:
                    return (
                        jsonify(
                            {"danger": True, "message": "Name Page sudah digunakan."}
                        ),
                        400,
                    )

                update_data["name_page"] = form.name_page.data
                update_data["icon_page"] = form.icon_page.data
                update_data["url_page"] = form.url_page.data

            # ✅ Jalankan update jika ada perubahan
            if update_data:
                result = update_record(model_page, id_page, **update_data)
                if not result.get("success"):
                    return (
                        jsonify(
                            {
                                "success": False,
                                "error": result.get("error", "Update gagal"),
                            }
                        ),
                        400,
                    )

            return (
                jsonify({"success": True, "message": "SideBar berhasil diupdate."}),
                200,
            )

        # Kalau form invalid
        print("❌ FORM ERRORS:", form.errors)
        return (
            jsonify({"success": False, "error": f"Form tidak valid: {form.errors}"}),
            400,
        )

    except Exception as e:
        print("❌ Exception di levelupdate:", str(e))
        return jsonify({"success": False, "error": str(e)}), 500

@level_bp.route("/delete/<int:record_id>", methods=["POST"])
def delete_level(record_id):
    result = delete_record(model_level, record_id)
    if result.get("success"):
        return jsonify({"status": "success", "message": result.get("message")})
    else:
        return jsonify({"status": "error", "message": result.get("error")}), 400

@levelaccount_bp.route("/levelaccount/create", methods=["POST"])
def levelaccount():
    try:
        # Ambil data dari form (HTML form)
        name_level_user = request.form.get("name_level")

        # ✅ Cek apakah email sudah ada
        existing_user = model_level.query.filter_by(name_level=name_level_user).first()
        if existing_user:
            print("❌ Name Level sudah terdaftar:", name_level_user)
            flash("Name Level sudah terdaftar!", "warning")
            return redirect(url_for(Leveluser))

        # Data yang mau diinsert
        data = {
            "name_level": name_level_user,
        }

        print("📌 DATA SEBELUM INSERT:", data)

        # Insert ke DB via helper
        result = create_record(model_level, **data)
        print("📌 RESULT INSERT:", result)

        if result["success"]:
            flash("Level berhasil dibuat!", "success")
            return redirect(url_for(Leveluser))
        else:
            flash(f"Gagal: {result['error']}", "danger")
            return redirect(url_for(Leveluser))

    except Exception as e:
        import traceback

        traceback.print_exc()  # biar error detail muncul di terminal
        flash(f"Error: {str(e)}", "danger")
        return redirect(url_for(Leveluser))

@updatelevel.route(
    "/levelupdate/<int:id_level>", methods=["POST"], endpoint="levelupdate"
)
def levelupdate(id_level):
    try:
        form = RoleForm()
        leveldb = model_level.query.filter_by(id_level=id_level).first()

        if not leveldb:
            return jsonify({"success": False, "error": "Level tidak ditemukan"}), 404

        if form.validate_on_submit():
            update_data = {}

            # Cek apakah name_level diganti
            if form.name_level.data != leveldb.name_level:
                # Pastikan name_level belum dipakai level lain
                existing = model_level.query.filter_by(
                    name_level=form.name_level.data
                ).first()
                if existing:
                    return (
                        jsonify(
                            {"danger": True, "message": "Name Level sudah digunakan."}
                        ),
                        400,
                    )
                update_data["name_level"] = form.name_level.data

            # ✅ Jalankan update jika ada perubahan
            if update_data:
                result = update_record(model_level, id_level, **update_data)
                if not result.get("success"):
                    return (
                        jsonify(
                            {
                                "success": False,
                                "error": result.get("error", "Update gagal"),
                            }
                        ),
                        400,
                    )

            return (
                jsonify({"success": True, "message": "Level berhasil diupdate."}),
                200,
            )

        # Kalau form invalid
        print("❌ FORM ERRORS:", form.errors)
        return (
            jsonify({"success": False, "error": f"Form tidak valid: {form.errors}"}),
            400,
        )

    except Exception as e:
        print("❌ Exception di levelupdate:", str(e))
        return jsonify({"success": False, "error": str(e)}), 500


@account_bp.route("/delete/<int:record_id>", methods=["POST"])
def delete_account(record_id):
    result = delete_record(model_useraccount, record_id)

    if result.get("success"):
        return jsonify({"status": "success", "message": result.get("message")})
    else:
        return jsonify({"status": "error", "message": result.get("error")}), 400


@useraccount_bp.route("/useraccount/create", methods=["POST"])
def create_useraccount():
    try:
        # Ambil data dari form (HTML form)
        name = request.form.get("nama_lengkap")
        email = request.form.get("email")
        password = request.form.get("password")
        level_user = request.form.get("level_user")
        kode_kampus = request.form.get("kode_kampus")
        flag_active = request.form.get("flag_active")

        print("📌 DEBUG FORM DATA:")
        print("name:", name)
        print("email:", email)
        print("password:", password)
        print("level_user:", level_user)
        print("kode_kampus:", kode_kampus)
        print("flag_active:", flag_active)

        # ✅ Cek apakah email sudah ada
        existing_user = model_useraccount.query.filter_by(email=email).first()
        if existing_user:
            print("❌ Email sudah terdaftar:", email)
            flash("Email sudah terdaftar!", "warning")
            return redirect(url_for(Dashboard))

        # Hash password biar aman
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        print("🔑 Hashed password:", hashed_password)

        # Data yang mau diinsert
        data = {
            "nama_lengkap": name,
            "email": email,
            "password": hashed_password,
            "level_user": int(level_user) if level_user else None,
            "kode_kampus": int(kode_kampus) if kode_kampus else None,
            "flag_active": int(flag_active) if flag_active else 1,
            "create_by": datetime.now(),  # ✅ auto isi waktu saat insert
        }

        print("📌 DATA SEBELUM INSERT:", data)

        # Insert ke DB via helper
        result = create_record(model_useraccount, **data)
        print("📌 RESULT INSERT:", result)

        if result["success"]:
            flash("User berhasil dibuat!", "success")
            return redirect(url_for(Dashboard))
        else:
            flash(f"Gagal: {result['error']}", "danger")
            return redirect(url_for(Dashboard))

    except Exception as e:

        traceback.print_exc()  # biar error detail muncul di terminal
        flash(f"Error: {str(e)}", "danger")
        return redirect(url_for(Dashboard))


@updateaccount.route(
    "/userupdate/<int:id_account>", methods=["POST"], endpoint="userupdate"
)
def userupdate(id_account):
    try:
        form = AccountUpdate()
        accountdb = model_useraccount.query.filter_by(id_account=id_account).first()

        if not accountdb:
            return jsonify({"success": False, "error": "Account tidak ditemukan"}), 404

        if form.validate_on_submit():
            update_data = {}

            # ✅ Password hanya update kalau user isi baru
            if form.password.data and form.password.data != accountdb.password:
                md5_hashed_password = hashlib.md5(
                    form.password.data.encode()
                ).hexdigest()
                update_data["password"] = md5_hashed_password

            if form.level_user.data:
                update_data["level_user"] = form.level_user.data
            if form.nama_lengkap.data:
                update_data["nama_lengkap"] = form.nama_lengkap.data
            if form.kode_kampus.data:
                update_data["kode_kampus"] = form.kode_kampus.data
            if form.flag_active.data is not None:
                update_data["flag_active"] = form.flag_active.data

            # ✅ Jalankan update
            result = update_record(model_useraccount, id_account, **update_data)

            if result["success"]:
                # 🔑 Cek apakah user update dirinya sendiri
                current_id = request.cookies.get("uniqID")  # atau session["user_id"]
                if str(id_account) == str(current_id):
                    # Hapus cookies biar otomatis logout
                    resp = make_response(
                        jsonify(
                            {
                                "success": True,
                                "message": "Account berhasil update. Silakan login ulang.",
                            }
                        )
                    )
                    resp.delete_cookie("uniqID")
                    resp.delete_cookie("levelUser")
                    return resp, 200

                return (
                    jsonify({"success": True, "message": "Account berhasil update."}),
                    200,
                )
            else:
                return jsonify({"success": False, "error": result["error"]}), 400

        # Debug kalau form error
        print("❌ FORM ERRORS:", form.errors)
        return (
            jsonify({"success": False, "error": f"Form tidak valid: {form.errors}"}),
            400,
        )

    except Exception as e:
        print("❌ Exception di userupdate:", str(e))
        return jsonify({"success": False, "error": str(e)}), 500


@kampus_bp.route("/delete/<int:record_id>", methods=["POST"])
def delete_kampus(record_id):
    try:
        kampusdb = model_kampus.query.filter_by(id_kampus=record_id).first()
        if not kampusdb:
            return (
                jsonify({"status": "error", "message": "Kampus tidak ditemukan"}),
                404,
            )

        result = delete_record(model_kampus, record_id)
        if result.get("success"):
            return jsonify(
                {
                    "status": "success",
                    "message": f"Data '{kampusdb.name_kampus}' berhasil dihapus",
                }
            )
        else:
            return jsonify({"status": "error", "message": result.get("error")}), 400

    except Exception as e:
        print("❌ ERROR delete_kampus:", str(e))
        print(traceback.format_exc())
        return jsonify({"status": "error", "message": str(e)}), 500


@kampusaccount_bp.route("/kampusaccount/create", methods=["GET", "POST"])
def createkampus():
    if request.method == "POST":
        kampus_user = request.form.get("name_kampus", "").strip()
        alamat_kampus = request.form.get("alamat_kampus", "").strip()

        if not kampus_user:
            flash("❌ Name Kampus tidak boleh kosong!", "warning")
            return redirect(url_for(Kampus))

        # ===== Cek master =====
        existing = model_kampus.query.filter_by(name_kampus=kampus_user).first()
        if existing:
            flash("❌ Kampus sudah ada!", "warning")
            return redirect(url_for(Kampus))

        # ===== Simpan master =====
        result = create_record(
            model_kampus, name_kampus=kampus_user, alamat_kampus=alamat_kampus
        )
        if not result["success"]:
            flash(f"Gagal: {result['error']}", "danger")
            return redirect(url_for(Kampus))

        return redirect(url_for(Kampus))


@updatekampus.route(
    "/kampusupdate/<int:id_kampus>", methods=["POST"], endpoint="kampusupdate"
)
def kampusupdate(id_kampus):
    try:
        form = KampusForm()
        kampusdb = model_kampus.query.filter_by(id_kampus=id_kampus).first()

        if not kampusdb:
            return jsonify({"success": False, "error": "Kampus tidak ditemukan"}), 404

        if form.validate_on_submit():
            update_data = {}
            if form.name_kampus.data:
                update_data["name_kampus"] = form.name_kampus.data
            if form.alamat_kampus.data:
                update_data["alamat_kampus"] = form.alamat_kampus.data

            result = update_record(model_kampus, id_kampus, **update_data)

            if result["success"]:
                return (
                    jsonify(
                        {"success": True, "message": "Data kampus berhasil diupdate!"}
                    ),
                    200,
                )
            else:
                return jsonify({"success": False, "error": result["error"]}), 400

        return (
            jsonify(
                {"success": False, "error": "Form tidak valid", "details": form.errors}
            ),
            400,
        )

    except Exception as e:
        print("❌ Exception di kampusupdate:", str(e))
        return jsonify({"success": False, "error": str(e)}), 500




