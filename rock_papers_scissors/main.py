#########################################################################################################
""" 
En este nuevo apartado vamos a aprender a trabajar el login de usuarios.
"""
#########################################################################################################


from flask import Flask, render_template, request, redirect, url_for
from forms import SignupForm, PostForm

"""
Importamos la librería que hemos instalado para poder trabajar el login de usuarios
1. Importamos diferentes elementos de flask_login para poder trabajar el login de los usuarios.
2. De froms.py importamos diferentes elementos que hemos creado para la gestión de usuarios.
3. Importamos el nuevo formulario que hemos creado para el login a la plataforma.
4. Importamos la librería de python urllib.parse para asignar alias a urls.
"""
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from models import users, get_user, User
from forms import LoginForm
from urllib.parse import urlparse as url_parse
from models import db
from ppt import juego


app = Flask(__name__)
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://piedra:papel_tijeras@localhost/piedra_papel_tijeras'
db.init_app(app)

"""
· Para gestionar el login debemos crear un objeto con LogginManager
· Redirigimos al usuario a la página de login cuando intenta acceder a vistas protegidas (vistas que solo pueden acceder usuarios
  previamente registrados)
"""
login_manager = LoginManager(app)
login_manager.login_view = "login"


# Lista de diccionarios donde almacenamos los posts del blog
posts = [
    {"title": "Primer Post", "slug": "primer-post", "content": "Contenido del primer post."},
    # {"title": "Segundo Post", "slug": "segundo-post", "content": "Contenido del segundo post."},
    # Puedes agregar más posts aquí
]



###########################################################
######################## FUNCIONES ########################
###########################################################

# Función principal para trabajar el index.
@app.route("/")
def index():
    return render_template("index.html", num_posts=len(posts))


# Función donde mostramos todos los posts del blog.
@app.route('/show_post/')
def show_post():
    return render_template('post_view.html', posts=posts)


# Función para la gestión del formulario de registro al blog
"""
Modificamos la vista para ir añadiendo a los usuarios registrados a la lista users.
"""
# http://127.0.0.1:5000/signup/
@app.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = SignupForm()
    
    if form.validate_on_submit():
        nick = form.nick.data
        mail = form.mail.data
        contraseña = form.contraseña.data
        
        # Crear un nuevo usuario y guardarlo en la base de datos
        user = User(nick=nick, mail=mail, contraseña=contraseña)
        user.set_password(contraseña)  # Asumiendo que tienes un método set_password() en tu modelo User para cifrar la contraseña
        db.session.add(user)
        db.session.commit()
        
        # Iniciar sesión con el nuevo usuario
        login_user(user, remember=True)
        
        # Redireccionar al usuario dependiendo de si hay una página siguiente o no
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        else:
            next_page = url_for('signup')
        return redirect(next_page)
    
    return render_template('signup_form.html', form=form)




 
@app.route('/jugar', methods=['GET', 'POST'])
def jugar():

    mensaje = ""
    if request.method == 'POST':
        # Obtener el input del usuario del formulario
        input_usuario = request.form['input_usuario']
        # Llamar a la función juego con el input del usuario
        resultado_juego = juego(int(input_usuario))
        mensaje = resultado_juego

    # Renderizar la plantilla HTML con el mensaje
    return render_template('index.html', mensaje=mensaje)




# Función para que un usuario registrado se identifique.
"""
Creamos una función para manejar la validación de los usuarios.
"""
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Si el usuario ya está autenticado, redirige a la página principal
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    # En caso contrario, carga, muestra y valida el formulario de acceso
    form = LoginForm()
    
    # Validamos si el usuario ha presionado el botón de submit del formulario de login
    if form.validate_on_submit():
        # Consultamos el usuario en la base de datos basándonos en el correo electrónico
        user = User.query.filter_by(mail=form.mail.data).first()
        
        # Verificamos si el usuario existe y si la contraseña coincide
        if user is not None and user.check_password(form.contraseña.data):
            # Inicia sesión con el usuario utilizando Flask-Login
            login_user(user, remember=form.remember_me.data)
            
            # Redirección después de iniciar sesión según si la identificación es válida o fallida
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            else:
                next_page = url_for('login')
            return redirect(next_page)
    
    return render_template('login_form.html', form=form)

# Función para que un usuario cierre sesión
"""
Creamos una función para gestionar el cierre de sesión de los usuarios.
"""
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


"""
Función esencial para que Flask-Login pueda gestionar y cargar usuarios en las sesiones de manera adecuada.
Para que funcione correctamente es conveniente situarla al final de nuestro código main.py.
"""
@login_manager.user_loader
def load_user(nick):
    return User.query.filter_by(nick=nick).first()


# Definimos este como el script principal
if __name__ == '__main__':
    app.run(debug=True)