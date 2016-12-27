#!/usr/bin/env python
import subprocess
import sys

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from done import app, db 

from done.models import *



manager = Manager(app)

manager.add_command('db', MigrateCommand)

migrate = Migrate(app, db)

@manager.command
def createdb(drop_first=False):
	"""Creates the database"""
	if drop_first:
		db.drop_all()
	db.create_all()



@manager.command
def test():
    """Runs unit tests."""
    tests = subprocess.call(['python', '-c', 'import tests; tests.run()'])
    sys.exit(tests)


@manager.command
def lint():
    """Runs code linter."""
    lint = subprocess.call(['flake8', '--ignore=E402', 'elite/',
                            'manage.py', 'tests/']) == 0
    if lint:
        print('OK')
    sys.exit(lint)

if __name__ == '__main__':
	manager.run()