import sys
from datacenter.models import Mark
from datacenter.models import Schoolkid
from datacenter.models import Chastisement
from datacenter.models import Lesson
from datacenter.models import Commendation
from random import choice


def fix_marks(schoolkid: Schoolkid):
    """Исправление оценок ученика."""
    schoolkid_bad_marks = Mark.objects.filter(schoolkid=schoolkid, points__in=[2,3])
    schoolkid_bad_marks.update(points=5)


def remove_chastisements(schoolkid: Schoolkid):
    """Удаление замечаний ученика."""
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    chastisements.delete()


def create_commendation(kid_name, subject):
    """Создание похвалы от учителя."""
    compliments = [
        'Молодец!',
        'Мы с тобой не зря поработали!',
        'Замечательно!',
        'Потрясающе!',
        'Ты меня очень обрадовал!',
        'Ты меня приятно удивил!',
        'Великолепно!',
        'Прекрасно!',
    ]

    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=kid_name)
    except Schoolkid.DoesNotExist:
        print(f'Ученики с именем "{kid_name}" не найдены.')
        sys.exit(1)
    except Schoolkid.MultipleObjectsReturned:
        print(f'Найдено несколько учеников с именем "{kid_name}"')
        sys.exit(1)

    subject_lessons = Lesson.objects.filter(
        year_of_study = schoolkid.year_of_study,
        group_letter = schoolkid.group_letter,
        subject__title = subject,
    )

    last_lesson = subject_lessons.order_by('-date').first()
    
    Commendation.objects.create(
        text = choice(compliments),
        created = last_lesson.date,
        schoolkid = schoolkid,
        subject = last_lesson.subject,
        teacher = last_lesson.teacher,
    )