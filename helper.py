from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError
from model import *

# DROP DOWN SELECT
def fetch_level_user_options():
    role_accounts = model_level.query.all()
    return [(role.name_level, str(role.id_level)) for role in role_accounts]

def fetch_level_user_Super(id):
    role_accounts = model_level.query.filter_by(id_level=id).all()
    return [(role.name_level, str(role.id_level)) for role in role_accounts]

def fetch_level_user_Admin():
    role_accounts = model_level.query.filter(model_level.id_level != 1).all()
    return [(role.name_level, str(role.id_level)) for role in role_accounts]

def fetch_website_super():
    website_data = model_website.query.all()
    return [(web.name_website, str(web.id_website)) for web in website_data]


def fetch_website_admin(id):
    website_data = model_website.query.filter_by(id_website=id).all()
    return [(web.name_website, str(web.id_website)) for web in website_data]


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


def fetch_website_all(leveling: int):
    query = model_website.query
    if leveling != 1:
        query = query.filter(model_website.id_website != 1)

    websitez = query.all()

    return [(str(role.id_website), role.name_website) for role in websitez]


def fetch_website(id_website: int) -> str:
    website = model_website.query.filter(
        model_website.id_website == id_website, model_website.id_website != 1
    ).first()
    return website.name_website if website else "Unknown"


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
