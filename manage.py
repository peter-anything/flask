from apps import app, db
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
import importlib

manager = Manager(app)
migrate = Migrate(app, db)

installed_apps = app.config['INSTALLED_APPS']

for installed_app in installed_apps:
    try:
        app_models = importlib.import_module('.%s.models' % installed_app, package='apps')
        app_module = importlib.import_module('.%s' % installed_app, package='apps')
        print(app_module)
        app.register_blueprint(app_module.blue_print, url_prefix='/%s' % installed_app)
    except Exception as e:
        print('Import failed, %s' % e)


def make_shell_context():
    return dict(app=app, db=db)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

print(app.url_map)

if __name__ == '__main__':
    manager.run()
