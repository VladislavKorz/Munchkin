# user - это экземпляр модели CustomUser


# сколько игр у пользователя
def get_games_count(user):
	return user.roomPlayer.all().count()


# дата последней игры
def last_game_date(user):
	return user.roomPlayer.order_by('create').last().update


# суммарный уровень по всем играм
def level_sum(user):
	return sum([ i.get_leavel() for i in user.roomPlayer.all()])


# скольк всего побед (10 уровней) у игрока
def get_victories(user):
	wins = sum([i.leavel.filter(leavel=10).count() for i in user.roomPlayer.all()])
	games = user.roomPlayer.all().count()
	try:
		return (wins/games)*100
	except ZeroDivisionError:
		return 0
