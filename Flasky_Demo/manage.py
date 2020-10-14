import os
from flask_script import Manager, Shell
from flask_script.commands import ShowUrls, Clean, Server
from flask_migrate import Migrate, MigrateCommand

from app import create_app, db

app = create_app(os.getenv("FLASK_CONFIG", 'default'))
manager = Manager(app)
migrate = Migrate(app, db)


def _make_shell_context():
    return dict(app=app, db=db)


@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)


manager.add_command("shell", Shell(make_context=_make_shell_context))
manager.add_command("db", MigrateCommand)
manager.add_command("show-urls", ShowUrls())
manager.add_command("clean", Clean())
manager.add_command("runserver", Server())

if __name__ == '__main__':
    manager.run()
