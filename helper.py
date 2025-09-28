from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError
from model import *

# DROP DOWN SELE
import os
from werkzeug.utils import secure_filename
from flask import current_app
import re

def slugify_label(label: str) -> str:
    """
    Ubah label_task jadi aman untuk nama file:
    - Ganti spasi dengan underscore
    - Hapus karakter selain huruf, angka, underscore
    - Lowercase
    """
    # Ganti spasi dengan underscore
    text = label.strip().replace(" ", "_")

    # Hapus karakter selain alfanumerik + underscore
    text = re.sub(r"[^A-Za-z0-9_]", "", text)

    # Biar konsisten, lowercase semua
    return text.lower()


def save_file_with_label(file, folder_name, label, id_kampus, kode_matkul):
    if not file:
        return None

    # Bersihkan label dulu (jadi aman untuk filename)
    clean_label = slugify_label(label)

    # Ambil ekstensi file
    ext = os.path.splitext(file.filename)[1]

    # Format nama file
    filename = secure_filename(f"{clean_label}{ext}")

    # Buat folder bertingkat: static/videos/<id_kampus>/<kode_matkul>
    upload_folder = os.path.join(
        current_app.root_path, "static", folder_name, str(id_kampus), str(kode_matkul)
    )
    os.makedirs(upload_folder, exist_ok=True)

    # Path lengkap penyimpanan
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)

    # Path relatif untuk disimpan ke DB
    return f"{folder_name}/{id_kampus}/{kode_matkul}/{filename}"


def clear_task_folder(folder_name, id_kampus, kode_matkul):
    """
    Hapus semua file dalam folder static/<folder_name>/<id_kampus>/<kode_matkul>
    tapi tidak menghapus foldernya.
    """
    folder_path = os.path.join(
        current_app.root_path, "static", folder_name, str(id_kampus), str(kode_matkul)
    )

    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path):  # hanya file
                    os.remove(file_path)
            except Exception as e:
                print(f"❌ Gagal hapus {file_path}: {e}")
        return True
    return False


def truncate_text(text, length=50):
    """Potong teks jika lebih panjang dari batas (default 50 karakter)."""
    if text and len(text) > length:
        return text[:length] + "..."
    return text if text else "-"


def fetch_level_user_options():
    role_accounts = model_level.query.all()
    return [(role.name_level, str(role.id_level)) for role in role_accounts]

def fetch_level_user_Super(id):
    role_accounts = model_level.query.filter_by(id_level=id).all()
    return [(role.name_level, str(role.id_level)) for role in role_accounts]

def fetch_level_user_Admin():
    role_accounts = model_level.query.filter(model_level.id_level != 1).all()
    return [(role.name_level, str(role.id_level)) for role in role_accounts]

def fetch_kampus_super():
    kampus_data = model_kampus.query.all()
    return [(kampus.name_kampus, str(kampus.id_kampus)) for kampus in kampus_data]


def fetch_kampus_admin(id):
    kampus_data = model_kampus.query.filter_by(id_kampus=id).all()
    return [(kampus.name_kampus, str(kampus.id_kampus)) for kampus in kampus_data]


def fetch_matkul_super():
    matkul_data = model_matapel.query.all()
    return [(matkul.nama_mk, str(matkul.id_mk)) for matkul in matkul_data]


def fetch_matkul_admin(id):
    matkul_data = model_matapel.query.filter_by(kode_kampus=id).all()
    return [(matkul.nama_mk, str(matkul.id_mk)) for matkul in matkul_data]


def fetch_active(status: int) -> str:
    if status == 1:
        return "No Active"
    elif status == 2:
        return "Active"
    else:
        return "Status tidak diketahui"


def fetch_status_user_options():
    return [
        (1, fetch_active(1)),
        (2, fetch_active(2)),
    ]


def fetch_kampus_all(leveling: int):
    query = model_kampus.query
    if leveling != 1:
        query = query.filter(model_kampus.id_kampus != 1)

    kampusz = query.all()

    return [(str(role.id_kampus), role.name_kampus) for role in kampusz]


def fetch_kampus(id_kampus: int) -> str:
    kampus = model_kampus.query.filter(
        model_kampus.id_kampus == id_kampus, model_kampus.id_kampus != 1
    ).first()
    return kampus.name_kampus if kampus else "Unknown"


def fetch_matpel(id_kampus: int) -> str:
    kampus = model_matapel.query.filter(
        model_matapel.kode_kampus == id_kampus, model_matapel.kode_kampus != 1
    ).first()
    return kampus.name_kampus if kampus else "Unknown"


# CREATE
def create_record(model, **kwargs):
    try:
        record = model(**kwargs)
        db.session.add(record)
        db.session.commit()
        return {
            "success": True,
            "data": record.as_dict() if hasattr(record, "as_dict") else str(record),
        }
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"success": False, "error": str(e)}


# READ
def get_record_by_id(model, record_id):
    record = model.query.get(record_id)
    if record:
        return {
            "success": True,
            "data": record.as_dict() if hasattr(record, "as_dict") else str(record),
        }
    return {"success": False, "error": "Record not found"}


def get_all_records(model):
    records = model.query.all()
    return {
        "success": True,
        "data": [r.as_dict() if hasattr(r, "as_dict") else str(r) for r in records],
    }


# UPDATE
def update_record(model, record_id, **kwargs):
    record = model.query.get(record_id)
    if not record:
        return {"success": False, "error": "Record not found"}
    try:
        for key, value in kwargs.items():
            setattr(record, key, value)
        db.session.commit()
        return {
            "success": True,
            "data": record.as_dict() if hasattr(record, "as_dict") else str(record),
        }
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"success": False, "error": str(e)}


# DELETE
def delete_record(model, record_id):
    record = model.query.get(record_id)
    if not record:
        return {"success": False, "error": "Record not found"}
    try:
        db.session.delete(record)
        db.session.commit()
        return {"success": True, "message": "Record deleted"}
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"success": False, "error": str(e)}
