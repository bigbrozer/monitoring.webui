================================================================================
Developper documentation
================================================================================

This is the developper documentation (handbook) for this project. This is things
to know.

PyCharm
=======

Team configuration
------------------

The Pycharm's config is shared among us and stored in ``.idea`` folder which is
part of the repository. It includes default run configuration, coding styles,
etc...

Configuring Python interpreter
------------------------------

The Python interpreter should be called ``Python (optools)`` and Python bin set
to ``~/Envs/optools/bin/python``.

Making Changes to a Database Schema
===================================

This is the procedure to apply if you change the database schema for the
project.

- Add the field to your model.

- Run ``manage.py sqlall [yourapp]`` to see the new
CREATE TABLE statement for the model. Note the column definition for the new
field.

- Start your database’s interactive shell (e.g., psql or mysql, or you can
use ``manage.py dbshell``). Execute an ``ALTER TABLE`` statement that adds your
new column.

Cron jobs
=========

Look at the django's user crontab for the list of croned jobs on
monitoring-dc.app.corp::

 $ ssh monitoring-dc.app.corp -l django
 $ crontab -l
