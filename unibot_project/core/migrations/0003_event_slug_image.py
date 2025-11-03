from django.db import migrations, models
from django.utils.text import slugify

def populate_event_slugs(apps, schema_editor):
    Event = apps.get_model('core', 'Event')
    used = set()
    # نمشي بترتيب ثابت عشان ما يصير تعارض
    for ev in Event.objects.all().order_by('created_at'):
        if not getattr(ev, 'slug', None):
            base = (slugify(ev.title)[:200] or 'event')
            cand = base
            i = 1
            # نضمن التفرد حتى لو فيه عناوين متشابهة
            while Event.objects.filter(slug=cand).exclude(pk=ev.pk).exists() or cand in used:
                i += 1
                cand = f"{base}-{i}"
            ev.slug = cand
            ev.save(update_fields=['slug'])
            used.add(cand)

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_knowledgebase'),
    ]

    operations = [
        # 1) نضيف الحقول - slug يسمح بالـ NULL مؤقتًا
        migrations.AddField(
            model_name='event',
            name='slug',
            field=models.SlugField(max_length=220, unique=True, db_index=True, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='image',
            field=models.ImageField(upload_to='events/', null=True, blank=True),
        ),
        # 2) نعبّي slugs للسجلات القديمة
        migrations.RunPython(populate_event_slugs, migrations.RunPython.noop),
        # 3) بعد التعبئة، نخلي slug غير قابل للـ NULL
        migrations.AlterField(
            model_name='event',
            name='slug',
            field=models.SlugField(max_length=220, unique=True, db_index=True, blank=True, null=False),
        ),
    ]
