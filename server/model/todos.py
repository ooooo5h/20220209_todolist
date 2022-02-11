from server import db

class Todos(db.Model):
    
    __tablename__ = 'todos'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    duedate = db.Column(db.Date, nullable=False)
    is_completed = db.Column(db.Boolean, nullable=False, default=False)
    
    def get_data_object(self):
        data = {
            'id' : self.id,
            'user_id' : self.user_id,
            'title' : self.title,
            'content' : self.content,
            'created_at' : str(self.created_at),
            'duedate' : str(self.duedate),
            'is_completed' : self.is_completed,
        }
        
        return data