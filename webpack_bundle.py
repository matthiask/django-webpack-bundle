import io
import logging
import os

from django import template
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.html import mark_safe

from webpack_loader.exceptions import BaseWebpackLoaderException
from webpack_loader.utils import get_files


if hasattr(settings, "WEBPACK_BUNDLE_PATH"):
    WEBPACK_BUNDLE_PATH = settings.WEBPACK_BUNDLE_PATH
elif hasattr(settings, "BASE_DIR"):
    WEBPACK_BUNDLE_PATH = os.path.join(settings.BASE_DIR, "static")
else:
    raise ImproperlyConfigured("Unable to determine the Webpack bundle path.")


JS_INLINE = '<script type="text/javascript">{chunk}</script>'
CSS_INLINE = '<style type="text/css">{chunk}</style>'
JS_EXTERNAL = '<script type="text/javascript" src="{url}" {attrs}></script>'
CSS_EXTERNAL = '<link type="text/css" rel="stylesheet" href="{url}" {attrs} />'


def webpack_bundle(
    bundle_name, extension=None, config="DEFAULT", attrs="", inline=False
):
    try:
        chunks = get_files(bundle_name, extension=extension, config=config)
    except BaseWebpackLoaderException:
        logging.warning(
            "Unable to resolve webpack bundle %s in config %s" % (bundle_name, config)
        )
        return ""

    tags = []
    for chunk in chunks:
        path = os.path.join(WEBPACK_BUNDLE_PATH, chunk["name"])
        if os.path.exists(path) and inline:
            with io.open(path, "r", encoding="utf-8") as f:
                if chunk["name"].endswith((".js", ".js.gz")):
                    tags.append(JS_INLINE.format(chunk=f.read()))
                elif chunk["name"].endswith((".css", ".css.gz")):
                    tags.append(CSS_INLINE.format(chunk=f.read()))
        else:
            if chunk["name"].endswith((".js", ".js.gz")):
                tags.append(JS_EXTERNAL.format(url=chunk["url"], attrs=attrs))
            elif chunk["name"].endswith((".css", ".css.gz")):
                tags.append(CSS_EXTERNAL.format(url=chunk["url"], attrs=attrs))
    return mark_safe("".join(tags))
