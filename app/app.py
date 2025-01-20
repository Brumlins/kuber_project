from flask import Flask, request, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
# Inicializace aplikace a připojení k SQLite databázi
app = Flask(__name__)
app.secret_key = 'secret-key-for-flash-messages'

# Nastavení pro připojení k SQLite databázi
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializace SQLAlchemy
db = SQLAlchemy(app)

# Model pro uživatele (databázová tabulka)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name}>"

# WTForm pro přidání uživatele
class UserForm(FlaskForm):
    first_name = StringField('Jméno', validators=[DataRequired(message='Jméno je povinné!')])
    last_name = StringField('Příjmení', validators=[DataRequired(message='Příjmení je povinné!')])

@app.route('/')
def index():
    users = User.query.all()  # Získání všech uživatelů z databáze
    return render_template('index.html', users=users)

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    form = UserForm()

    if form.validate_on_submit():
        # Získání dat z formuláře
        first_name = form.first_name.data
        last_name = form.last_name.data
        
        # Vytvoření nového uživatele
        new_user = User(first_name=first_name, last_name=last_name)
        
        # Přidání uživatele do databáze
        db.session.add(new_user)
        db.session.commit()
        
        flash('Uživatel byl úspěšně přidán!', 'success')
        return redirect(url_for('index'))
    
    return render_template('add_user.html', form=form)

@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    # Nahrazení starší metody .get() novější metodou db.session.get()
    user = db.session.get(User, user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash('Uživatel byl úspěšně odstraněn!', 'success')
    else:
        flash('Uživatel nebyl nalezen!', 'error')
    return redirect(url_for('index'))


if __name__ == '__main__':
    # Vytvoření tabulek v databázi (pokud ještě neexistují)
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)
