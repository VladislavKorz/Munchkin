# сколько игр у пользователя
def get_games_count(user):
	return user.roomPlayer.all().count()


# дата последней игры
def last_game_date(user):
	return user.roomPlayer.order_by('create').last().update


# суммарный уровень по всем играм
def level_sum(user):
	return sum([ i.get_leavel() for i in user.roomPlayer.all()])
