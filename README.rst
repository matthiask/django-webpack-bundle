=====================
django-webpack-bundle
=====================

Install ``django-webpack-loader``

Register webpack bundle as a template tag somewhere:

.. code-block:: python

    from django import template

    from webpack_bundle import webpack_bundle

    register = template.Library()

    register.simple_tag(webpack_bundle)


``webpack_bundle`` assumes that it may load Webpack bundles from
``settings.WEBPACK_BUNDLE_PATH`` or ``settings.BASE_DIR + "static/"``.
