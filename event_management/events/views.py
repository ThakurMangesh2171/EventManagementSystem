import logging
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from .models import Event, CustomUser
from .serializers import EventSerializer, UserSerializer
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .customException import EventExistsError,EventNotFoundException,UserNotFoundException
import uuid

# Configure the logger
logger = logging.getLogger(__name__)


@csrf_exempt
@require_http_methods(["POST"])
def create_event(request):
    logger.info("hit the API")

    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = EventSerializer(data=data)

        if serializer.is_valid():
            logger.info("Valid serializer")

            event_id = data.get('event_id')
            title = data.get('title')
            description = data.get('description')
            date = data.get('date')
            time = data.get('time')
            location = data.get('location')
            organizer = data.get('organizer')

            if event_id is None:
                logger.info("Creating event")
                response = save_event(title, description, date, time, location, organizer)
            else:
                logger.info(f"Updating event with event_id: {event_id}")
                response = update_event(event_id, title, description, date, time, location, organizer)

            return JsonResponse(response)

        else:
            logger.warning('Invalid data for create_event API')
            return JsonResponse({'errors': serializer.errors}, status=400)

    logger.warning('Invalid request method for create_event API')
    return JsonResponse({'error': 'Invalid request method for create_event API'}, status=400)


def get_organizer(user_id):
    try:
        logger.info(f"Getting customer info from Db: {user_id}")
        return CustomUser.objects.get(user_id=user_id)
    except CustomUser.DoesNotExist:
        logger.error('Organizer does not exist')
        return None


def save_event(title, description, date, time, location, organizer):
    try:
        logger.info("Creating event")
        user_id = organizer

        organizer_obj = get_organizer(user_id)
        if organizer_obj is None:
            # return {'message': 'Organizer does not exist'}, status=400
            raise UserNotFoundException("User not found with user_id:", user_id)

        event_id = 2  # You might want to generate a unique event_id here

        Event.objects.create(
            event_id=event_id,
            title=title,
            description=description,
            date=date,
            time=time,
            location=location,
            organizer=organizer_obj
        )

        logger.info("Event created successfully")
        return {'message': 'Event created successfully'}

    except Exception as e:
        logger.error(f"Error creating event: {e}")
        return {'message': 'Error creating event'}


def update_event(event_id, title, description, date, time, location, organizer):
    try:
        logger.info(f"Updating event with event_id: {event_id}")
        event = Event.objects.get(event_id=event_id)

    except Event.DoesNotExist:
        logger.warning(f"Event does not exist with event_id: {event_id}")
        # return {'message': f'Event does not exist with event_id: {event_id}'}, status=400
        raise EventNotFoundException("Event does not exist with event_id",event_id)

    try:
        organizer_obj = get_organizer(organizer)
        if organizer_obj is None:
            # return {'message': 'Organizer does not exist'}, status=400
            raise UserNotFoundException("User not found with user_id",organizer)

        event.title = title
        event.description = description
        event.date = date
        event.time = time
        event.location = location
        event.organizer = organizer_obj
        event.save()

        logger.info("Event updated successfully")
        return {'message': 'Event updated successfully'}

    except Exception as e:
        logger.error(f"Error updating event: {e}")
        return {'message': 'Error updating event'}





@csrf_exempt
@require_http_methods(["POST"])
def create_user(request):
    logger.info("Creating user")

    data = JSONParser().parse(request)
    serializer = UserSerializer(data=data)

    if serializer.is_valid():
        custom_user = CustomUser(
            password=data.get('password'),
            last_login=data.get('last_login'),
            is_superuser=data.get('is_superuser'),
            username=data.get('username'),
            first_name=data.get('first_name'),
            email=data.get('email'),
            is_staff=data.get('is_staff'),
            is_active=data.get('is_active'),
            date_joined=data.get('date_joined'),
            user_id=data.get('user_id'),
            last_name=data.get('last_name'),
            phone_number=data.get('phone_number'),
            email_id=data.get('email_id'),
            address=data.get('address'),
        )

        custom_user.save()
        logger.info("User created successfully")
        return JsonResponse({'message': 'User created successfully'})
        
    else:
        logger.warning('Invalid data received')
        return JsonResponse({'errors': serializer.errors}, status=400)
