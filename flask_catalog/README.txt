
// 
// mysql part
1) Install all noted requirements sudo pip install -r requirements.txt
2) login into mysql with "mysql -u root -p"
3) type "CREATE DATABASE catalog"
4) type "Use Catalog"
5) 

// ORM part
1) ssh into vagrant
2) cd into vagrant
3) command => python flask_catalog/manage.py shell
4) a shell will appear
5) type "from flask_catalog import db"
6) type "from author.models import *"
7) type "db.create_all()"
8) you can verify that everything worked by going to the mysql tab and run "show tables" and you should see the "author" table created
9) type "from catalog.models import *"
10) type "db.create_all()"
11) verify that the 1) item, 2) catalog and 3) category tables are created

// To run application
1) in the terminal, run "python /vagrant/flask_catalog/manage.py runserver"