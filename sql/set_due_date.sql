update issues
set due_date = date(updated_on)
where due_date is null
and status_id in (5, 6, 10);
