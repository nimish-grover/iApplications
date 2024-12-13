from iJalagam.app.db import db

class Population(db.Model):
    __tablename__ = 'population'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    population_type = db.Column(db.String(100), nullable=False)
    short_name = db.Column(db.String(100), nullable=False) # sc, st, male, female
    display_name = db.Column(db.String(100), nullable=False)

    def __init__(self, population_type, display_name, short_name):
        self.population_type = population_type
        self.display_name = display_name
        self.short_name = short_name

    def __repr__(self):
        return f"<Population(id={self.id}, population_type={self.population_type}, display_name={self.display_name}, short_name={self.short_name})>"

    def json(self):
        return {
            "id": self.id,
            "population_type": self.population_type,
            "display_name": self.display_name,
            "short_name": self.short_name
        }
        
    @classmethod
    def get_all(cls):
        query = cls.query.order_by(cls.id).all()
        json_data = [result.json() for result in query]
        if json_data:
            return json_data
        else:
            return None