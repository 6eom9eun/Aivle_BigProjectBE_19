import csv
import os
from django.core.management.base import BaseCommand
from study.models import Word

class Command(BaseCommand):
    help = 'CSV파일 단어, 단어 뜻 DB 저장'

    def handle(self, *args, **kwargs):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        with open(os.path.join(BASE_DIR, 'words(add).csv'), 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                Word.objects.create(word=row[0], meaning=row[1])
        self.stdout.write(self.style.SUCCESS('Successfully populated words'))
