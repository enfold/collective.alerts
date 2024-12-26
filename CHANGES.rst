Changelog
=========


3.1.3 (2024-12-26)
------------------

- When the alert is opened, add a class to the button in case special styling is needed
  [frapell]


3.1.2 (2023-06-28)
------------------

- Replace 'alt' in buttons with 'aria-label'
  [frapell]


3.1.1 (2023-05-19)
------------------

- Add 'alt' attribute to alert buttons
  [frapell]


3.1.0 (2022-12-20)
------------------

- Upgrade to latest mockup and patternslib
  [frapell]

- When rendering in "mobile" mode, simply add a new class to the element
  [frapell]

- Add ability to specify how much time a minimized alert, should not 
  automatically start opened
  [frapell]

- Add 'id' attributes to the viewlet <div>'s
  [frapell]

- Add 'Slide from the top' location to the alert
  [frapell]


3.0.0 (2022-09-01)
------------------

- Plone 6 / ES6
  [frapell]


2.3.0 (2019-12-10)
------------------

- Allow to modify the alert types from the control panel
  [frapell]

- Honour the 'Enable alerts' setting on content
  [frapell]

- Find whether the get-alerts views are intended to be cached, and avoid
  jquery .ajax() call to bust the cache automatically. Also provide a
  cache purge event for them
  [frapell]

- Include jquery.cookie plugin
  [frapell]


2.2.0 (2018-07-25)
------------------

- Allow to create an alert message using a request header
  [frapell]


2.1.0 (2018-05-11)
------------------

- Include a permission that protects the 'Enable Alerts' checkbox when
  adding/editing content
  [frapell]


2.0.2 (2018-03-08)
------------------

- Default cookie expire to 24 hours
  [frapell]


2.0.1 (2017-12-07)
------------------

- Include minimize icon
  [frapell]


2.0 (2017-11-08)
----------------

- Release again with new version to avoid conflicts
  [frapell]


1.0 (2017-10-06)
----------------

- Initial release.
  [frapell]
