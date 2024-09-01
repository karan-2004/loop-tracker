from django.core.management.base import BaseCommand, CommandError
import csv
from django.apps import apps


class Command(BaseCommand):
    help = "Importing data from csv"

    def add_arguments(self, parser):
        parser.add_argument("model", nargs=1, type=str)
        parser.add_argument('file_path', nargs=1, type=str)

    def handle(self, *args, **options):
        self.model_name = options['model'][0]
        self.file_path = options['file_path'][0]
        self.model = self.get_model()
        self.main()

    def get_model(self):
        return apps.get_model(app_label='tracker', model_name=self.model_name)

    def main(self):
        self.stdout.write("importing data")

        with open(self.file_path, mode='r') as f:
            reader = csv.DictReader(f)
            for index, row_dict in enumerate(reader):
                try:
                    obj = self.model(**row_dict)
                    obj.save()

                except Exception as e:
                    self.stderr.write(f"{index} {e}")
                    break