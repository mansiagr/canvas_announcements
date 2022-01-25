import canvasapi
from dateutil.tz import gettz
from jinja2 import Environment, FileSystemLoader
from datetime import datetime, timedelta
import datetime
import dateutil.tz

def my_function(access_token, course_number, number_of_week):
    con = canvasapi.Canvas('https://canvas.ucdavis.edu/',access_token)
    course = con.get_course(course_number)
    today = datetime.datetime.now(gettz('America/Los_Angeles'))
    tomorrow = today + datetime.timedelta(days = 1)
    assignments = course.get_assignments(published = True, locked_for_user = False, order_by = 'due_at')
    assignments = list(assignments)
    item_list_today = []
    item_list_tomorrow = []
    item_list_due = []
    url_due = []
    url_today = []
    url_tomorrow = []
    url_weekly = []

    for assignment in assignments: #setting due and lock date to America/Los_Angeles timezone
        if assignment.due_at != None:
            assignment.due_at_date =assignment.due_at_date.astimezone(gettz('America/Los_Angeles'))
        if assignment.lock_at != None:
            assignment.lock_at_date = assignment.lock_at_date.astimezone(gettz('America/Los_Angeles'))
    item_num_today = 0

    for assignment in assignments: #storing assignments 'due today' in a list
        if assignment.due_at != None:
            if assignment.due_at_date.date() == today.date():
                item_list_today.append(assignment)
                url_today.append('<a href="{}">'.format(assignment.html_url))
    if len(item_list_today) == 0: #will use to check if nothing is 'due today'
        item_num_today =1
    else:
        item_num_today = 0

    for assignment in assignments: #storing assignments 'due tomorrow' in a list
        if assignment.due_at != None:
            if assignment.due_at_date == tomorrow:
                item_list_tomorrow.append(assignment)
                url_tomorrow.append('<a href="{}">'.format(assignment.html_url))
    item_num_tomorrow =0;

    if len(item_list_tomorrow) == 0: #will use to check if nothing is 'due tomorrow'
        item_num_tomorrow =1
    else:
        item_num_tomorrow = 0

    url_today_len = len(url_today)
    number_of_weeks=number_of_week
    loop_variable = number_of_weeks+1
    
    #initializing variables to keep track of the days of the week
    one_day_off = datetime.timedelta(days=1) 
    six_days_off =datetime.timedelta(days=6)
    next_monday = today + datetime.timedelta(days=-today.weekday(), weeks=1)
    last_monday = today - datetime.timedelta(days=today.weekday())
    next_week = next_monday + datetime.timedelta(days=6)
    this_week = last_monday + datetime.timedelta(days=6)
    item_list_weekly = {}
    
    for i in range(1,loop_variable):
        if i != 1:
            last_monday = next_monday
            next_monday = next_week + one_day_off
            next_week = next_monday + six_days_off
            this_week = last_monday + six_days_off
        for assignment in assignments: #storing assignments 'due this week' in a dictionary
            if assignment.due_at != None:
                if last_monday <= assignment.due_at_date<= this_week:
                    url_weekly.append('<a href="{}">'.format(assignment.html_url))
                    if len(item_list_weekly) == 0:
                        item_list_weekly = { i: [assignment]}
                    else:
                        if i in item_list_weekly:
                            item_list_weekly[i].append(assignment)
                        else:
                            item_list_weekly.update({i:[assignment]})
                            
    for assignment in assignments: #storing assignments without a due date in a list
        if assignment.due_at == None:
            item_list_due.append(assignment.name)
            url_due.append('<a href="{}">'.format(assignment.html_url))

    list_len = len(item_list_due)
    
    #making jinja template
    file_loader = FileSystemLoader('file')
    env = Environment(loader=file_loader,extensions=['jinja2.ext.loopcontrols'])
    template = env.get_template('announcement.txt')
    
    #sending to jinja
    output = template.render(item_list=item_list_today, assignments=assignments, none=None, today=today,url_today=url_today, url_tomorrow=url_tomorrow,url_weekly=url_weekly,
                             item_list_tomorrow=item_list_tomorrow, item_list_weekly=item_list_weekly,url_today_len=url_today_len,
                             tomorrow=tomorrow, next_monday = next_monday, last_monday =last_monday,next_week=next_week, this_week =this_week, number_of_weeks=number_of_weeks,temp=loop_variable, one_day=one_day_off, other_day = six_days_off, item_list_due=item_list_due, list_len=list_len,  url_due=url_due, item_num_tomorrow=item_num_tomorrow, item_num_today=item_num_today)
   
    announcement = course.create_discussion_topic(title = 'Weekly Announcement', message = output, is_announcement = True) #creating announcement
    
my_function('3438~4Vsni6jehGa41fIsm2TqOVgbz8yhkBFk3lszBla2XKE16khplycivhmtKqsUZ3QK', 1599, 10) #calling function
