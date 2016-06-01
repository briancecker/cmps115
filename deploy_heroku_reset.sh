#!/bin/bash
git push heroku heroku_deployment:master
heroku pg:reset DATABASE_URL
heroku python run lazy_lecture_bot/manage.py migrate
heroku python run lazy_lecture_bot/manage.py loaddata lazy_lecture_bot/main/fixtures/initial_data.json
heroku python run lazy_lecture_bot/manage.py rebuild_index
