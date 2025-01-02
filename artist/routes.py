from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app


artist_bp = Blueprint('artist', __name__, template_folder='templates')

@artist_bp.route('/profile')
def profile():
    return render_template('artist/profile.html', title="Artist Profile")

@artist_bp.route('/search')
def search():
    return render_template('artist/search.html', title="Search Songs/Albums")

@artist_bp.route('/remove-songs', methods=['GET', 'POST'])
def remove_songs():
    try:
        if request.method == 'POST':
            remove_type = request.form.get('remove_type')
            title = request.form.get('title')
            confirm = request.form.get('confirm')

            # Validate input
            if not remove_type or not title or not confirm:
                flash("Type, Title, and Confirmation are required!", "danger")
                return redirect(url_for('artist.remove_songs'))

            # Access MySQL connection
            cur = current_app.config['MYSQL'].connection.cursor()
            if remove_type == 'song':
                query = "DELETE FROM Sarki WHERE SarkiAdi = %s"
                cur.execute(query, (title,))
            elif remove_type == 'album':
                query = "DELETE FROM Album WHERE AlbumAdi = %s"
                cur.execute(query, (title,))
            else:
                flash("Invalid type selected. Please choose 'Song' or 'Album'.", "danger")
                return redirect(url_for('artist.remove_songs'))

            # Commit the transaction
            current_app.config['MYSQL'].connection.commit()
            cur.close()

            # Provide feedback to the user
            flash(f"{remove_type.capitalize()} '{title}' has been removed successfully!", "success")
            return redirect(url_for('artist.remove_songs'))
    except Exception as e:
        flash(f"An error occurred: {e}", "danger")
        return redirect(url_for('artist.remove_songs'))

    return render_template('artist/remove_songs.html', title="Remove Songs/Albums")


@artist_bp.route('/add-songs', methods=['GET', 'POST'])
@artist_bp.route('/add-songs', methods=['GET', 'POST'])
def add_songs():
    try:
        if request.method == 'POST':
            name = request.form.get('name')
            type_ = request.form.get('type')
            duration = request.form.get('duration')
            artist_id = request.form.get('artist_id')
            genre_id = request.form.get('genre_id')
            album_id = request.form.get('album_id')
            release_date = request.form.get('release_date')

            # Validate MM:SS format for duration
            import re
            if duration and not re.match(r"^[0-5][0-9]:[0-5][0-9]$", duration):
                flash("Duration must be in MM:SS format (e.g., 03:45).", "danger")
                return redirect(url_for('artist.add_songs'))

            if not name or not type_ or not artist_id:
                flash("Name, Type, and Artist ID are required!", "danger")
                return redirect(url_for('artist.add_songs'))

            # Access MySQL from current_app
            cur = current_app.config['MYSQL'].connection.cursor()
            if type_ == 'song':
                query = """
                    INSERT INTO Sarki (SarkiAdi, Sure, YayinTarihi, TurID, AlbumID, SanatciID)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                params = (name, duration or None, release_date or None, genre_id or None, album_id or None, artist_id)
                cur.execute(query, params)
            elif type_ == 'album':
                query = """
                    INSERT INTO Album (AlbumAdi, YayinTarihi, TurID, SanatciID)
                    VALUES (%s, %s, %s, %s)
                """
                params = (name, release_date or None, genre_id or None, artist_id)
                cur.execute(query, params)

            current_app.config['MYSQL'].connection.commit()
            cur.close()

            flash(f"{type_.capitalize()} '{name}' has been added successfully!", "success")
            return redirect(url_for('artist.add_songs'))
    except Exception as e:
        flash(f"An error occurred: {e}", "danger")
        return redirect(url_for('artist.add_songs'))

    return render_template('artist/add_songs.html', title="Add Songs/Albums")