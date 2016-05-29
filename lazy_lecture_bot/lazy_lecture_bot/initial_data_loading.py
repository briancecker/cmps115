# Load some intial data from the fixtures files
import os

from django.core.management import call_command


# The app's that have fixtures you want to load data from
from django.db import connection

FIXTURES = [("main", "fixtures", "initial_data.json")]


def import_data():
    if "main_pipelinetypes" in connection.introspection.table_names():
        for fixture in FIXTURES:
            call_command("loaddata", os.path.join(*fixture))



