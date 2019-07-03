=====================
django-webpack-bundle
=====================

A `django-webpack-loader <https://github.com/owais/django-webpack-loader>`__
template tag which optionally supports rendering chunks inline. This may be
useful e.g. for the manifest respectively the Webpack runtime.

Install ``django-webpack-loader``

Register webpack bundle as a template tag somewhere:

.. code-block:: python

    from django import template

    from webpack_bundle import webpack_bundle

    register = template.Library()

    register.simple_tag(webpack_bundle)


``webpack_bundle`` assumes that it may load Webpack bundles from
``settings.WEBPACK_BUNDLE_PATH`` or ``settings.BASE_DIR + "static/"``.

The arguments to the ``{% webpack_bundle %}`` template tag are basically
the same as those for django-webpack-loader's ``{% render_bundle %}`` 
except for the additional ``inline`` argument which optionally allows
rendering chunks inline if the files can be found.
