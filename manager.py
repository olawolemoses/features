#!/usr/bin/env python
import os
COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

if os.path.exists('.env'):
    print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

from app import create_app, db
from app.models import User, Client, Role, ProductArea, Project
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def deploy():
    from flask_migrate import upgrade
    from app.models import Role, User

    # migrate database to latest revision
    upgrade()

    "Add seed data to the database."
    #clients
    client1 = Client(client_name="Client A")
    db.session.add(client1)
    client2 =Client(client_name="Client B")
    db.session.add(client2)
    client3 = Client(client_name="Client C")
    db.session.add(client3)

    #roles
    role1 = Role(name="Admin", description='Admin of IWS')
    db.session.add(role1)
    role2 =Role(name="Staff", description='Staff of IWS')
    db.session.add(role2)

    #product areas
    product_area1 = ProductArea(product_area="Policies")
    db.session.add(product_area1)
    product_area2 =ProductArea(product_area="Billing")
    db.session.add(product_area2)
    product_area3 = ProductArea(product_area="Claims")
    db.session.add(product_area3)
    product_area3 = ProductArea(product_area="Reports")
    db.session.add(product_area3)

    #project
    project1 = Project(project_name="Project A")
    db.session.add(project1)
    project2 =Project(project_name="Project B")
    db.session.add(project2)
    project3 = Project(project_name="Project C")
    db.session.add(project3)

    db.session.commit()

@manager.command
def test(coverage=False):
    """Run the unit tests."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()


@manager.command
def profile(length=25, profile_dir=None):
    """Start the application under the code profiler."""
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length],
                                      profile_dir=profile_dir)
    app.run()


if __name__ == '__main__':
    manager.run()
