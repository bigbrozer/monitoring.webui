update issues
set created_on = datetime(due_date)
where created_on > due_date;
