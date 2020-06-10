from app import db

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coursename = db.Column(db.String(128), index=True, unique=True)
    files = db.relationship('Files', backref='Cname', lazy='dynamic')

    def __repr__(self):
        return '<Coursename {}>'.format(self.coursename)

class Files(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(256), index=True, unique=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))

    def __repr__(self):
        return '<Filename {}>'.format(self.filename)      