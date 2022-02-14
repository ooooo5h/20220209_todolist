from server import db

class TodoImages(db.Model):
    
    __tablename__ = 'todo_images'
    
    id = db.Column(db.Integer, primary_key=True)
    todo_id = db.Column(db.Integer, db.ForeignKey('todos.id'))
    image_url = db.Column(db.String(200))
    
    def get_data_object(self):
        data = {
            'id' : self.id,
            'todo_id' : self.todo_id,
            'image_url' : self.image_url,
        }
        
        
        return data