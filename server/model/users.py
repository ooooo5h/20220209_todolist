from server import db

class Users(db.Model):
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    u_id = db.Column(db.String(20), nullable=False)
    u_pw_hashed = db.Column(db.String(32), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    nickname = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    signout_at = db.Column(db.DateTime)
    
    my_toto = db.relationship('Todos', backref= 'user')
    
    def get_data_object(self, need_todos=False):
        data = {
            'id' : self.id,
            'u_id' : self.u_id,
            'name' : self.name,
            'phone' : self.phone,
            'nickname' : self.nickname,
            'created_at' : str(self.created_at),
            'signout_at' : str(self.signout_at) if self.signout_at else None, # "None"이 아닌 null로 나가게끔 => 그렇게 해야 프론트에서 쓸 떄 에러안나고 쓰기 좋음 
        }
        
        if need_todos:
            data['my_totos'] = [mine.get_data_object() for mine in self.my_toto]
        
        return data