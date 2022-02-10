from server import db

class Users(db.Model):
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    u_id = db.Column(db.String(20), nullable=False)
    u_pw = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    nickname = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    signout_at = db.Column(db.DateTime)
    
    def get_data_object(self):
        data = {
            'id' : self.id,
            'u_id' : self.u_id,
            'name' : self.name,
            'nickname' : self.nickname,
            'created_at' : str(self.created_at),
            'signout_at' : str(self.signout_at) if self.signout_at else None,
        }
        
        return data