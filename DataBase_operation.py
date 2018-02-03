from sqlalchemy.orm import sessionmaker

from sqlalchemy import create_engine

from DataBase import Base, Category_table, Item, user_table

url = 'sqlite:///categories_menu.db'

engine = create_engine(url)

Base.metadata.bind = engine

database_session = sessionmaker(bind=engine)

session = database_session()

# create operations class

class database_operations:
    def adduser(self, login_session):
        newUser = user_table(
            name=login_session['userName'],
            email=login_session['email'],
            img_user=login_session['img_user'])
        session.add(newUser)
        session.commit()
        return

    def GetUserBy(self, login_session):
        try:
            user = session.query(user_table).filter_by(
                email=login_session['email']).one()
            return user
        except:
            self.adduser(login_session)
            return session.query(
                user_table).filter_by(email=login_session['email']).one()

    def addDatabase(self, add_element):
        session.add(add_element)
        session.commit()
        return

    def addDatabase(self, updated_element):
        session.add(updated_element)
        session.commit()
        return

    def deleteDatabase(self, item):
        session.delete(item)
        session.commit()
        return

class item_operations:
    def GetCategory(self, cat_id):
        return session.query(Category_table).filter_by(id=cat_id).one()

    def GetAllCategory(self):
        return session.query(Category_table).all()

    def GetOneItem(self, i_id):
        return session.query(Item).filter_by(id=i_id).join(Category_table).one()

    def GetItem(self, cat_id):
        return session.query(Item).filter_by(cat_id=cat_id).all()

    def Get_last_item(self):
        return session.query(Item).limit(10)
