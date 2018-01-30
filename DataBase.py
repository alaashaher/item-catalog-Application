from sqlalchemy import Integer

from sqlalchemy import String

from sqlalchemy import Column

from sqlalchemy import ForeignKey

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()


# make categories table


class Category_table(Base):
    __tablename__ = 'categories_menu'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    @property
    def serialize(self):
        # Return object data in easily serializeable format
        return {
            'id': self.id,
            'name': self.name,
        }


# for user table

class user_table(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    img_user = Column(String, nullable=False)
    email = Column(String(250), nullable=False)


# for items table

class Item(Base):
    __tablename__ = 'items_menu'
    name = Column(String, nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    cat_id = Column(Integer, ForeignKey('categories_menu.id'))
    item_cat = relationship(Category_table)
    user_id = Column(Integer, ForeignKey('user.id'))
    item_user = relationship(user_table)

    @property
    def serialize(self):
        # Return object data in easily serializeable
        return {
            'name': self.name,
            'id': self.id,
            'description': self.description,
            'cat_id': self.cat_id,
        }


engine = create_engine('sqlite:///categories_menu.db')

Base.metadata.create_all(engine)
