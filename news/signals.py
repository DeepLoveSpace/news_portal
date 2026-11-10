from django.contrib.auth.models import Group, User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed, post_save, post_migrate
from django.dispatch import receiver
from .models import PostCategory


@receiver(m2m_changed, sender=PostCategory)
def post_created(sender, instance, **kwargs):
    if kwargs['action'] != 'post_add':
        return

    emails = User.objects.filter(
        subscriptions__category__in=instance.category.all()
    ).values_list('email', flat=True)

    subject = f'Новый пост в категории {",".join([cat.name for cat in instance.category.all()])}'

    text_content = (
        f'Заголовок поста: {instance.title}\n'
        f'Ссылка на пост: http://127.0.0.1:8000{instance.get_absolute_url()}'
    )
    html_content = (
        f'Заголовок поста: {instance.title}<br>'
        f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
        f'Ссылка на пост</a>'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()


@receiver(post_migrate)
def create_groups(sender, **kwargs):
    if sender.name == 'news':
        Group.objects.get_or_create(name='common')
        Group.objects.get_or_create(name='authors')


@receiver(post_save, sender=User)
def add_to_common_group(sender, instance, created, **kwargs):
    if created:
        common_group, _ = Group.objects.get_or_create(name='common')
        instance.groups.add(common_group)