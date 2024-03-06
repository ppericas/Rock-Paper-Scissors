from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash # Generar passwords seguras.


"""
Esta clase representa a los usuarios de nuestra aplicación. Además, contiene toda la lógica para crear usuarios,
guardar las contraseñas de modo seguro o verificar los passwords.
"""
# Definición de la clase User que hereda de UserMixin proporcionado por Flask-Login
class User(UserMixin):

    # Constructor de la clase User
    def __init__(self, id, name, email, password, is_admin=False):
        # Inicialización de las propiedades del usuario
        self.id = id
        self.name = name
        self.email = email
        # Almacena la contraseña como un hash seguro utilizando Werkzeug
        self.password = generate_password_hash(password)
        self.is_admin = is_admin

    # Método para establecer la contraseña del usuario
    def set_password(self, password):
        # Actualiza la contraseña almacenando su hash seguro
        self.password = generate_password_hash(password)

    # Método para verificar la contraseña proporcionada con la contraseña almacenada
    def check_password(self, password):
        # Compara la contraseña proporcionada con el hash almacenado
        return check_password_hash(self.password, password)

    # Método especial para representar el objeto User en formato legible
    def __repr__(self):
        return '<User {}>'.format(self.email)

    

"""
La función get_user la utilizaremos provisionalmente para buscar un usuario por su email dentro de la lista users. Es decir,
la función get_user busca un usuario en la lista users por su dirección de correo electrónico y devuelve el objeto de usuario
si se encuentra, o None si no hay ninguna coincidencia.
Importante recordar que aquí no guardamos "strings", aquí tenemos usuarios (objetos) generados desde User y que por lo tanto
contienen elementos como mail o contraseña.
"""
users = []
# Función para obtener un usuario por su dirección de correo electrónico
def get_user(email):
    # Itera sobre cada usuario en la lista
    for user in users:
        # Verifica si la dirección de correo electrónico coincide
        if user.email == email:
            # Devuelve el usuario si se encuentra una coincidencia
            return user
    # Devuelve None si no se encuentra ningún usuario con el correo electrónico proporcionado
    return None