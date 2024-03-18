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
        nick = form.name.data
        mail = form.email.data
        contraseña = form.password.data
        
        # Crear un nuevo usuario y guardarlo en la base de datos
        user = User(nick, mail, contraseña)
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


# Función para crear nuevas entradas del blog mediante un formulario.
# http://127.0.0.1:5000/admin/post/
@app.route("/admin/post/", methods=['GET', 'POST'])
@login_required # Solo podrán acceder los usuarios logeados
def post_form():
    # Cargamos el formulario de forms.py para poder emplearlo
    form = PostForm()
    # Validamos si el usuario a presionado el botón de submit del formulario
    if form.validate_on_submit():
        # Si lo ha presionado, obtenemos los valores de los campos del fomrulario
        title = form.title.data
        title_slug = form.title_slug.data
        content = form.content.data
        # Añadimos estos nuevos valores a nuestra lista de diccionarios.
        posts.append({'title': title,
                      'title_slug': title_slug,
                      'content': content})
        # Redirigimos a la plantilla show_post.html para observar el nuevo post junto con los anteriores.
        return redirect(url_for('show_post'))
    
    # Si no lo presiona (al inicializar) simplemente pasamos al html el formulario de trabajo para poder trabajar con él.
    return render_template("admin/post_form.html", form=form)
    

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
        # Comprobamos si la dirección de correo introducida está almacenada en nuestra lista de usuarios
        user = get_user(form.email.data)
        # Verificamos si el usuario existe (no es None) y si la contraseña coincide
        if user is not None and user.check_password(form.password.data):
            # Inicia sesión con el usuario utilizando Flask-Login
            login_user(user, remember=form.remember_me.data)
            # Redirección después de iniciar sesión según si la identificación es válida o fallida.
            """
            El parámetro "next" se utiliza en aplicaciones web para recordar la URL originalmente solicitada antes
            de que un usuario sea redirigido a una página de inicio de sesión. Cuando un usuario no autenticado intenta
            acceder a una página protegida, se agrega el parámetro "next" a la URL de redirección. Después de iniciar
            sesión correctamente, la aplicación utiliza el valor de "next" para redirigir al usuario de vuelta a la página
            originalmente solicitada, proporcionando una experiencia de usuario más fluida y devolviéndolo a la ubicación
            deseada después de la autenticación.
            """
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                # Si las credenciales son correctas, redireccionamos al usuario a index.
                next_page = url_for('index')
            else:
                # Si las credenciales son incorrectas, mantenemos al usuario en la página de inicio de sesión.
                next_page = url_for('login')
            return redirect(next_page)
            
    # Si el formulario no se ha enviado o la autenticación falló, renderiza el formulario de inicio de sesión
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
def load_user(user_id):
    for user in users:
        if user.id == int(user_id):
            return user
    return None






# Definimos este como el script principal
if __name__ == '__main__':
    app.run(debug=True)