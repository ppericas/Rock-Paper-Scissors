from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash # Generar passwords seguras.
from flask_sqlalchemy import SQLAlchemy

"""
Esta clase representa a los usuarios de nuestra aplicación. Además, contiene toda la lógica para crear usuarios,
guardar las contraseñas de modo seguro o verificar los passwords.
"""
db = SQLAlchemy()

# Definición de la clase User que hereda de UserMixin proporcionado por Flask-Login
class User(UserMixin, db.Model):
    __tablename__ = 'usuarios'

    nick = db.Column(db.String(30), primary_key=True)
    mail = db.Column(db.String(50))
    contraseña = db.Column(db.String(128))

    def __init__(self, nick, mail, contraseña):
        self.nick = nick
        self.mail = mail
        self.contraseña = contraseña

    def set_password(self, password):
        self.contraseña = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.contraseña, password)

    def __repr__(self):
        return '<User {}>'.format(self.nick)
    
    def get_id(self):
        return self.nick

    

"""
La función get_user la utilizaremos provisionalmente para buscar un usuario por su email dentro de la lista users. Es decir,
la función get_user busca un usuario en la lista users por su dirección de correo electrónico y devuelve el objeto de usuario
si se encuentra, o None si no hay ninguna coincidencia.
Importante recordar que aquí no guardamos "strings", aquí tenemos usuarios (objetos) generados desde User y que por lo tanto
contienen elementos como mail o contraseña.
"""
users = []
# Función para obtener un usuario por su dirección de correo electrónico
def get_user(mail):
    # Consulta el usuario en la base de datos basándose en el correo electrónico
    return User.query.filter_by(mail=mail).first()