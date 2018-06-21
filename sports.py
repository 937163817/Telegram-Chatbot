import sports_py

sports = input('please input sport:')

matches = sports_py.get_sport_scores(sports)
for match in matches:
    print('{} vs {}: {}-{}'.format(match.home_team, match.away_team, match.home_score, match.away_score))