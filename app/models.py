from app import app, db

class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key = True)
  username = db.Column(db.String(64), index = True, unique = True)
  password = db.Column(db.String)

  def is_authenticated(self):
    return True

  def is_active(self):
    return True

  def get_id(self):
    return unicode(self.id)

  def is_anonymous(self):
    return False

class Todo(db.Model):
  __tablename__ = 'todo'
  id = db.Column(db.Integer, primary_key = True)
  user = db.Column(db.Integer)
  subject = db.Column(db.String(64))
  priority = db.Column(db.Integer)
  deadline = db.Column(db.String(64))
