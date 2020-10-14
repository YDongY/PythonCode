import os
from flask_migrate import Migrate

from app import create_app, db
from app.models import User

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

app = create_app(os.getenv("FLASK_CONFIG", 'default'))
migrate = Migrate(app, db)


@app.shell_context_processor
def _make_shell_context():
    return dict(app=app, db=db)


@app.cli.command()
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
