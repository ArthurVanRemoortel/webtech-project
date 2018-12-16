#!/bin/bash

perl -i -pe 's/(^.*choices=\[\(o.id, str\(o.name\)\) for o in Venue.objects.all\(\)\])/#$1/' webtech/forms.py
python3 manage.py makemigrations
python3 manage.py migrate
perl -i -pe 's/^#(.*choices=\[\(o.id, str\(o.name\)\) for o in Venue.objects.all\(\)\])/$1/' webtech/forms.py

