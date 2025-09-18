from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, Text
from datetime import datetime


db = SQLAlchemy()


class model_page(db.Model):
    __bind_key__ = "auls"  # <- wajib kalau pakai bind
    __tablename__ = "page"
    id_page = db.Column(db.Integer, primary_key=True)
    name_page = db.Column(db.String(250))
    icon_page = db.Column(db.String(250))
    url_page = db.Column(db.String(250))


class model_useraccount(db.Model):
    __bind_key__ = "auls"  # <- wajib kalau pakai bind
    __tablename__ = "useraccount"
    id_account = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), nullable=True, unique=True)  # biasanya email unik
    password = db.Column(db.String(250), nullable=True)
    level_user = db.Column(db.Integer)
    flag_active = db.Column(db.Integer)
    nama_lengkap = db.Column(db.String(250))  # tadinya int, harus string sesuai DB
    kode_kampus = db.Column(db.Integer)
    create_by = db.Column(db.DateTime, server_default=func.now())
    last_sign = db.Column(db.DateTime, server_default=func.now())


class model_level(db.Model):
    __bind_key__ = "auls"  # <- wajib kalau pakai bind
    __tablename__ = "level_user"
    id_level = db.Column(db.Integer, primary_key=True)
    name_level = db.Column(db.String(500), nullable=True)


class model_page_setting(db.Model):
    __bind_key__ = "auls"  # <- wajib kalau pakai bind
    __tablename__ = "page_setting"
    id_set_page = db.Column(db.Integer, primary_key=True)
    id_account = db.Column(db.Integer, nullable=False)
    page1 = db.Column(db.Enum("1", "2", name="page1_enum"), nullable=False)
    page2 = db.Column(db.Enum("1", "2", name="page2_enum"), nullable=False)
    page3 = db.Column(db.Enum("1", "2", name="page3_enum"), nullable=False)
    page4 = db.Column(db.Enum("1", "2", name="page4_enum"), nullable=False)
    page5 = db.Column(db.Enum("1", "2", name="page5_enum"), nullable=False)
    page6 = db.Column(db.Enum("1", "2", name="page6_enum"), nullable=False)
    page7 = db.Column(db.Enum("1", "2", name="page7_enum"), nullable=False)
    page8 = db.Column(db.Enum("1", "2", name="page8_enum"), nullable=False)
    page9 = db.Column(db.Enum("1", "2", name="page9_enum"), nullable=False)
    page10 = db.Column(db.Enum("1", "2", name="page10_enum"), nullable=False)
    page11 = db.Column(db.Enum("1", "2", name="page11_enum"), nullable=False)

class model_setting_crud(db.Model):
    __bind_key__ = "auls"  # <- wajib kalau pakai bind
    __tablename__ = "setting_crud"
    id_setting = db.Column(db.Integer, primary_key=True)
    id_account = db.Column(db.Integer, nullable=False)
    create_setting = db.Column(db.Enum("1", "2", name="create"), nullable=False)
    update_setting = db.Column(db.Enum("1", "2", name="update"), nullable=False)
    delete_setting = db.Column(db.Enum("1", "2", name="delete"), nullable=False)
    table_setting = db.Column(db.Enum("1", "2", name="table"), nullable=False)


class model_kampus(db.Model):
    __bind_key__ = "auls"  # <- wajib kalau pakai bind
    __tablename__ = "kampus"
    id_kampus = db.Column(db.Integer, primary_key=True)
    name_kampus = db.Column(db.String(500), nullable=True)
    alamat_kampus = db.Column(db.String(500), nullable=True)


class model_soal(db.Model):
    __bind_key__ = "auls"  # <- wajib kalau pakai bind
    __tablename__ = "soal"
    id_soal = db.Column(db.Integer, primary_key=True)
    id_mk = db.Column(db.Integer, nullable=False)
    id_task = db.Column(db.Integer, nullable=False)
    pertanyaan = db.Column(db.String(500), nullable=True)
    jawaban_benar = db.Column(db.String(500), nullable=True)
    A = db.Column(db.String(500), nullable=True)
    B = db.Column(db.String(500), nullable=True)
    C = db.Column(db.String(500), nullable=True)
    D = db.Column(db.String(500), nullable=True)


class model_matapel(db.Model):
    __bind_key__ = "auls"  # <- wajib kalau pakai bind
    __tablename__ = "mata_pelajaran"
    id_mk = db.Column(db.Integer, primary_key=True)
    kode_kampus = db.Column(db.Integer, nullable=False)
    nama_m = db.Column(db.String(500), nullable=True)


class model_task(db.Model):
    __bind_key__ = "auls"  # <- wajib kalau pakai bind
    __tablename__ = "task"
    id_task = db.Column(db.Integer, primary_key=True)
    id_matkul = db.Column(db.Integer, nullable=False)
    id_kampus = db.Column(db.Integer, nullable=False)
    label_task = db.Column(db.String(500), nullable=True)
    introduction = db.Column(db.String(500), nullable=True)
    video = db.Column(db.String(250), nullable=True)
    gambar = db.Column(db.String(250), nullable=True)
    audio = db.Column(db.String(250), nullable=True)


class model_finish_task(db.Model):
    __bind_key__ = "auls"  # <- wajib kalau pakai bind
    __tablename__ = "finish_task"
    id_finish = db.Column(db.Integer, primary_key=True)
    id_account = db.Column(db.Integer, nullable=False)
    id_task = db.Column(db.Integer, nullable=False)


class model_jawaban(db.Model):
    __bind_key__ = "auls"  # <- wajib kalau pakai bind
    __tablename__ = "jawaban"
    id_jawaban = db.Column(db.Integer, primary_key=True)
    id_account = db.Column(db.Integer, nullable=False)
    id_soal = db.Column(db.Integer, nullable=False)
    id_kampus = db.Column(db.Integer, nullable=False)
    jawaban = db.Column(db.String(250), nullable=True)


class model_hasilsiswa(db.Model):
    __bind_key__ = "auls"  # <- wajib kalau pakai bind
    __tablename__ = "hasil_siswa"
    id_siswa = db.Column(db.Integer, primary_key=True)
    id_account = db.Column(db.Integer, nullable=False)
    id_mk = db.Column(db.Integer, nullable=False)
    nilai = db.Column(db.String(250), nullable=True)
    grade = db.Column(db.String(250), nullable=True)
