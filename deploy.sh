# clean blog deploy script

echo '\n==== Start Install package from requirements.txt'
pip install -r requirements.txt

echo '\n==== start Migrate'
python manage.py migrate

echo '\n==== Create Super User'
python manage.py createsuperuser
