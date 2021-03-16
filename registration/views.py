import json
import logging

import djstripe
import stripe
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView
from djstripe.models import Product

from .models import CustomUser

logger = logging.getLogger(__name__)


@method_decorator(login_required, name="dispatch")
class ProfilePage(View):
    """
    It displays the profile page after logging in.
    """

    def get(self, request, *args, **kwargs):

        if request.user.active_subscription:

            logger.info("User logged in successfully")
            return render(request, "subscription/subscriptioncomplete.html")

        context = {
            "products": Product.objects.all(),
            "publishable_key": settings.STRIPE_TEST_PUBLIC_KEY,
        }

        return render(request, "login/profile_page.html", context)


@method_decorator(login_required, name="dispatch")
class LogoutView(View):
    """
    View to perform logout action.
    """

    def get(self, request):
        logout(request)
        logger.info("User logged out successfully")
        return render(request, "logout/logout_page.html")


@method_decorator(login_required, name="dispatch")
class CreateSubscription(View):
    """
    This view is used for customer creation and subscription.
    """

    def post(self, request):

        data = json.loads(request.body)
        logger.info("Card Data")
        logger.info(data)
        payment_method = data["payment_method"]
        stripe.api_key = djstripe.settings.STRIPE_SECRET_KEY

        payment_method_obj = stripe.PaymentMethod.retrieve(payment_method)
        djstripe.models.PaymentMethod.sync_from_stripe_data(payment_method_obj)

        try:
            # This creates a new Customer and attaches the PaymentMethod in one API call.
            customer = stripe.Customer.create(
                payment_method=payment_method,
                email=request.user.email,
                invoice_settings={"default_payment_method": payment_method},
            )
            logger.info("Stripe customer created")
            djstripe_customer = djstripe.models.Customer.sync_from_stripe_data(customer)
            request.user.customer = djstripe_customer

            # At this point, associate the ID of the Customer object with your
            # own internal representation of a customer, if you have one.

            # Subscribe the user to the subscription created
            subscription = stripe.Subscription.create(
                customer=customer.id,
                items=[
                    {
                        "price": data["price_id"],
                    },
                ],
                trial_period_days=7,
                expand=["latest_invoice.payment_intent"],
            )
            logger.info("Stripe subscription created")
            djstripe_subscription = djstripe.models.Subscription.sync_from_stripe_data(
                subscription
            )
            request.user.active_subscription = True
            request.user.subscription = djstripe_subscription
            request.user.save()
            logger.info("Subscription for user marked active")
            return JsonResponse(subscription)

        except (KeyError, LookupError, TypeError, ValueError) as e:
            logger.error("Something got wrong while subscribing")
            logger.error(e)
            return JsonResponse({"error": (e.args[0])}, status=403)
        else:
            return HttpResponse("request method not allowed")


@method_decorator(login_required, name="dispatch")
class Complete(View):
    """
    This view render the template if subscription get completed.
    """

    def get(self, request):
        logger.info("Subscription and Payment successful")
        return render(request, "subscription/subscriptioncomplete.html")


@method_decorator(login_required, name="dispatch")
class UserSubscriptionPlan(View):
    """
    This view is to display the plan that user has selected
    """

    def get(self, request):

        logger.info("Displaying user's active plans")
        return render(request, "subscription/mysubscriptionplan.html")


@method_decorator(login_required, name="dispatch")
class CancelSubscription(View):
    """
    this view is used for cancelling customer subscription.
    """

    def get(self, request):

        sub_id = request.user.subscription.id
        stripe.api_key = djstripe.settings.STRIPE_SECRET_KEY

        try:
            request.user.active_subscription = False
            stripe.Subscription.delete(sub_id)
            request.user.save()
            logger.info("User subscription cancelled")
        except (LookupError, TypeError, ValueError) as e:
            logger.error("Subscription cancellation failed!")
            logger.error(e)
            return render(request, "subscription/nosubscriptionplans.html")

        return render(request, "subscription/subscriptioncancel.html")