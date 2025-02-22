import random
from itertools import combinations
from collections import defaultdict

class Player:
    def __init__(self, name, gender, level):
        self.name = name
        self.gender = gender
        self.level = level
        self.appearances = 0  # 出场次数
        self.priority = 0  # 出场优先级（较高的优先考虑）

# 选手列表（可以修改）
players = [
    Player("星星", "女", 3),
    Player("老袁", "男", 5),
    Player("yc", "男", 4),
    Player("元元", "男", 4),
    Player("panjoy", "男", 4),
    Player("马大姐", "女", 4.5),
    Player("cc", "男", 5.5),
    Player("贾维斯", "男", 5.5),
    Player("程程", "女", 4),
    Player("遥远", "男", 3),
    Player("老麦", "男", 5),
    Player("vera", "女", 4),
]

def valid_pairing(team1, team2):
    """ 确保两个队伍的性别组合是相同的 """
    team1_males = sum(1 for p in team1 if p.gender == "男")
    team1_females = len(team1) - team1_males
    team2_males = sum(1 for p in team2 if p.gender == "男")
    team2_females = len(team2) - team2_males

    if (team1_males == 2 and team2_females == 2) or \
            (team1_females == 2 and team2_males == 2):
        return False
    return True  # ❌ 禁止 2 男 vs 2 女

haters = [{"yc", "遥远"}]
good_paris = [{"老袁", "贾维斯"}]
def match_in_history(history, x):
    all_pairs = [set([x[0][0][0].name, x[0][0][1].name]), set([x[0][1][0].name, x[0][1][1].name]), set([x[1][0][0].name, x[1][0][1].name]), set([x[1][1][0].name, x[1][1][1].name])]
    times = 0
    for pairs in all_pairs:
        if pairs in good_paris:
            times -= 200
        if pairs in haters:
            times += 200
        times += sum(1 for past in history if set(past) == pairs)
    return times

def generate_matchups(players):
    random.shuffle(players)
    history = []  # 记录历史对阵
    total_games = (len(players) * 7) // 8  # 确保每个人恰好出场 7 次
    index = 0
    chuchangcishu = 8

    while any(p.appearances < chuchangcishu for p in players):
        index += 1
        # 按照 出场次数（少的优先） 和 优先级（上一场没打优先） 排序
        players.sort(key=lambda p: (p.appearances, -p.priority))

        # 选择 8 名符合要求的选手
        available_players = [p for p in players if p.appearances < chuchangcishu]
        selected_players = available_players[:8]

        # 更新选手的优先级和出场次数
        for p in players:
            if p in selected_players:
                p.priority = -1  # 本轮已出场
                p.appearances += 1
            else:
                p.priority += 1  # 没出场的优先级增加

        # 组合所有可能的 (2+2) vs (2+2) 匹配方式
        valid_matches = []
        for team1 in combinations(selected_players, 2):
            remaining_players = [p for p in selected_players if p not in team1]
            for team2 in combinations(remaining_players, 2):
                other_players = [p for p in selected_players if p not in team1 and p not in team2]
                for team3 in combinations(other_players, 2):
                    team4 = tuple(p for p in selected_players if p not in team1 and p not in team2 and p not in team3)

                    # 确保性别匹配
                    if valid_pairing(team1, team2) and valid_pairing(team3, team4):
                        # 计算等级差
                        level1, level2 = sum(p.level for p in team1), sum(p.level for p in team2)
                        level3, level4 = sum(p.level for p in team3), sum(p.level for p in team4)
                        diff1, diff2 = abs(level1 - level2), abs(level3 - level4)
                        if diff1 <= 1 and diff2 <= 1:
                            # 记录匹配选项
                            valid_matches.append(((team1, team2), (team3, team4), diff1 + diff2))

        # 找到最优的匹配，尽量避免重复搭配
        valid_matches.sort(key=lambda x: match_in_history(history, x))

        # 选择最佳匹配
        best_match = valid_matches[0]
        history.append([best_match[0][0][0].name, best_match[0][0][1].name])
        history.append([best_match[0][1][0].name, best_match[0][1][1].name])
        history.append([best_match[1][0][0].name, best_match[1][0][1].name])
        history.append([best_match[1][1][0].name, best_match[1][1][1].name])

        # 输出本轮匹配
        (team1, team2), (team3, team4), diff = best_match
        print(f" 第{index}轮对阵安排：")
        print(f"  {2*index - 1} 左队 ({sum(p.level for p in team1)}) : {', '.join(p.name for p in team1)} vs 右队 ({sum(p.level for p in team2)}) : {', '.join(p.name for p in team2)}")
        print(f"  {2*index} 左队 ({sum(p.level for p in team3)}) : {', '.join(p.name for p in team3)} vs 右队 ({sum(p.level for p in team4)}) : {', '.join(p.name for p in team4)}")
        print("-" * 50)

if __name__ == "__main__":
    generate_matchups(players)
