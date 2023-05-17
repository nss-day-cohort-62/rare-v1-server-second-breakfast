#!/bin/bash

rm -rf rareapi/migrations
rm db.sqlite3
python3 manage.py makemigrations
python3 manage.py migrate
python manage.py makemigrations rareapi
python manage.py migrate rareapi
python3 manage.py loaddata users tokens rare_users  category posts comments tags reactions post_reactions post_tags subscriptions