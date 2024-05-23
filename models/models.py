from models.database import db

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    muscle = db.Column(db.String(100), nullable=False)
    equipment = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)

    def __init__(self, name, type, muscle, equipment, difficulty):
        self.name = name
        self.type = type
        self.muscle = muscle
        self.equipment = equipment
        self.difficulty = difficulty

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'muscle': self.muscle,
            'equipment': self.equipment,
            'difficulty': self.difficulty
        }