from flask import Blueprint, render_template

artist_bp = Blueprint('artist', __name__, template_folder='templates')

@artist_bp.route('/profile')
def profile():
    return render_template('artist/profile.html', title="Artist Profile")
