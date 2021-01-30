from dataclasses import asdict
from typing import Type

from django.conf import settings
from django.utils.translation import gettext_lazy as _

from boatsandjoy_api.boats.api import api as boats_api
from boatsandjoy_api.core.responses import (
    ErrorResponseBuilder,
    ResponseBuilder,
    ResponseBuilderInterface,
)
from boatsandjoy_api.core.utils import send_email
from .constants import BookingStatus
from .domain import Booking
from .exceptions import BookingsApiException
from .payment_gateways import PaymentGateway, StripePaymentGateway
from .repository import BookingsRepository, DjangoBookingsRepository
from .requests import (
    CreateBookingRequest,
    GetBookingRequest,
    MarkBookingAsErrorRequest,
    MarkBookingAsPaidRequest,
    RegisterBookingEventRequest,
)
from .validators import (
    BookingCreationRequestValidator,
    GetBookingRequestValidator,
    IdentifyBookingBySessionRequestValidator,
)
from ..boats.requests import FilterBoatsRequest


class BookingsApi:

    def __init__(
        self,
        bookings_repository: Type[BookingsRepository],
        response_builder: Type[ResponseBuilderInterface],
        error_builder: Type[ResponseBuilderInterface],
        payment_gateway: Type[PaymentGateway]
    ):
        self.bookings_repository = bookings_repository
        self.response_builder = response_builder
        self.error_builder = error_builder
        self.payment_gateway = payment_gateway

    def create(self, request: CreateBookingRequest):
        """
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
        try:
            BookingCreationRequestValidator.validate(request)
            purchase_details = self.bookings_repository.get_purchase_details(
                slot_ids=request.slot_ids,
                price=request.price
            )
            session_id = self.payment_gateway.generate_checkout_session_id(
                **purchase_details
            )
            booking = self.bookings_repository.create(
                **asdict(request),
                session_id=session_id
            )
            return self.response_builder(booking).build()

        except BookingsApiException as e:
            return self.error_builder(e).build()

    def get(self, request: GetBookingRequest):
        try:
            GetBookingRequestValidator.validate(request)
            request_dict = asdict(request)
            generate_new_session_id = request_dict.pop(
                'generate_new_session_id'
            )
            booking = self.bookings_repository.get(**request_dict)
            if generate_new_session_id:
                purchase_details = self.bookings_repository.get_purchase_details(
                    slot_ids=booking.slot_ids,
                    price=booking.price
                )
                session_id = self.payment_gateway.generate_checkout_session_id(
                    **purchase_details
                )
                booking = self.bookings_repository.update(
                    booking=booking,
                    session_id=session_id
                )
            return self.response_builder(booking).build()

        except BookingsApiException as e:
            return self.error_builder(e).build()

    def mark_as_paid(self, request: MarkBookingAsPaidRequest):
        try:
            IdentifyBookingBySessionRequestValidator.validate(request)
            booking = self.bookings_repository.get(**asdict(request))
            if booking.status != BookingStatus.CONFIRMED:
                self._send_payment_success_notification_email(booking)
            booking = self.bookings_repository.mark_as_paid(booking)
            api_request = FilterBoatsRequest(obj_id=booking.boat_id)
            results = boats_api.get(api_request)
            return self.response_builder({
                'booking': booking,
                'boat': results['data']
            }).build()

        except BookingsApiException as e:
            return self.error_builder(e).build()

    def mark_as_error(self, request: MarkBookingAsErrorRequest):
        try:
            IdentifyBookingBySessionRequestValidator.validate(request)
            booking = self.bookings_repository.get(**asdict(request))
            if booking.status != BookingStatus.CONFIRMED:
                self._send_payment_error_notification_email(booking)
            booking = self.bookings_repository.mark_as_error(booking)
            return self.response_builder(booking).build()

        except BookingsApiException as e:
            return self.error_builder(e).build()

    def register_event(self, request: RegisterBookingEventRequest):
        try:
            event = self.payment_gateway.register_event(
                headers=request.headers,
                body=request.body
            )
            session_id = self.payment_gateway.get_session_id_from_event(event)
            customer_email = self.payment_gateway.get_customer_email_from_event(
                event=event
            )
            booking = self.bookings_repository.get(session_id=session_id)
            booking = self.bookings_repository.update(
                booking=booking,
                customer_email=customer_email
            )
            self.send_confirmation_email(booking)
            return self.response_builder([]).build()

        except BookingsApiException as e:
            return self.error_builder(e).build()

    @staticmethod
    def send_confirmation_email(booking: Booking):
        if booking.customer_email:
            api_request = FilterBoatsRequest(obj_id=booking.boat_id)
            results = boats_api.get(api_request)
            send_email(
                subject=_('B&J: Booking confirmation'),
                to_email=booking.customer_email,
                from_email=settings.EMAIL_HOST_USER,
                template='emails/confirmation.html',
                booking=booking,
                boat=results['data'],
                EMAIL_HOST_USER=settings.EMAIL_HOST_USER
            )

    @staticmethod
    def _send_payment_success_notification_email(booking: Booking):
        """
        Email sent just for company information
        """
        if settings.EMAIL_HOST != 'localhost':   # Temporal
            send_email(
                subject=f'Booking {booking.locator} payment success',
                to_email=settings.EMAIL_HOST_USER,
                from_email=settings.EMAIL_HOST_USER,
                template='emails/payment_success_notification.html',
                booking=booking
            )

    @staticmethod
    def _send_payment_error_notification_email(booking: Booking):
        """
        Email sent just for company information
        """
        if settings.EMAIL_HOST != 'localhost':  # Temporal
            send_email(
                subject=f'Booking {booking.locator} payment error',
                to_email=settings.EMAIL_HOST_USER,
                from_email=settings.EMAIL_HOST_USER,
                template='emails/payment_error_notification.html',
                booking=booking
            )


api = BookingsApi(
    DjangoBookingsRepository,
    ResponseBuilder,
    ErrorResponseBuilder,
    StripePaymentGateway
)
