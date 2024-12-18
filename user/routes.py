from flask import Blueprint, render_template

user_bp = Blueprint('user', __name__, template_folder='templates')

@user_bp.route('/home')
def home():
    return render_template('user/home.html', title="User Home")
