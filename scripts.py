import sys
from datacenter.models import Mark
from datacenter.models import Schoolkid
from datacenter.models import Chastisement
from datacenter.models import Lesson
from datacenter.models import Commendation
from random import choice


COMPLIMENTS = [
    'Молодец!',
    'Мы с тобой не зря поработали!',
    'Замечательно!',
    'Потрясающе!',
    'Ты меня очень обрадовал!',
    'Ты меня приятно удивил!',
    'Великолепно!',
    'Прекрасно!',
]


def get_schoolkid(kid_name):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=kid_name)
        return schoolkid
    except Schoolkid.DoesNotExist:
        print(f'\nУченики с именем "{kid_name}" не найдены\n')
        raise Schoolkid.DoesNotExist
    except Schoolkid.MultipleObjectsReturned:
        print(f'\nНайдено несколько учеников с именем "{kid_name}"\n')
        raise Schoolkid.MultipleObjectsReturned


def fix_marks(kid_name):
    """Исправление оценок ученика."""
    kid = get_schoolkid(kid_name)
    schoolkid_bad_marks = Mark.objects.filter(schoolkid=kid, points__in=[2,3])
    schoolkid_bad_marks.update(points=5)


def remove_chastisements(kid_name):
    """Удаление замечаний ученика."""
    kid = get_schoolkid(kid_name)
    chastisements = Chastisement.objects.filter(schoolkid=kid)
    chastisements.delete()


def create_commendation(kid_name, subject):
    """Создание похвалы от учителя."""
    schoolkid = get_schoolkid(kid_name)

    subject_lessons = Lesson.objects.filter(
        year_of_study = schoolkid.year_of_study,
        group_letter = schoolkid.group_letter,
        subject__title = subject,
    )

    last_lesson = subject_lessons.order_by('-date').first()

    if not last_lesson:
        print(f'\nУроки по предмету "{subject}" отсутствуют\n')
        return
    
    Commendation.objects.create(
        text = choice(COMPLIMENTS),
        created = last_lesson.date,
        schoolkid = schoolkid,
        subject = last_lesson.subject,
        teacher = last_lesson.teacher,
    )