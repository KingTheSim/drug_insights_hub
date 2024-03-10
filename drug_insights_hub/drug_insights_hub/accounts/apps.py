from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'drug_insights_hub.accounts'

    def ready(self) -> None:
        import drug_insights_hub.accounts.signals
