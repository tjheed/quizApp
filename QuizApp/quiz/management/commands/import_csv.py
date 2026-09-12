import csv
from django.core.management.base import BaseCommand
from quiz.models import Topic, Question, Choice

class Command(BaseCommand):
    help = 'Import questions from a CSV file'

    def add_arguments(self, parser):
        # Allow the user to pass the CSV file path as an argument
        parser.add_argument('csv_file', type=str, help='The path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']

        try:
            with open(csv_file_path, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file, skipinitialspace=True)
                # reader = csv.reader(file)
                # Uncomment the next line if your CSV has a header row (like Topic, Question, etc.)
                # next(reader) 

                for row in reader:
                    topic_name = row[0].strip()
                    question_text = row[1].strip()
                    choices = [row[2].strip(), row[3].strip(), row[4].strip(), row[5].strip()]
                    correct_answer_index = int(row[6].strip()) - 1
                    
                    # Capture the explanation safely if it exists in the 8th column
                    explanation_text = row[7].strip() if len(row) > 7 else ""

                    topic, created = Topic.objects.get_or_create(name=topic_name)

                    question = Question.objects.create(
                        topic=topic,
                        text=question_text,
                        explanation=explanation_text
                    )

                    for index, choice_text in enumerate(choices):
                        Choice.objects.create(
                            question=question,
                            text=choice_text,
                            is_correct=(index == correct_answer_index)
                        )

                self.stdout.write(self.style.SUCCESS('Successfully imported all questions from CSV!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing CSV: {e}'))