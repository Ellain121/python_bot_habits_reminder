import sqlite3
import os
from datetime import datetime

project_path = os.path.dirname(os.path.realpath(__file__))


def daily_goal_to_str(daily_goal: int):
    if daily_goal == -1:
        return "Yes"
    else:
        return str(daily_goal)


class Habit:
    def __init__(self, id: int, name: str, daily_goal: int):
        self.id = id
        self.name = name
        self.daily_goal = daily_goal
        self.daily_result = 0


class DatabaseManager:
    def __init__(self):
        con = sqlite3.connect(project_path + "/data/habits.db")
        cur = con.cursor()
        res = cur.execute("SELECT id, name, dailyGoal FROM habits_id")
        db_habits = res.fetchall()

        self.habits = []
        for db_habit in db_habits:
            self.habits.append(Habit(*db_habit))

        res = cur.execute(
            f"SELECT id_{', id_'.join(str(habit.id) for habit in self.habits)} FROM habits_data WHERE date='{datetime.today().strftime('%Y-%m-%d')}'")
        daily_results = res.fetchall()[0]
        for i in range(len(daily_results)):
            self.habits[i].daily_result = daily_results[i]
            print(daily_results[i])

    def get_habits(self):
        return self.habits

    def get_habits_full_str(self):
        longest_len: int = 0
        longest_len_2: int = 0
        for habit in self.habits:
            if len(habit.name) > longest_len:
                longest_len = len(habit.name)
            if len(daily_goal_to_str(habit.daily_goal)) > longest_len_2:
                longest_len_2 = len(daily_goal_to_str(habit.daily_goal))

        str_list = str("`")
        for habit in self.habits:
            cur_len: int = len(habit.name)
            cur_len_2: int = len(daily_goal_to_str(habit.daily_goal))
            n_spaces: int = longest_len - cur_len + 1
            n_spaces_2: int = longest_len_2 - cur_len_2 + 1
            line = habit.name + " " * n_spaces + \
                "\| goal: " + daily_goal_to_str(habit.daily_goal) + " " * n_spaces_2 + \
                "\| result: " + str(habit.daily_result)
            str_list = str_list + line + "\n"
        str_list += "`"
        print(str_list)
        return str_list

    def get_habits_str(self):
        longest_len: int = 0
        for habit in self.habits:
            if len(habit.name) > longest_len:
                longest_len = len(habit.name)

        str_list = str("`")
        for habit in self.habits:
            cur_len: int = len(habit.name)
            n_spaces: int = longest_len - cur_len + 1
            line = habit.name + " " * n_spaces + \
                "\| goal: " + daily_goal_to_str(habit.daily_goal)
            str_list = str_list + line + "\n"
        str_list += "`"
        print(str_list)
        return str_list
