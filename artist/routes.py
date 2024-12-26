from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app



artist_bp = Blueprint('artist', __name__, template_folder='templates')

@artist_bp.route('/profile')
def profile():
    return render_template('artist/profile.html', title="Artist Profile")

@artist_bp.route('/search')
def search():
    return render_template('artist/search.html', title="Search Songs/Albums")

@artist_bp.route('/add-songs', methods=['GET', 'POST'])
def add_songs():
    # Logic to add songs will be implemented here
    return render_template('artist/add_songs.html', title="Add Songs/Albums")

@artist_bp.route('/remove-songs', methods=['GET', 'POST'])
def remove_songs():
    # Logic to remove songs will be implemented here
    return render_template('artist/remove_songs.html', title="Remove Songs/Albums")


# Placeholder data for songs/albums
songs_albums = [
    {"type": "song", "title": "Song A"},
    {"type": "album", "title": "Album B"},
    {"type": "song", "title": "Song C"},
    {"type": "album", "title": "Album D"}
]

@artist_bp.route('/remove', methods=['GET', 'POST'])
def remove_song():
    if request.method == 'POST':
        remove_type = request.form.get('remove_type')
        title = request.form.get('title')
        confirm = request.form.get('confirm')

        # Validate form data
        if not remove_type or not title or not confirm:
            flash("All fields are required, and confirmation must be checked.", "danger")
            return redirect(url_for('artist.remove_song'))

        # Check if the song/album exists
        item_to_remove = next((item for item in songs_albums if item['type'] == remove_type and item['title'].lower() == title.lower()), None)

        if item_to_remove:
            songs_albums.remove(item_to_remove)
            flash(f"{remove_type.capitalize()} '{title}' has been successfully removed.", "success")
        else:
            flash(f"{remove_type.capitalize()} '{title}' not found.", "warning")

        return redirect(url_for('artist.remove_song'))

    return render_template('artist/remove_song.html', title="Remove Songs/Albums")

# Placeholder for the songs and albums data
songs_albums = []
"""
@artist_bp.route('/add', methods=['GET', 'POST'])
def add_song():
    if request.method == 'POST':
        name = request.form.get('name')
        type_ = request.form.get('type')

        # Validate inputs
        if not name or not type_:
            flash("All fields are required!", "danger")
            return redirect(url_for('artist.add_song'))

        # Check if the song/album already exists
        existing_item = next((item for item in songs_albums if item['type'] == type_ and item['title'].lower() == name.lower()), None)
        if existing_item:
            flash(f"{type_.capitalize()} '{name}' already exists.", "warning")
            return redirect(url_for('artist.add_song'))

        # Add the new song/album
        songs_albums.append({"type": type_, "title": name})
        flash(f"{type_.capitalize()} '{name}' has been added successfully!", "success")
        return redirect(url_for('artist.add_song'))

    return render_template('artist/add_songs.html', title="Add Songs/Albums")
"""
@artist_bp.route('/add', methods=['GET', 'POST'])
def add_song():
    if request.method == 'POST':
        # Get the song name from the form
        sarki_adi = request.form.get('name')

        # Validate the input
        if not sarki_adi:
            flash("Song name is required!", "danger")
            return redirect(url_for('artist.add_song'))

        # Use the MySQL instance from the current app context
        cur = current_app.mysql.connection.cursor()

        # Check if the song already exists in the database
        cur.execute("SELECT * FROM Sarki WHERE SarkiAdi = %s", (sarki_adi,))
        existing_song = cur.fetchone()

        if existing_song:
            flash(f"The song '{sarki_adi}' already exists.", "warning")
            cur.close()
            return redirect(url_for('artist.add_song'))

        # Insert the song into the database
        cur.execute("INSERT INTO Sarki (SarkiAdi) VALUES (%s)", (sarki_adi,))
        current_app.mysql.connection.commit()
        cur.close()

        flash(f"Song '{sarki_adi}' has been added successfully!", "success")
        return redirect(url_for('artist.add_song'))

    return render_template('artist/add_songs.html', title="Add Songs/Albums")