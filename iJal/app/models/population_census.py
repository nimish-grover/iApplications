from sqlalchemy import func
from iJal.app.db import db
from iJal.app.models import Population, TerritoryJoin

class PopulationCensus(db.Model):
    __tablename__ = 'population_census'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    population_id = db.Column(db.Integer, db.ForeignKey('population.id'), nullable=False)
    population_count = db.Column(db.Integer, nullable=False)
    territory_id = db.Column(db.Integer, db.ForeignKey('territory_joins.id'), nullable=False)

    # Relationships
    population = db.relationship('Population', backref=db.backref('population_census', lazy="dynamic"))
    territory = db.relationship('TerritoryJoin', backref=db.backref('population_census', lazy="dynamic"))

    def __init__(self, population_id, population_count, territory_id):
        """
        Initialize the PopulationCensus instance with the provided attributes.
        """
        self.population_id = population_id
        self.population_count = population_count
        self.territory_id = territory_id

    def __repr__(self):
        """
        Provides a string representation of the PopulationCensus instance.
        """
        return (f"<PopulationCensus(id={self.id}, population_id={self.population_id}, "
                f"population_count={self.population_count}, territory_id={self.territory_id})>")

    def json(self):
        """
        Returns a JSON serializable dictionary representation of the PopulationCensus instance.
        """
        return {
            "id": self.id,
            "population_id": self.population_id,
            "population_count": self.population_count,
            "territory_id": self.territory_id
        }


    @classmethod
    def get_population_by_block(cls, block_id, district_id):
        query = db.session.query(
        func.sum(PopulationCensus.population_count).label("population_count"),
        Population.id,
        Population.display_name
        ).join(TerritoryJoin, TerritoryJoin.id == PopulationCensus.territory_id
        ).join(Population, Population.id == PopulationCensus.population_id
        ).filter(
            TerritoryJoin.block_id == block_id,
            TerritoryJoin.district_id == district_id,
            Population.id.in_([2, 3]) # 2 = 'male', 3 = 'female'
        ).group_by(
            TerritoryJoin.block_id,
            TerritoryJoin.district_id,
            Population.id,
            Population.display_name,
            Population.population_type
        )
        results = query.all()

        if results:
            result = [
                {
                    "entity_value": row.population_count,
                    "entity_id": row.id,
                    "entity_name": row.display_name
                }
                for row in results
            ]
            return result
        else:
            return None
