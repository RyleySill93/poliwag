import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# DJANGO Setup
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "poliwag.settings")
django.setup()


def main():
    # Do stuff
    ...


if __name__ == "__main__":
    main()
