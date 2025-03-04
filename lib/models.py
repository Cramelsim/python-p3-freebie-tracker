from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, create_engine
from sqlalchemy.orm import relationship, sessionmaker, declarative_base, backref


convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s"
}
metadata = MetaData(naming_convention=convention)


Base = declarative_base(metadata=metadata)


class Company(Base):
    __tablename__ = 'companies'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    founding_year = Column(Integer, nullable=False)

    freebies = relationship("Freebies", backref="company", cascade="all, delete-orphan")
    devs = relationship("Dev", secondary="freebies", back_populates="companies")

    def __repr__(self):
        return f"<Company {self.name}>"

    def give_freebie(self, session, dev, item_name, value):
        freebie = Freebies(item_name=item_name, value=value, dev=dev, company=self)
        session.add(freebie)
        session.commit()

    @classmethod
    def oldest_company(cls, session):
        return session.query(cls).order_by(cls.founding_year).first()

class Dev(Base):
    __tablename__ = 'devs'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    freebies = relationship("Freebies", backref="dev", cascade="all, delete-orphan")
    companies = relationship("Company", secondary="freebies", back_populates="devs")

    def __repr__(self):
        return f"<Dev {self.name}>"

    def received_one(self, item_name):
        return any(freebie.item_name == item_name for freebie in self.freebies)

    def give_away(self, session, dev, freebie):
        if freebie in self.freebies:
            freebie.dev = dev
            session.commit()

class Freebies(Base):
    __tablename__ = 'freebies'

    id = Column(Integer, primary_key=True)
    item_name = Column(String, nullable=False)
    value = Column(Integer, nullable=False)
    dev_id = Column(Integer, ForeignKey('devs.id', ondelete="CASCADE"))
    company_id = Column(Integer, ForeignKey('companies.id', ondelete="CASCADE"))

    
    def __repr__(self):
        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}."


DATABASE_URL = 'sqlite:///freebies.db'
engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)

def create_tables():
    Base.metadata.create_all(engine)
