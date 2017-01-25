import graphene
from graphene import AbstractType
from graphene import relay

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import SetPasswordForm
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode as uid_decoder

from kquotes.auth.decorators import login_required
from .nodes import UserNode


#class RegisterUser(relay.ClientIDMutation):
#    ok = graphene.Boolean()
#    user = graphene.Field(UserNode)
#
#    class Input:
#        username = graphene.String(required=True)
#        email = graphene.String(required=True)
#        password = graphene.String(required=True)
#        first_name = graphene.String()
#        last_name = graphene.String()
#
#    @classmethod
#    def mutate_and_get_payload(cls, input, context, info):
#        model = get_user_model()
#
#        username = input.pop('username')
#        email = input.pop('email')
#        password = input.pop('password')
#
#        user = model.objects.create_user(username, email, password, **input)
#        user.is_current_user = True
#
#        return RegisterUser(ok=True, user=user)


class LoginUser(relay.ClientIDMutation):
    """ Mutation to authenticate a user.

    Example

        Operation:
            mutation loginUser($input: LoginUserInput!) {
              loginUser(input: $input){
                ok,
                user {
                  username
                  firstName
                  lastName
                  email
                  token
                }
              }
            }

        Vars:

            {
              "input": {
                "username": "admin",
                "password": "123123"
              }
            }
    """
    ok = graphene.Boolean()
    user = graphene.Field(UserNode)

    class Input:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        params = {
            'username': input.get('username'),
            'password': input.get('password')
        }

        user = authenticate(**params)

        if user:
            user.is_current_user = True
            return LoginUser(ok=True, user=user)
        else:
            return LoginUser(ok=False, user=None)


class ResetPasswordRequest(relay.ClientIDMutation):
    ok = graphene.Boolean()

    class Input:
        email = graphene.String(required=True)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        data = {
            'email': input.get('email'),
        }

        reset_form = PasswordResetForm(data=data)

        if not reset_form.is_valid():
            raise Exception("The email is not valid")

        options = {
            'use_https': context.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': context
        }

        reset_form.save(**options)

        return ResetPasswordRequest(ok=True)


class ResetPassword(relay.ClientIDMutation):
    ok = graphene.Boolean()
    user = graphene.Field(UserNode)

    class Input:
        id = graphene.String(required=True)
        token = graphene.String(required=True)
        password = graphene.String(required=True)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        model = django.contrib.auth.get_user_model()

        try:
            uid = force_text(uid_decoder(input.get('id')))
            user = model.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, model.DoesNotExist):
            raise Exception('uid has an invalid value')

        data = {
            'uid': input.get('id'),
            'token': input.get('token'),
            'new_password1': input.get('password'),
            'new_password2': input.get('password')
        }

        reset_form = SetPasswordForm(user=user, data=data)

        if not reset_form.is_valid():
            raise Exception("The token is not valid")

        reset_form.save()

        return ResetPassword(ok=True, user=user)


class UpdateUser(relay.ClientIDMutation):
    ok = graphene.Boolean()
    result = graphene.Field(UserNode)

    class Input:
        username = graphene.String()
        email = graphene.String()
        password = graphene.String()
        current_password = graphene.String()
        first_name = graphene.String()
        last_name = graphene.String()

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, input, context, info):
        model = get_user_model()
        user = context.user
        user.is_current_user = True

        if not user.is_authenticated:
            raise Exception("You must be logged in to update renter profiles.")

        if 'password' in input:
            try:
                current_password = input.pop('current_password')
            except KeyError:
                raise Exception("Please provide your current password to change your password.")

            if user.check_password(current_password):
                user.set_password(input.pop('password'))
            else:
                raise Exception("Current password is incorrect.")

        for key, value in input.items():
            if not key is 'current_password':
                setattr(user, key, value)

        user.save()

        updated_user = model.objects.get(pk=user.pk)

        return UpdateUser(ok=True, result=updated_user)


class UsersMutation(AbstractType):
#    register_user = RegisterUser.Field()
    login_user = LoginUser.Field()
    reset_password_request = ResetPasswordRequest.Field()
    reset_password = ResetPassword.Field()
    update_user = UpdateUser.Field()
