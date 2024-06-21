from flask import (
        Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('workout', __name__)

@bp.route('/')
@login_required
def index():
    db = get_db()
    workouts = db.execute(
            'SELECT w.id, w.date, w.workout_name, u.username'
            ' FROM workout w JOIN users u ON w.user_id = u.id'
            ' ORDER BY w.date DESC'
    ).fetchall()
    return render_template('workout/index.html', workouts=workouts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        workout_name = request.form['workout_name']
        date = request.form['date']
        exercises = request.form.getlist('exercises')
        error = None

        if not workout_name:
            error = 'Workout name is required.'

        if not date:
            error = 'Date is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO workouts (user_id, date, workout_name)'
                ' VALUES (?, ?, ?)',
                (date, workout_name, g.user['id'])
            )
            workout_id = db.execute('SELECT last_insert_rowid()').fetchone()[0]
            for exercise in exercises:
                db.execute(
                    'INSERT INTO exercises (workout_id, exercise_name, sets, reps, weight)'
                    ' VALUES (?, ?, ?, ?, ?)',
                    (workout_id, exercise['name'], exercise['sets'], exercise['reps'], exercise['weight'])
                )
            db.commit()
            return redirect(url_for('workout.index'))

    return render_template('workout/create.html')

def get_workout(id, check_author=True):
    workout = get_db().execute(
        'SELECT w.id, w.date, w.workout_name, w.user_id, u.username'
        ' FROM workouts w JOIN user u ON w.user_id = u.id'
        ' WHERE w.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Workout id {id} doesn't exist.")

    if check_author and post['user_id'] != g.user['id']:
        abort(403)

    return workout

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    workout = get_workout(id)

    if request.method == 'POST':
        workout_name = request.form['workout_name']
        date = request.form['date']
        exercises = request.form.getlist('exercises')
        error = None

        if not workout_name:
            error = 'Workout name is required.'

        if not date:
            error = 'Date is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE workouts SET workout_name = ?, body = ?'
                ' WHERE id = ?',
                (workout_name, date, id)
            )
            db.execute('DELETE FROM exercises WHERE workout_id = ?', (id,))
            for exercise in exercises:
                db.execute(
                    'INSERT INTO exercises (workout_id, exercise_name, sets, reps, weight)'
                    ' VALUES (?, ?, ?, ?, ?)',
                    (id, exercise['name'], exercise['sets'], exercise['reps'], exercise['weight'])
                )
            db.commit()
            return redirect(url_for('workout.index'))

    return render_template('workout/update.html', workout=workout)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_workout(id)
    db = get_db()
    db.execute('DELETE FROM workouts WHERE id = ?', (id,))
    db.execute('DELETE FROM exercises WHERE workout_id = ?', (id,))
    db.commit()
    return redirect(url_for('workout.index'))
