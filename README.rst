CookieCutter Provider Template
=====================

A cookiecutter template to create a Django app for a new third party provider:
    * The main provider event model.
    * Django admin views for the model changelist and model importing.

Quickstart
==========

1. Install cookiecutter, and apps listed in requirements.txt for our generated app.  Install them all with:

.. code-block:: console

    pip install -r https://raw.github.com/Feverup/cookiecutter-provider-template/master/requirements.txt


2. Run cookiecutter using this template.  Note that **it will overwrite existing files without warning if you already have an app dir of the same name**, so make sure your code is checked in or backed up.

.. code-block:: console

    cookiecutter git@github.com:Feverup/cookiecutter-provider-template.git


3. Update urls.py to include the new app:

.. code-block:: python

    url(r'^things/', include('yourproject.yourapp.urls', namespace='yourapp')),