#!/bin/bash
git push heroku heroku_deployment:master
heroku run python lazy_lecture_bot/manage.py migrate
