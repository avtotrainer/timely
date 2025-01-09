from datetime import datetime, timedelta

# import os


class ClassSchedule:
    def __init__(
        self,
        start_time="09:00",
        lesson_duration=45,
        short_break=5,
        long_break_after=2,
        long_break=10,
        total_lessons=7,
    ):
        self.start_time = datetime.strptime(start_time, "%H:%M")
        self.lesson_duration = timedelta(minutes=lesson_duration)
        self.short_break = timedelta(minutes=short_break)
        self.long_break_after = long_break_after
        self.long_break = timedelta(minutes=long_break)
        self.total_lessons = total_lessons

    def generate_schedule(self, school_code):
        schedule = []
        current_time = self.start_time
        for lesson in range(1, self.total_lessons + 1):
            lesson_in = current_time.strftime("%M %H")
            current_time += self.lesson_duration
            lesson_out = current_time.strftime("%M %H")

            schedule.append(f"{lesson_in} * *  1-5 sudo /home/tc/bell.c in")
            schedule.append(f"{lesson_out} * *  1-5 sudo /home/tc/bell.c out")

            if lesson < self.total_lessons:
                if lesson == self.long_break_after:
                    current_time += self.long_break
                else:
                    current_time += self.short_break

        file_name = school_code
        with open(file_name, "w") as file:
            for idx, entry in enumerate(schedule):
                if idx % 2 == 0:
                    file.write(f"\n# ᲒᲐᲙᲕᲔᲗᲘᲚᲘ {idx // 2 + 1}\n")
                file.write(entry + "\n")
        return file_name
