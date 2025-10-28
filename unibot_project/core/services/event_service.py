from django.utils import timezone
from datetime import datetime
from ..models import Event

class EventService:
    @staticmethod
    def list_events(from_date=None, to_date=None):
        events = Event.objects.all()
        if from_date:
            from_dt = datetime.fromisoformat(from_date.replace('Z', '+00:00'))
            events = events.filter(start_date__gte=from_dt)
        if to_date:
            to_dt = datetime.fromisoformat(to_date.replace('Z', '+00:00'))
            events = events.filter(end_date__lte=to_dt) if to_date else events.filter(start_date__lte=to_dt)
        return list(events.values('id', 'title', 'start_date', 'end_date', 'location', 'description', 'created_at'))

    @staticmethod
    def create_event(data):
        try:
            event = Event.objects.create(
                title=data['title'],
                start_date=datetime.fromisoformat(data['start_date'].replace('Z', '+00:00')),
                end_date=datetime.fromisoformat(data['end_date'].replace('Z', '+00:00')) if data.get('end_date') else None,
                location=data.get('location', ''),
                description=data.get('description', '')
            )
            return event
        except ValueError as e:
            raise ValueError(f"Invalid date: {e}")

    @staticmethod
    def update_event(id, data):
        try:
            event = Event.objects.get(id=id)
            if 'title' in data:
                event.title = data['title']
            if 'start_date' in data:
                event.start_date = datetime.fromisoformat(data['start_date'].replace('Z', '+00:00'))
            if 'end_date' in data:
                event.end_date = datetime.fromisoformat(data['end_date'].replace('Z', '+00:00')) if data['end_date'] else None
            if 'location' in data:
                event.location = data['location']
            if 'description' in data:
                event.description = data['description']
            event.save()
            return event
        except Event.DoesNotExist:
            return None

    @staticmethod
    def delete_event(id):
        try:
            event = Event.objects.get(id=id)
            event.delete()
            return True
        except Event.DoesNotExist:
            return False

