from datetime import datetime, timedelta


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
        """
        Generates a schedule and returns it along with the file name.

        Args:
            school_code (str): Unique school code for the file name.

        Returns:
            tuple: (list of schedule strings, file name)
        """
        schedule = []
        current_time = self.start_time
        for lesson in range(1, self.total_lessons + 1):
            lesson_in = current_time.strftime("%H:%M")
            current_time += self.lesson_duration
            lesson_out = current_time.strftime("%H:%M")

            schedule.append(f"{lesson_in} * * 1-5 bell.c in")
            schedule.append(f"{lesson_out} * * 1-5 bell.c out")

            if lesson < self.total_lessons:
                current_time += (
                    self.long_break
                    if lesson == self.long_break_after
                    else self.short_break
                )

        file_name = school_code
        return schedule, file_name
