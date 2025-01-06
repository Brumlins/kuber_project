from flask import Flask, request, render_template, redirect, url_for, flash


from app import db_manager
from app import login_manager


db = db_manager.session
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, SubmitField,DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length,InputRequired
from .models import User,Uzivatele
app = Flask(__name__)
app.secret_key = 'secret-key-for-flash-messages'

# Seznam uživatelů jako dočasné úložiště
users = []

class FormFormular(FlaskForm):
    name = StringField('Jméno', validators=[ InputRequired(message="Toto nemůže být prázdné")])
    surename = StringField('Příjmení', validators=[ InputRequired(message="Toto nemůže být prázdné")])

@app.route('/')
def index():
    form=FormFormular()
    if form.validate_on_submit():
        print(form.name.data)
        new_user = Uzivatele(name=form.name.data, surename=form.surename.data)
        db.add(new_user)
        db.commit()
        return "Formular submitted"
    return render_template("formular.html",form=form)

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        # Získání dat z formuláře
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        
        # Validace formuláře
        if not first_name or not last_name:
            flash('Jméno a příjmení jsou povinná pole!', 'error')
            return redirect(url_for('add_user'))
        
        # Přidání uživatele do seznamu
        users.append({'first_name': first_name, 'last_name': last_name})
        flash('Uživatel byl úspěšně přidán!', 'success')
        return redirect(url_for('index'))
    
    return render_template('add_user.html')

@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if 0 <= user_id < len(users):
        del users[user_id]
        flash('Uživatel byl úspěšně odstraněn!', 'success')
    else:
        flash('Uživatel nebyl nalezen!', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)