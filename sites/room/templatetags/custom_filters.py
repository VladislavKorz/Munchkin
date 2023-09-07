from django import template
from room.models import Rooms

register = template.Library()

@register.filter
def get_room_levels(room):
        # Получите QuerySet всех player для комнаты room
    players = room.player.all()

    # Используйте генератор списка для получения всех связанных объектов leavel
    leavel_list = [leavel for player in players for leavel in player.leavel.all()]
    power_list = [power for player in players for power in player.power.all()]
    race_list = [playerRace for player in players for playerRace in player.playerRace.all()]
    class_list = [playerClass for player in players for playerClass in player.playerClass.all()]

    lst = leavel_list+power_list+race_list+class_list
    # Теперь leavel_list содержит все связанные объекты leavel для каждого player


    return lst


@register.filter
def get_item_type(item):
    model_name = type(item).__name__ # 'PlayerRace', 'PlayerPower' etc.
    return model_name


# {% if item|get_item_type == 'PlayerLeavel' %}
#     <div class="timeline">
#                     <div class="timeline-content">
#                         <span class="date">
#                             <span class="month">{{ item.create.time }}</span>
#                             <span class="year">{{ item.create.date|date:"d.m"  }}</span>
#                         </span>
#                         <h2 class="title" style="background: #02a2dd;"><span class="fa fa-chevron-up" aria-hidden="true"></span> {{ item.player.player.email }} теперь {{ item.leavel }} уровня
#                         </h2>
#                         <p class="description">Игрок {{ item.player.player.email }} изменил уровень</p>
#                     </div>
#                 </div>
# {% elif item|get_item_type == 'PlayerPower' %}
#     <div class="timeline">
#                     <div class="timeline-content">
#                         <span class="date">
#                             <span class="month">{{ item.create.time }}</span>
#                             <span class="year">{{ item.create.date|date:"d.m"  }}</span>
#                         </span>
#                         <h2 class="title" style="background: #02a2dd;"><span class="fa fa-chevron-up" aria-hidden="true"></span> {{ item.player.player.email }} теперь {{ item.power }} уровня
#                         </h2>
#                         <p class="description">Игрок {{ item.player.player.email }} изменил уровень</p>
#                     </div>
#                 </div>
# {% elif item|get_item_type == 'PlayerClass' %}
#     <div class="timeline">
#                     <div class="timeline-content">
#                         <span class="date">
#                             <span class="month">{{ item.create.time }}</span>
#                             <span class="year">{{ item.create.date|date:"d.m"  }}</span>
#                         </span>
#                         <h2 class="title" style="background: #02a2dd;"><span class="fa fa-chevron-up" aria-hidden="true"></span> {{ item.player.player.email }} теперь {{ item.value }} уровня
#                         </h2>
#                         <p class="description">Игрок {{ item.player.player.email }} изменил уровень</p>
#                     </div>
#                 </div>
# {% elif item|get_item_type == 'PlayerRace' %}
#     <div class="timeline">
#                     <div class="timeline-content">
#                         <span class="date">
#                             <span class="month">{{ item.create.time }}</span>
#                             <span class="year">{{ item.create.date|date:"d.m"  }}</span>
#                         </span>
#                         <h2 class="title" style="background: #02a2dd;"><span class="fa fa-chevron-up" aria-hidden="true"></span> {{ item.player.player.email }} теперь {{ item.value }} уровня
#                         </h2>
#                         <p class="description">Игрок {{ item.player.player.email }} изменил уровень</p>
#                     </div>
#                 </div>
# {% endif %}
