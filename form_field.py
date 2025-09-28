from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    IntegerField,
    PasswordField,
    SubmitField,
    DateField,
    validators,
    DateTimeField,
    RadioField,
    SelectField,
)
from flask_wtf.file import FileField
from wtforms.validators import DataRequired, InputRequired, Email,Optional
from datetime import date


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("password", validators=[DataRequired()])
    submit_login = SubmitField("submit_login")


class RoleForm(FlaskForm):
    name_level = StringField("name_level", validators=[DataRequired()])


class KampusForm(FlaskForm):
    name_kampus = StringField("name_kampus", validators=[DataRequired()])
    alamat_kampus = StringField("alamat_kampus", validators=[DataRequired()])


class PageForm(FlaskForm):
    name_page = StringField("name_page", validators=[DataRequired()])
    icon_page = StringField("icon_page", validators=[DataRequired()])
    url_page = StringField("url_page", validators=[DataRequired()])

class AccountForm(FlaskForm):
    nama_lengkap = StringField("nama_lengkap", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired(), Email()])
    password = PasswordField("password", validators=[DataRequired()])
    level_user = IntegerField("level_user", validators=[DataRequired()])
    kode_kampus = IntegerField("kode_kampus", validators=[DataRequired()])
    flag_active = IntegerField("flag_active", validators=[DataRequired()])


# di form_field.py
class AccountUpdate(FlaskForm):
    nama_lengkap = StringField("nama_lengkap", validators=[DataRequired()])
    password = PasswordField("password", validators=[Optional()])
    level_user = IntegerField("level_user", validators=[DataRequired()])
    kode_kampus = IntegerField("kode_kampus", validators=[DataRequired()])
    flag_active = IntegerField("flag_active", validators=[DataRequired()])


class MataPelajaranForm(FlaskForm):
    kode_kampus = IntegerField("kode_kampus", validators=[DataRequired()])
    nama_mk = StringField("nama_mk", validators=[DataRequired()])


class TaskForm(FlaskForm):
    id_matkul = IntegerField("id_matkul", validators=[DataRequired()])
    id_kampus = IntegerField("id_kampus", validators=[DataRequired()])
    label_task = StringField("label_task", validators=[DataRequired()])
    introduction = StringField("introduction", validators=[DataRequired()])

    # Video
    video_method = SelectField(
        "Metode Video",
        choices=[("file", "Upload File"), ("url", "Input URL")],
        validators=[DataRequired()],
    )
    file_video = FileField("Upload Video", validators=[Optional()])
    url_video = StringField("Video URL", validators=[Optional()])

    # Image
    image_method = SelectField(
        "Metode Image",
        choices=[("file", "Upload File"), ("url", "Input URL")],
        validators=[DataRequired()],
    )
    file_image = FileField("Upload Image", validators=[Optional()])
    url_image = StringField("Image URL", validators=[Optional()])

    # Audio
    audio_method = SelectField(
        "Metode Audio",
        choices=[("file", "Upload File"), ("url", "Input URL")],
        validators=[DataRequired()],
    )
    file_audio = FileField("Upload Audio", validators=[Optional()])
    url_audio = StringField("Audio URL", validators=[Optional()])


class TaskFormUpdate(FlaskForm):
    introduction = StringField("introduction", validators=[DataRequired()])
    # Video
    video_method = SelectField(
        "Metode Video",
        choices=[("file", "Upload File"), ("url", "Input URL")],
        validators=[DataRequired()],
    )
    file_video = FileField("Upload Video", validators=[Optional()])
    url_video = StringField("Video URL", validators=[Optional()])

    # Image
    image_method = SelectField(
        "Metode Image",
        choices=[("file", "Upload File"), ("url", "Input URL")],
        validators=[DataRequired()],
    )
    file_image = FileField("Upload Image", validators=[Optional()])
    url_image = StringField("Image URL", validators=[Optional()])

    # Audio
    audio_method = SelectField(
        "Metode Audio",
        choices=[("file", "Upload File"), ("url", "Input URL")],
        validators=[DataRequired()],
    )
    file_audio = FileField("Upload Audio", validators=[Optional()])
    url_audio = StringField("Audio URL", validators=[Optional()])
