External libraries
==================

Because that right now we are only using crypto-js, it is unnecessary to use npm or bower, so if crypto-js needs to be upgraded here are the steps:

1) Go to https://github.com/brix/crypto-js/releases
2) Download the latest release
3) Unzip
4) Fix paths in registry.xml
5) Recompile JS


We also use the alerts css from bootstrap.

1) Go to http://getbootstrap.com/getting-started/
2) Download "Source code"
3) Copy variables.less and alerts.less to the "less" folder inside the pattern


Compiling Javascript
====================

The Javascript here is compiled as follows:

./bin/plone-compile-resources --site-id=Plone --bundle=jsalerts
