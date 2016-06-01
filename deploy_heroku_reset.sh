#!/bin/bash
git push heroku heroku_deployment:master
heroku pg:reset DATABASE_URL
heroku run python lazy_lecture_bot/manage.py migrate
heroku run python lazy_lecture_bot/manage.py loaddata lazy_lecture_bot/main/fixtures/initial_data.json
heroku run python lazy_lecture_bot/manage.py rebuild_index
