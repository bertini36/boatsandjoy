import json

from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from boatsandjoy_api.bookings.api import api as bookings_api
from boatsandjoy_api.bookings.requests import (
    CreateBookingRequest,
    GetBookingRequest,
    MarkBookingAsErrorRequest,
    RegisterBookingEventRequest,
    GetBookingBySessionRequest,
)


@api_view(['GET'])
def generate_payment(request: Request) -> Response:
    api_request = GetBookingRequest(
        obj_id=request.GET['booking_id'],
        generate_new_session_id=True
    )
    results = bookings_api.get(api_request)
    return Response(results)


@api_view(['POST'])
def create_booking(request: Request) -> Response:
    """
    Creates a booking

    :return {
        'error': bool,
        'data': {
            'id': int,
            'created': datetime,
            'price': Decimal,
            'status': str,
            'session_id': str
        }
    }
    """
    data = json.loads(request.body)
    api_request = CreateBookingRequest(
        price=data['price'],
        slot_ids=[int(slot_id) for slot_id in data['slot_ids'].split(',')],
        customer_name=data['customer_name'],
        customer_telephone_number=data['customer_telephone_number'],
        extras=data['extras'],
    )
    results = bookings_api.create(api_request)
    return Response(results)


@api_view(['POST'])
def register_booking_event(request: Request) -> Response:
    api_request = RegisterBookingEventRequest(
        headers=request.META,
        body=json.loads(request.body)
    )
    response = bookings_api.register_event(api_request)
    if response['error']:
        return Response(status=400)
    return Response(status=200)


@api_view(['GET'])
def mark_booking_as_error(request: Request) -> Response:
    session_id = request.GET.get('session_id')
    results = None
    if session_id:
        api_request = MarkBookingAsErrorRequest(session_id=session_id)
        results = bookings_api.mark_as_error(api_request)
    return Response(results)


@api_view(['GET'])
def get_booking_by_session(request: Request) -> Response:
    session_id = request.GET.get('session_id')
    api_request = GetBookingBySessionRequest(session_id=session_id)
    results = bookings_api.get_booking_by_session(api_request)
    return Response(results)
