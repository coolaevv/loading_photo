import os
from flask import Flask, render_template, url_for, request, redirect, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

UPLOAD_FOLDER = 'static/img'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///img.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class ImgList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    filename = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<ImgList %r>' % self.id


def allowed_file(filename):
    filename = filename.lower()
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def HomePage():
    images = ImgList.query.order_by(ImgList.id).all()
    ln = len(ImgList.query.order_by(ImgList.id).all())
    return render_template('home.html', images=images, leng=ln)


@app.route('/image-list')
def ImagesPage():
    images = ImgList.query.order_by(ImgList.id).all()
    return render_template('ImageList.html', images=images)


@app.route('/edit_data', methods=['POST'])  # Изменеие конкретной записи
def EditData():
    id_post = request.values['id'].replace('img_', '')
    title = request.values['title']
    desc = request.values['desc']
    post = ImgList.query.order_by(ImgList.id).get(id_post)
    try:
        post.title = title
        post.description = desc
        db.session.commit()
    except:
        pass
    return 'Отредактировано'


@app.route('/del_data', methods=['POST'])  # Удаление конкретной записи
def DelData():
    id_post = request.values['id']
    id_post = id_post.replace('img_', '')
    post = ImgList.query.get_or_404(id_post)

    try:
        db.session.delete(post)
        db.session.commit()
    except:
        pass
    posts = ImgList.query.order_by(ImgList.id).all()
    index = 1
    for img in posts:
        img.id = index
        db.session.commit()
        index += 1
    print(index)
    return 'Удалено'


@app.route('/add', methods=['GET', 'POST'])
def AddPhoto():
    if request.method == 'POST':
        name = request.form['title']
        desc = request.form['desc']
        file = request.files['FileImg']
        filename = file.filename
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        query = ImgList(title=name, description=desc, filename=filename)
        try:
            db.session.add(query)
            db.session.commit()
            return redirect('/image-list')
        except:
            return 'При добавлении изображения произошла ошибка!'
    else:
        return render_template('AddImage.html')


if __name__ == '__main__':
    app.run(debug=True)
