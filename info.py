import schedule_info 


class Workers:
    def __init__(self, id) -> None:
        self.id = id
        #self.lessons = lessons
         
        
    def schedule(self):
        platon_lessons = schedule_info.platon_schedule
        if self.id == '270491271':
            return platon_lessons

'''
data = open('data.txt', 'r')
s = open('schedule_info.txt', 'r')

if (s.read() != data.read()):
    with open('E:/Platon_PDF/new_bot/schedule_info.txt', 'w') as file:
        file.write(open('data.txt').read())



platon = Workers('270491271')

lesson = platon.schedule()
print(type(lesson))
for lessons in platon.schedule():
    day=lesson[lessons]['day']
    print(day)
'''