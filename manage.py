#!/usr/bin/env python
import os
import sys

def find_app_directory(root):
   for d in os.listdir(root):
      if not os.path.isdir(d) or d.startswith('.'):
         continue
      if os.path.exists(os.path.join(d, 'settings')):
         return d

   raise RuntimeError('no settings file found')

if __name__ == "__main__":
    app_dir = find_app_directory('.')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "%s.settings" % app_dir)
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
