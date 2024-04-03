from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field: str = 'django.db.models.BigAutoField'
    name: str = 'drug_insights_hub.accounts'

    def ready(self) -> None:
        import drug_insights_hub.accounts.signals
