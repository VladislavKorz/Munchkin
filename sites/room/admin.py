from django.contrib import admin
from .models import *

admin.site.register(Rooms)
admin.site.register(RoomPlayer)

@admin.register(PlayerLeavel)
class PlayerLevelAdmin(admin.ModelAdmin):
    list_display = ('player', 'leavel', 'create')
    list_filter = ('player__room', 'create',)
    search_fields = ('player__name',)

@admin.register(PlayerPower)
class PlayerPowerAdmin(admin.ModelAdmin):
    list_display = ('player', 'power', 'create')
    list_filter = ('player__room', 'create',)
    search_fields = ('player__name',)

@admin.register(PlayerClass)
class PlayerClassAdmin(admin.ModelAdmin):
    list_display = ('player', 'value', 'create')
    list_filter = ('player__room', 'create',)
    search_fields = ('player__name',)

@admin.register(PlayerRace)
class PlayerRaceAdmin(admin.ModelAdmin):
    list_display = ('player', 'value', 'create')
    list_filter = ('player__room', 'create',)
    search_fields = ('player__name',)

@admin.register(RoomBattle)
class RoomBattleAdmin(admin.ModelAdmin):
    list_display = ('monster', 'player', 'create', 'update')
    list_filter = ('create',)
    search_fields = ('player__name',)

@admin.register(RoomBattlePlayer)
class RoomBattlePlayerAdmin(admin.ModelAdmin):
    list_display = ('battle', 'player', 'power', 'create', 'update')
    list_filter = ('player__room', 'create',)
    search_fields = ('player__name',)


@admin.register(RoomBattleMonster)
class RoomBattleMonsterAdmin(admin.ModelAdmin):
    list_display = ('battle', 'leavel', 'power', 'create', 'update')
    list_filter = ('battle',)
    search_fields = ('battle__id',)
    ordering = ('-pk',)
