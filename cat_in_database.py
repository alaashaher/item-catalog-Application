from DataBase import Category_table
from DataBase_operation import database_operations

item = database_operations()
new_categories = [Category_table(name='pizza'),
                  Category_table(name='pasta'),
                  Category_table(name='Chicken soup'),
                  Category_table(name='Cheese Steak'),
                  Category_table(name='Shawarma'),
                  Category_table(name='cake'),
                  Category_table(name='Cheesecake with cheese')]

for new_cat in new_categories:
    item.addDatabase(new_cat)
