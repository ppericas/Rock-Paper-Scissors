"""
En este script definiremos las diferentes clases que definirán nuestros formularios.

Aunque a simple vista parezca que deberiamos emplear funciones, flask-wtf nos obliga a emplear clases. Los motivos serían:
1. Orientación a Objetos: Las clases encapsulan lógica y datos relacionados con formularios, siguiendo un enfoque orientado a objetos.
2. Reutilización: Las clases de formularios permiten crear instancias reutilizables para diferentes partes de la aplicación.
3. Extensibilidad: Facilita la extensión y modificación de formularios al heredar y modificar clases existentes.
"""


# Importaciones necesarias desde Flask-WTF y WTForms
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

"""En el nuevo formulario de login trabajaremos con booleamos"""
from wtforms import BooleanField

# Definición de la clase para el formulario de registro
class SignupForm(FlaskForm):
    # Campos del formulario con etiquetas y validadores
    nick = StringField('nick', validators=[DataRequired(), Length(max=64)])
    contraseña = PasswordField('contraseña', validators=[DataRequired()])
    mail = StringField('mail', validators=[DataRequired(), Email()])
    submit = SubmitField('Registrar')  # Botón de envío del formulario

# Definición de la clase para el formulario de publicación
class PostForm(FlaskForm):
    # Campos del formulario con etiquetas y validadores
    title = StringField('Título', validators=[DataRequired(), Length(max=128)])
    title_slug = StringField('Título slug', validators=[Length(max=128)])
    content = TextAreaField('Contenido')  # Campo para contenido extenso
    submit = SubmitField('Enviar')  # Botón de envío del formulario

# Definición de la clase para el formulario de login
class LoginForm(FlaskForm):
    mail = StringField('mail', validators=[DataRequired()])
    contraseña = PasswordField('contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Login')