=====
Usage
=====

To use Django Handy in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_handy.apps.DjangoHandyConfig',
        ...
    )

Add Django Handy's URL patterns:

.. code-block:: python

    from django_handy import urls as django_handy_urls


    urlpatterns = [
        ...
        url(r'^', include(django_handy_urls)),
        ...
    ]
