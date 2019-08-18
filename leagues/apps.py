from django.apps import AppConfig


class LeaguesConfig(AppConfig):
    name = 'leagues'

    def ready(self):
        import leagues.signals