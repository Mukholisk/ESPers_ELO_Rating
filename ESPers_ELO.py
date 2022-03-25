'''
ESPers StarCraft ELO Ranking
Made By Mukho
Start date: 2022-03-25 FRI
Last modified date: 2022-03-25 FRI

- Rating Calculation
- Sorting by rating point

- Head-to-head records
'''

#-*-coding: utf-8 -*-
import os
import csv

# sorting: rating
class user:
    '''Initializer'''
    # info = [name, race]
    # rank_and_rating = [rank, rating]
    # wins_and_loses = [wins, loses, win_rate]
    def __init__(self, info, rank_and_rating=[-1, 1000], wins_and_loses=[0, 0, 0.00]):
        self.name = info[0]
        self.race = info[1]
        self.rank = rank_and_rating[0]
        self.rating = rank_and_rating[1]
        self.wins = wins_and_loses[0]
        self.loses = wins_and_loses[1]
        self.win_rate = wins_and_loses[2]

    '''Getter'''
    def get_name(self):
        return self.name

    def get_race(self):
        return self.race
    
    def get_rank(self):
        return self.rank
    
    def get_rating(self):
        return self.rating

    def get_wins(self):
        return self.wins
    
    def get_loses(self):
        return self.loses
    
    def get_win_rate(self):
        return self.win_rate

    '''Setter'''
    def set_rank(self, ranking):
        self.rank = ranking
    
    def set_win_rate(self, win_rate):
        self.win_rate = win_rate

    def game_result(self, is_win):
        if is_win:
            self.wins += 1
        else:
            self.loses += 1
        
        if is_win == 0 and self.wins == 0:
            self.set_win_rate(0.0)
        else:
            self.set_win_rate(round(self.wins / (self.wins + self.loses) * 100, 2))

    # etc.
    def print_user(self):
        print("| Rank {:>2} | {:>3} | {:^7} | {:>6}pts  | {:>4} | {:>4} | {:>6}%  |".format(self.rank, self.name, self.race, self.rating, self.wins, self.loses, self.win_rate))

class Application:
    '''
    Auto Loading when the application starts
    Auto Saving when the application ends
    '''
    def __init__(self):
        # user = [ [name, race, rank, rating, wins, loses, win_rate], ..., [] ]
        self.data = []

    def run(self):
        '''Auto Loading'''
        self.load()

        while(1):
            num = self.get_commend()

            if num == 1:
                self.add_user()
            elif num == 2:
                self.delete_user()
            elif num == 3:
                self.enter_result()
            elif num == 4:
                self.print_ranking()
            elif num == 5:
                self.save()
            # elif num == 6:
            #     self.get_h2h_record()
            elif num == 0:
                '''Auto Saving'''
                print("------------------------------------")
                self.save()
                print("-- ● Good bye                     --")
                print("------------------------------------")
                break
            else:
                os.system("cls")
                print("------------------------------------")
                print("-- ● Incorrect Input.             --")

    def get_commend(self):
        print("------------------------------------")
        print("----     ESPers ELO Ranking     ----")
        print("-- 1. Add User                    --")
        print("-- 2. Delete User                 --")
        print("-- 3. Enter Result                --")
        print("-- 4. Print Ranking               --")
        print("-- 5. Save                        --")
        # print("-- 6. Get Head-to-Head Record     --")
        print("-- 0. Shutdown                    --")
        print("------------------------------------")
        try:
            cmd = int(input("-- Enter a command number: "))
            return cmd
        except:
            os.system("cls")
            print("------------------------------------")
            print("-- ● Incorrect Input.             --")

    def add_user(self):
        os.system("cls")
        print("------------------------------------")
        print("----          Add User          ----")
        print("------------------------------------")
        name = input("-- Name: ")
        race = input("-- Race(Zerg, Protoss, Terran): ")
        print("------------------------------------")

        if race not in ['Zerg', 'Protoss', 'Terran']:
            print("-- ● Incorrect race input .   --")
            return

        is_duplication = self.find_user(name, race)
        if is_duplication == -1:
            new_user = user([name, race])
            self.data.append(new_user)
            print("-- ● A new user has been added.   --")
        else:
            print("-- ● Cannot add duplicate user.   --")

    def delete_user(self):
        os.system("cls")
        if len(self.data) == 0:
            print("------------------------------------")
            print("-- ● Zero user in data.           --")
            return

        print("------------------------------------")
        print("----        Delete User         ----")
        print("------------------------------------")
        name = input("-- Name: ")
        race = input("-- Race(Zerg, Protoss, Terran): ")
        print("------------------------------------")

        is_found = self.find_user(name, race)
        if is_found != -1:
            del self.data[is_found]
            print("-- ● Delete successfully.         --")
        else:
            print("-- ● Cannot find user.            --")

    def enter_result(self):
        os.system("cls")
        if len(self.data) < 2:
            print("------------------------------------")
            print("-- ● Not enough users.            --")
            return

        print("------------------------------------")
        print("----        Enter Result        ----")
        print("------------------------------------")
        winner_name = input("-- Winner Name: ")
        winner_race = input("-- Winner Race(Zerg, Protoss, Terran): ")
        loser_name = input("-- Loser Name: ")
        loser_race = input("-- Loser Race(Zerg, Protoss, Terran): ")
        print("------------------------------------")

        winner = self.find_user(winner_name, winner_race)
        loser = self.find_user(loser_name, loser_race)
        if -1 in [winner, loser]:
            print("-- ● Incorrect user input.        --")
            return

        self.data[winner].game_result(1)
        self.data[loser].game_result(0)
        print("-- ● Result Update Complete.      --")

    def print_ranking(self):
        os.system("cls")
        if len(self.data) == 0:
            print("------------------------------------")
            print("-- ● No user.                     --")
            return

        print("-------------------------------------------------------------------")
        print("| Ranking |  Name  |  Race   |   Rating   |  Win | Lose | Win rate |")
        for i in range(len(self.data)):
            self.data[i].print_user()
        print("-------------------------------------------------------------------")

    def save(self):
        os.system("cls")
        try:
            with open("dataFile.csv", "w", encoding='utf-8-sig', newline='') as f:
                wr = csv.writer(f)
                # [name, race, rank, rating, wins, loses, win_rate]
                for i in range(len(self.data)):
                    wr.writerow([self.data[i].get_name(), self.data[i].get_race(), self.data[i].get_rank(), self.data[i].get_rating(), self.data[i].get_wins(), self.data[i].get_loses(), self.data[i].get_win_rate()])
                print("------------------------------------")
                print("-- ● Save Complete.               --")
        except:
            print("------------------------------------")
            print("-- ● Save Uncomplete.             --")

    def load(self):
        try:
            with open("dataFile.csv", "r", encoding='utf-8-sig') as f:
                rd = csv.reader(f)
                for item in rd:
                    # wins, loses -> int type
                    for i in range(4, 6):
                        item[i] = int(item[i])

                    info = [item[0], item[1]]
                    rank_and_rating = [item[2], item[3]]
                    win_and_loses = [item[4], item[5], item[6]]
                    u = user(info, rank_and_rating, win_and_loses)
                    self.data.append(u)
                print("------------------------------------")
                print("-- ● Load Complete.               --")
        except:
            print("------------------------------------")
            print("-- ● Load Uncomplete.             --")

    def find_user(self, name, race):
        for i in range(len(self.data)):
            if name == self.data[i].get_name() and race == self.data[i].get_race():
                return i
        return -1

# Main Process
app = Application()
app.run()