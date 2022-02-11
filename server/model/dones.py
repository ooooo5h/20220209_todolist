from server import db

class Dones(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    todo_id = db.Column(db.Integer, db.ForeignKey('todos.id'))
    score = db.Column(db.Float) # 평점은 추후에 수정할 때만 나타내자
    
    def get_data_object(self):
        data = {
            'id' : self.id,
            'todo_id' : self.todo_id,
            'score' : self.score if self.score else None,
        }
        
        return data