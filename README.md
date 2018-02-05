-Item Catalog Applaction
	I will develop an application that provides a list of items within a variety of categories as well as provide a user registration and authentication system.


-Download Vagrant and install it

-Create file (DataBase.py) and put in it three tabe of database.

	** categories_menu the table of categories have.
	  *** id of it.
	  *** name of each  Category.

	** user the table of user have.
	  *** id of each  user.
	  *** name of each  user.
	  *** img_user of each  user.
	  *** email of each  user.

	** items_menu the table of items have.
	  *** id of each  item.
	  *** name of each  item.
	  *** description of each  item.
	  *** cat_id of each  item.
	  *** user_id of each  item.

Open terminal and go to path file vagrant

write vagrant up

write vagrant ssh

write cd /vagrant

put the file of project in vagrant file 

write cd \ITEM_CATALOG_APP

then write python DataBase.py

Create file (DataBase_operation.py) and put in it functions.

	** adduser : to add user in tabel user by Google.

	** GetUserBy : to check if user in data or not to add.

	** GetCategory : to get Category from data.

	** GetAllCategory: to get all Categories from data.

	** GetItem : to get item from data.

	** Get_last_item : to get all items from data.

	** addDatabase : to add item and upload in data.

	** deleteDatabase : to delete item from data.

then open Terminal and call it file by (DataBase_operation.py).

Create file (cat_in_database.py) and use it to put the Categories in categories_menu tabel.

then open Terminal and call it file by (cat_in_database.py).

the put client_secrets.json in the file and Vagrantfile.

then make folder templates and put in it 7 file.

	** login.html : that page show all catalog and the sign in Google.

	** categoires.html : that page show all categoires and items of it after login.

	** catogray.html : that show each cateogry and all it's items.

	** itemShow.html : login.html that show each item.

	** addItem.html : that add item in database.

	** delete_item.html: that delete item from database.

	** edite_item.html : that esite item in database.

Create file main_page.py that conected. #JSON API ** the function catalogJSON that show json for categoires.

	** the function catalogJSON that show json for categoires. #connected in google
	** the function gconnect that use to sign in Google. #login google
	** the function showLogin use to sign in Google. #start Pages show
	** the function show_items_for_category that show categoires.

#desconnectes in google
	** the function gdisconnect that use to sign up Google.

Open in a webpage
	Now you can open in a webpage by going to either: ** http://0.0.0.0:8080 ** http://localhost:5000 ** then open Terminal and call it file by (main_page.py).


