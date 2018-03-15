from django.apps import AppConfig


class ReceiptsConfig(AppConfig):
    name = 'receipts'

    def ready(self):
    	# connect the signals for receipt
        import receipts.signals