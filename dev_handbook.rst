================================================================================
Developper documentation
================================================================================

This is the developper documentation (handbook) for this project. This is things
to know.

Making Changes to a Database Schema
===================================

This is the procedure to apply if you change the database schema for the
project.

- Add the field to your model.

- Run manage.py sqlall [yourapp] to see the new
CREATE TABLE statement for the model. Note the column definition for the new
field.

- Start your database’s interactive shell (e.g., psql or mysql, or you can
use manage.py dbshell). Execute an ALTER TABLE statement that adds your new
column.
