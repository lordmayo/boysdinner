=====
Boys Dinner
=====

Boys Dinner is a web-based app that allows chefs to sign in with their
names and dish descriptions, then on a rotational basis vote for each 
other's dishes. It also stores historical voting data 


Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "boysdinner" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'boysdinner',
    )

2. Include the boysdinner URLconf in your project urls.py like this::

    url(r'^boysdinner/', include('boysdinner.urls')),

3. Run `python manage.py migrate` to create the boysdinner models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create users for admin/testing purposes  (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/boysdinner/ to begin!
