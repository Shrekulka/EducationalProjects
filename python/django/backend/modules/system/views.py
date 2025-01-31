# backend/modules/system/views.py

from typing import Any, Dict

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, \
    PasswordResetConfirmView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views.generic import DetailView, UpdateView, CreateView, View, TemplateView

from .forms import UserRegisterForm, UserLoginForm, UserPasswordChangeForm, UserForgotPasswordForm, \
    UserSetNewPasswordForm, UserUpdateForm, ProfileUpdateForm, FeedbackCreateForm
from .models import Profile, Feedback
from ..services.mixins import UserIsNotAuthenticated
from ..services.tasks import send_activate_email_message_task, send_contact_email_message_task
from ..services.utils import get_client_ip

User = get_user_model()


########################################################################################################################
class UserRegisterView(UserIsNotAuthenticated, CreateView):
    """
       Представление регистрации нового пользователя на сайте.

       Наследуется от UserIsNotAuthenticated и CreateView.

       Атрибуты:
           form_class (UserRegisterForm): Форма регистрации нового пользователя.
           success_url (str): URL-адрес, на который перенаправляется пользователь после успешной регистрации.
           template_name (str): Имя шаблона, используемого для отображения формы регистрации.

       Методы:
           get_context_data(**kwargs) -> Dict[str, Any]: Возвращает контекстные данные для шаблона.
           form_valid(self, form) -> HttpResponseRedirect: Обрабатывает успешную отправку формы регистрации.
    """

    # Определяем форму для регистрации нового пользователя

    form_class = UserRegisterForm
    # URL-адрес, на который перенаправляется пользователь после успешной регистрации
    success_url = reverse_lazy('home')
    # Имя шаблона, используемого для отображения формы регистрации
    template_name = 'system/registration/user_register.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
            Возвращает контекстные данные для шаблона.

            Аргументы:
                **kwargs: Дополнительные именованные аргументы.

            Возвращает:
                Dict[str, Any]: Словарь контекстных данных для шаблона.
        """
        # Получаем контекстные данные от родительского класса
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст заголовок страницы
        context['title'] = 'Регистрация на сайте'
        context['RECAPTCHA_PUBLIC_KEY'] = settings.RECAPTCHA_PUBLIC_KEY
        return context

    def form_valid(self, form: UserRegisterForm) -> HttpResponseRedirect:
        """
            Обрабатывает успешную отправку формы регистрации пользователя.

            Аргументы:
                form (UserRegisterForm): Форма регистрации нового пользователя.

            Возвращает:
                HttpResponseRedirect: Перенаправление на страницу подтверждения отправки письма.

            Действия:
                - Сохраняет данные пользователя из формы, устанавливая его как неактивного.
                - Запускает задачу Celery для отправки письма активации.
                - Перенаправляет пользователя на страницу подтверждения отправки письма.
        """
        # Создаем нового пользователя, но не сохраняем его в базе данных
        user = form.save(commit=False)
        # Устанавливаем пользователя как неактивного (требуется подтверждение email)
        user.is_active = False
        # Сохраняем пользователя в базе данных
        user.save()

        # Запускаем задачу Celery для отправки письма активации асинхронно
        send_activate_email_message_task.delay(user.id)

        # Перенаправляем пользователя на страницу подтверждения отправки письма
        return redirect('email_confirmation_sent')


########################################################################################################################
class UserConfirmEmailView(View):
    """
    Представление для подтверждения email пользователя.

    Методы:
        get(self, request, uidb64, token) -> HttpResponseRedirect: Обрабатывает GET-запрос для подтверждения email.
    """

    def get(self, request, uidb64, token):
        """
        Обрабатывает GET-запрос для подтверждения email.

        Аргументы:
            request (HttpRequest): Объект HTTP-запроса.
            uidb64 (str): Зашифрованный идентификатор пользователя в base64.
            token (str): Токен для подтверждения.

        Возвращает:
            HttpResponseRedirect: Перенаправление на соответствующую страницу в зависимости от результата подтверждения.
        """
        try:
            # Декодируем идентификатор пользователя из base64
            uid = force_str(urlsafe_base64_decode(uidb64))
            # Получаем объект пользователя по идентификатору
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            # Если произошла ошибка при декодировании или пользователь не найден, устанавливаем None
            user = None

        # Если пользователь найден и токен действителен
        if user is not None and default_token_generator.check_token(user, token):
            # Активируем пользователя
            user.is_active = True
            user.save()
            # Авторизуем пользователя в системе
            login(request, user)
            # Перенаправляем на страницу подтверждения email
            return redirect('email_confirmed')
        else:
            # Перенаправляем на страницу ошибки подтверждения email
            return redirect('email_confirmation_failed')


########################################################################################################################
class EmailConfirmationSentView(TemplateView):
    """
        Представление для отображения страницы подтверждения отправки письма.

        Атрибуты:
            template_name (str): Имя шаблона для отображения страницы.

        Методы:
            get_context_data(**kwargs) -> Dict[str, Any]: Возвращает контекстные данные для шаблона.
    """
    # Имя шаблона для отображения страницы с сообщением об успешной отправке письма
    template_name = 'system/registration/email_confirmation_sent.html'

    def get_context_data(self, **kwargs):
        """
            Возвращает контекстные данные для шаблона.

            Аргументы:
                **kwargs: Дополнительные именованные аргументы.

            Возвращает:
                Dict[str, Any]: Словарь контекстных данных для шаблона.
        """
        context = super().get_context_data(**kwargs)
        # Ваш код для добавления дополнительных данных в контекст
        return context


########################################################################################################################
class EmailConfirmedView(TemplateView):
    """
    Представление для отображения страницы подтверждения email.

    Атрибуты:
        template_name (str): Имя шаблона для отображения страницы.

    Методы:
        get_context_data(**kwargs) -> Dict[str, Any]: Возвращает контекстные данные для шаблона.
    """
    # Имя шаблона для отображения страницы подтверждения email
    template_name = 'system/registration/email_confirmed.html'

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        """
        Возвращает контекстные данные для шаблона.

        Аргументы:
            **kwargs: Дополнительные именованные аргументы.

        Возвращает:
            Dict[str, Any]: Словарь контекстных данных для шаблона.
        """
        # Получаем контекстные данные от родительского класса
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст заголовок страницы
        context['title'] = 'Ваш электронный адрес активирован'
        return context


########################################################################################################################
class EmailConfirmationFailedView(TemplateView):
    """
        Представление для отображения страницы ошибки подтверждения email.

        Атрибуты:
            template_name (str): Имя шаблона для отображения страницы.

        Методы:
            get_context_data(**kwargs) -> Dict[str, Any]: Возвращает контекстные данные для шаблона.
    """
    # Имя шаблона для отображения страницы ошибки подтверждения email
    template_name = 'system/registration/email_confirmation_failed.html'

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        """
            Возвращает контекстные данные для шаблона.

            Аргументы:
                **kwargs: Дополнительные именованные аргументы.

            Возвращает:
                Dict[str, Any]: Словарь контекстных данных для шаблона.
        """
        # Получаем контекстные данные от родительского класса
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст заголовок страницы
        context['title'] = 'Ваш электронный адрес не активирован'
        return context


########################################################################################################################
class UserLoginView(SuccessMessageMixin, LoginView):
    """
        Представление авторизации пользователя на сайте.

        Наследуется от SuccessMessageMixin и LoginView.

        Атрибуты:
            form_class (UserLoginForm): Форма авторизации пользователя.
            template_name (str): Имя шаблона, используемого для отображения формы авторизации.
            next_page (str): URL-адрес, на который перенаправляется пользователь после успешной авторизации.
            success_message (str): Сообщение, отображаемое после успешной авторизации.

        Методы:
            get_context_data(**kwargs): Возвращает контекстные данные для шаблона.
    """

    # Определяем форму для авторизации пользователя
    form_class = UserLoginForm
    # Имя шаблона, используемого для отображения формы авторизации
    template_name = 'system/registration/user_login.html'
    # URL-адрес, на который перенаправляется пользователь после успешной авторизации
    next_page = 'home'
    # Сообщение, отображаемое после успешной авторизации
    success_message = 'Добро пожаловать на сайт!'

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        """
            Возвращает контекстные данные для шаблона.

            Аргументы:
                **kwargs: Дополнительные именованные аргументы.

            Возвращает:
                Dict[str, Any]: Словарь контекстных данных для шаблона.
        """
        # Получаем контекстные данные от родительского класса
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст заголовок страницы
        context['title'] = 'Авторизация на сайте'
        return context


########################################################################################################################
class UserLogoutView(LogoutView):
    """
        Представление выхода пользователя с сайта.

        Это представление наследуется от `LogoutView` и обрабатывает процесс выхода
        пользователя из системы. После выхода, пользователь перенаправляется на главную страницу.

        Атрибуты:
            next_page (str): URL для перенаправления пользователя после успешного выхода из системы.

        Методы:
            dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
                Обрабатывает HTTP-запрос и проверяет аутентификацию пользователя.
                Если пользователь уже вышел из системы, перенаправляет на главную страницу.
    """
    # Определяем URL для перенаправления после выхода из системы
    next_page = reverse_lazy('home')

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """
            Обрабатывает HTTP-запрос и проверяет аутентификацию пользователя.

            Переопределяет метод dispatch родительского класса `LogoutView`.
            Если пользователь уже вышел из системы, перенаправляет его на главную страницу.

            Аргументы:
                request (HttpRequest): Объект HTTP-запроса.
                *args (Any): Позиционные аргументы.
                **kwargs (Any): Именованные аргументы.

            Возвращает:
                HttpResponse: Объект HTTP-ответа. Если пользователь уже вышел из системы,
                происходит перенаправление на главную страницу. В противном случае,
                вызывается метод dispatch родительского класса для обработки запроса.
        """
        # Проверяем, аутентифицирован ли пользователь (вышел из системы или нет)
        if not request.user.is_authenticated:
            # Если пользователь не аутентифицирован, перенаправляем его на главную страницу
            return redirect(self.next_page)

        # Если пользователь аутентифицирован, вызываем метод dispatch родительского класса
        # для обработки запроса выхода из системы
        return super().dispatch(request, *args, **kwargs)


########################################################################################################################
class UserPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    """
        Представление для изменения пароля пользователя.

        Наследуется от SuccessMessageMixin и PasswordChangeView.

        Атрибуты:
            form_class (UserPasswordChangeForm): Форма для изменения пароля пользователя.
            template_name (str): Имя шаблона, используемого для отображения формы изменения пароля.
            success_message (str): Сообщение, отображаемое после успешного изменения пароля.

        Методы:
            get_context_data(**kwargs) -> Dict[str, Any]: Возвращает контекстные данные для шаблона.
            get_success_url() -> str: Возвращает URL-адрес для перенаправления после успешного изменения пароля.
    """

    # Определяем форму для изменения пароля пользователя
    form_class = UserPasswordChangeForm
    # Имя шаблона, используемого для отображения формы изменения пароля
    template_name = 'system/registration/user_password_change.html'
    # Сообщение, отображаемое после успешного изменения пароля
    success_message = 'Ваш пароль был успешно изменён!'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
            Возвращает контекстные данные для шаблона.

            Аргументы:
                **kwargs: Дополнительные именованные аргументы.

            Возвращает:
                Dict[str, Any]: Словарь контекстных данных для шаблона.
        """
        # Получаем контекстные данные от родительского класса
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст заголовок страницы
        context['title'] = 'Изменение пароля на сайте'
        return context

    def get_success_url(self) -> str:
        """
            Возвращает URL-адрес для перенаправления после успешного изменения пароля.

            Возвращает:
                str: URL-адрес страницы профиля текущего пользователя.
        """
        # Возвращаем URL-адрес страницы профиля текущего пользователя
        return reverse_lazy('profile_detail', kwargs={'slug': self.request.user.profile.slug})


########################################################################################################################
class UserForgotPasswordView(SuccessMessageMixin, PasswordResetView):
    """
        Представление для сброса пароля по электронной почте.

        Наследуется от PasswordResetView и добавляет сообщение об успешной отправке инструкции по восстановлению пароля.

        Атрибуты:
            form_class (Type[forms.Form]): Класс формы, используемой для запроса восстановления пароля.
            template_name (str): Путь к шаблону, используемому для отображения формы запроса восстановления пароля.
            success_url (str): URL для перенаправления после успешной отправки инструкции по восстановлению пароля.
            success_message (str): Сообщение, отображаемое после успешной отправки инструкции по восстановлению пароля.
            subject_template_name (str): Путь к шаблону, используемому для темы письма с инструкцией по восстановлению
                                         пароля.
            email_template_name (str): Путь к шаблону, используемому для тела письма с инструкцией по восстановлению
                                       пароля.
    """
    # Указываем класс формы, который будет использоваться для запроса на восстановление пароля
    form_class = UserForgotPasswordForm

    # Указываем путь к шаблону, который будет использоваться для отображения формы запроса на восстановление пароля
    template_name = 'system/registration/user_password_reset.html'

    # Указываем URL для перенаправления после успешной отправки инструкции по восстановлению пароля
    success_url = reverse_lazy('home')

    # Указываем сообщение об успешной отправке инструкции по восстановлению пароля
    success_message = 'Письмо с инструкцией по восстановлению пароля отправлено на ваш email'

    # Указываем путь к шаблону, который будет использоваться для темы письма с инструкцией по восстановлению пароля
    subject_template_name = 'system/email/password_subject_reset_mail.txt'

    # Указываем путь к шаблону, который будет использоваться для тела письма с инструкцией по восстановлению пароля
    email_template_name = 'system/email/password_reset_mail.html'

    def get_context_data(self, **kwargs: Any) -> dict:
        """
            Добавляет дополнительные данные в контекст.

            Аргументы:
                **kwargs: Дополнительные именованные аргументы.

            Возвращает:
                dict: Обновленный контекст данных.
        """
        # Получаем стандартный контекст данных от родительского класса
        context = super().get_context_data(**kwargs)
        # Добавляем заголовок страницы в контекст
        context['title'] = 'Запрос на восстановление пароля'
        return context


########################################################################################################################
class UserPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    """
        Представление для установки нового пароля после подтверждения.

        Наследуется от PasswordResetConfirmView и добавляет сообщение об успешной смене пароля.

        Атрибуты:
            form_class (Type[forms.Form]): Класс формы, используемой для установки нового пароля.
            template_name (str): Путь к шаблону, используемому для отображения формы установки нового пароля.
            success_url (str): URL для перенаправления после успешной смены пароля.
            success_message (str): Сообщение, отображаемое после успешной смены пароля.
    """
    # Указываем класс формы, который будет использоваться для установки нового пароля
    form_class = UserSetNewPasswordForm

    # Указываем путь к шаблону, который будет использоваться для отображения формы установки нового пароля
    template_name = 'system/registration/user_password_set_new.html'

    # Указываем URL для перенаправления после успешного изменения пароля
    success_url = reverse_lazy('home')

    # Указываем сообщение об успешной смене пароля, которое будет отображаться пользователю
    success_message = 'Пароль успешно изменен. Можете авторизоваться на сайте.'

    def get_context_data(self, **kwargs: Any) -> dict:
        """
            Добавляет дополнительные данные в контекст.

            Аргументы:
                **kwargs: Дополнительные именованные аргументы.

            Возвращает:
                dict: Обновленный контекст данных.
        """
        # Получаем стандартный контекст данных от родительского класса
        context = super().get_context_data(**kwargs)
        # Добавляем заголовок страницы в контекст
        context['title'] = 'Установить новый пароль'
        return context


########################################################################################################################
class ProfileDetailView(DetailView):
    """
       Представление для просмотра профиля.

       Атрибуты:
           model (Profile): Модель профиля.
           context_object_name (str): Имя переменной контекста, содержащей объект профиля.
           template_name (str): Имя шаблона для отображения профиля.
           queryset (QuerySet): Запрос для получения профиля с предварительно загруженными связанными объектами,
                                включая пользователей, подписчиков и подписки.
    """
    # Указываем модель, с которой работает представление
    model = Profile
    # Указываем имя переменной контекста, в которой будет доступен объект профиля в шаблоне
    context_object_name = 'profile'
    # Указываем имя шаблона, который будет использоваться для отображения профиля
    template_name = 'system/profile_detail.html'
    # Определяем запрос для получения профиля с предварительно загруженными связанными объектами
    queryset = model.objects.all().select_related('user').prefetch_related('followers', 'followers__user', 'following',
                                                                           'following__user')

    def get_context_data(self, **kwargs: Any) -> dict:
        """
            Добавляет заголовок страницы в контекст.

            Returns:
                dict: Контекст данных для шаблона.
        """
        # Получаем базовый контекст с помощью вызова метода get_context_data родительского класса
        context = super().get_context_data(**kwargs)
        # Добавляем заголовок страницы, содержащий имя пользователя, в контекст
        context['title'] = f'Страница пользователя: {self.object.user.username}'
        return context


########################################################################################################################
class ProfileUpdateView(UpdateView):
    """
        Представление для редактирования профиля.

        Атрибуты:
            model (Profile): Модель профиля.
            form_class (ProfileUpdateForm): Форма для обновления профиля.
            template_name (str): Имя шаблона для отображения формы редактирования профиля.
    """

    # Указываем модель, с которой работает представление
    model = Profile
    # Указываем класс формы, которая будет использоваться для редактирования профиля
    form_class = ProfileUpdateForm
    # Указываем имя шаблона, который будет использоваться для отображения формы редактирования профиля
    template_name = 'system/profile_edit.html'

    def get_object(self, queryset=None) -> Profile:
        """
            Получает объект профиля текущего пользователя.

            Returns:
                Profile: Объект профиля.
        """
        # Возвращает профиль текущего пользователя, используя атрибут request.user
        return self.request.user.profile

    def get_context_data(self, **kwargs: Any) -> dict:
        """
            Добавляет форму обновления данных пользователя в контекст.

            Args:
                **kwargs: Дополнительные аргументы.

            Returns:
                dict: Контекст данных для шаблона.
        """
        # Получаем базовый контекст с помощью вызова метода get_context_data родительского класса
        context = super().get_context_data(**kwargs)
        # Добавляем заголовок страницы, содержащий имя пользователя, в контекст
        context['title'] = f'Редактирование профиля пользователя: {self.request.user.username}'
        # Проверяем, были ли переданы данные POST (т.е. была отправлена форма)
        if self.request.POST:
            # Если данные POST были переданы, создаем экземпляр формы обновления данных пользователя
            context['user_form'] = UserUpdateForm(self.request.POST, instance=self.request.user)
        else:
            # Если данные POST не были переданы, создаем экземпляр формы обновления данных пользователя с текущим
            # пользователем
            context['user_form'] = UserUpdateForm(instance=self.request.user)
        return context

    def form_valid(self, form: ProfileUpdateForm) -> HttpResponse:
        """
            Обрабатывает валидную форму.

            Args:
                form (ProfileUpdateForm): Форма для обновления профиля.

            Returns:
                HttpResponse: Ответ сервера после успешного обновления профиля.
        """
        # Получаем контекст данных для шаблона
        context = self.get_context_data()
        # Получаем форму обновления данных пользователя из контекста
        user_form = context['user_form']
        # Начинаем транзакцию базы данных
        with transaction.atomic():
            # Проверяем, валидны ли формы обновления профиля и данных пользователя
            if all([form.is_valid(), user_form.is_valid()]):
                # Если обе формы валидны, сохраняем данные пользователя и профиля
                user_form.save()
                form.save()
            else:
                # Если хотя бы одна форма не валидна, обновляем контекст с информацией об ошибке
                context.update({'user_form': user_form})
                # Возвращаем страницу с формой, заполненной предыдущими данными и сообщением об ошибке
                return self.render_to_response(context)
        # Если все прошло успешно, вызываем метод form_valid родительского класса
        return super().form_valid(form)

    def get_success_url(self) -> str:
        """
            Получает URL для перенаправления после успешного обновления профиля.

            Returns:
                str: URL для перенаправления.
        """
        # Возвращает URL для перенаправления на страницу деталей профиля с учетом его slug
        return reverse_lazy('profile_detail', kwargs={'slug': self.object.slug})


########################################################################################################################
class FeedbackCreateView(SuccessMessageMixin, CreateView):
    """
       Представление для создания отзыва через контактную форму.

       Это представление на основе класса CreateView позволяет пользователям
       отправлять обратную связь через контактную форму. Оно также использует
       SuccessMessageMixin для отображения сообщения об успешной отправке формы.

       Атрибуты класса:
           model: Модель Feedback, связанная с этим представлением.
           form_class: Форма FeedbackCreateForm, которая будет использоваться для создания отзыва.
           success_message: Сообщение об успешной отправке.
           template_name: Шаблон для отображения формы.
           extra_context: Дополнительный контекст для шаблона.
           success_url: URL, на который будет выполнен редирект после успешной отправки формы.

       Методы:
           form_valid: Обрабатывает валидную форму.
    """
    model = Feedback  # Модель, связанная с этим представлением
    form_class = FeedbackCreateForm  # Форма, которая будет использоваться для создания отзыва
    success_message = 'Ваше письмо успешно отправлено администрации сайта'  # Сообщение об успешной отправке
    template_name = 'system/feedback.html'  # Шаблон для отображения формы
    extra_context = {'title': 'Контактная форма'}  # Дополнительный контекст для шаблона
    success_url = reverse_lazy('home')  # URL, на который будет выполнен редирект после успешной отправки формы

    def form_valid(self, form: FeedbackCreateForm) -> CreateView:
        """
            Обрабатывает валидную форму.

            Этот метод вызывается, когда форма успешно прошла валидацию.
            Он сохраняет объект отзыва, добавляет IP-адрес пользователя, и если
            пользователь аутентифицирован, сохраняет пользователя. Затем
            отправляется электронное письмо с данными отзыва.

            Аргументы:
                form (FeedbackCreateForm): Валидированная форма отзыва.

            Возвращает:
                HttpResponse: Ответ, перенаправляющий пользователя на success_url.
        """
        if form.is_valid():  # Проверяем, прошла ли форма валидацию
            feedback = form.save(commit=False)  # Сохраняем форму, но не отправляем ее в базу данных
            feedback.ip_address = get_client_ip(self.request)  # Получаем IP-адрес пользователя и сохраняем его в отзыв

            if self.request.user.is_authenticated:  # Если пользователь аутентифицирован
                feedback.user = self.request.user  # Сохраняем пользователя в отзыве

            # Отправляем электронное письмо с данными отзыва через Celery задачу
            send_contact_email_message_task.delay(
                feedback.subject,  # Передаем тему отзыва
                feedback.email,  # Передаем email отправителя отзыва
                feedback.content,  # Передаем содержимое отзыва
                feedback.ip_address,  # Передаем IP-адрес отправителя отзыва
                feedback.user_id  # Передаем идентификатор пользователя, если есть
            )

        return super().form_valid(form)  # Вызываем метод родительского класса для завершения обработки формы


########################################################################################################################
def tr_handler404(request: HttpRequest, exception: Exception) -> HttpResponse:
    """
        Обработка ошибки 404 (Страница не найдена)

        Эта функция обрабатывает ошибку 404, возникающую, когда пользователь пытается
        получить доступ к несуществующей странице. Она возвращает страницу с сообщением об ошибке.

        Аргументы:
        - request: HttpRequest объект, представляющий текущий запрос.
        - exception: Исключение, вызвавшее ошибку 404.

        Возвращает:
        - HttpResponse объект, содержащий отрендеренную страницу с сообщением об ошибке 404.
    """
    # Рендерим шаблон 'system/errors/error_page.html' с контекстом для ошибки 404
    return render(
        request=request,
        template_name='system/errors/error_page.html',
        status=404,
        context={
            'title': 'Страница не найдена: 404',  # Заголовок страницы ошибки
            'error_message': 'К сожалению такая страница была не найдена, или перемещена',  # Сообщение об ошибке
        }
    )


def tr_handler500(request: HttpRequest) -> HttpResponse:
    """
        Обработка ошибки 500 (Внутренняя ошибка сервера)

        Эта функция обрабатывает ошибку 500, возникающую в случае внутренней ошибки сервера.
        Она возвращает страницу с сообщением об ошибке.

        Аргументы:
        - request: HttpRequest объект, представляющий текущий запрос.

        Возвращает:
        - HttpResponse объект, содержащий отрендеренную страницу с сообщением об ошибке 500.
    """
    # Рендерим шаблон 'system/errors/error_page.html' с контекстом для ошибки 500
    return render(
        request=request,
        template_name='system/errors/error_page.html',
        status=500,
        context={
            'title': 'Ошибка сервера: 500',  # Заголовок страницы ошибки
            'error_message': 'Внутренняя ошибка сайта, вернитесь на главную страницу, отчет об ошибке мы направим администрации сайта',
            # Сообщение об ошибке
        }
    )


def tr_handler403(request: HttpRequest, exception: Exception) -> HttpResponse:
    """
        Обработка ошибки 403 (Доступ запрещен)

        Эта функция обрабатывает ошибку 403, возникающую, когда пользователь пытается
        получить доступ к странице, доступ к которой ограничен. Она возвращает страницу с сообщением об ошибке.

        Аргументы:
        - request: HttpRequest объект, представляющий текущий запрос.
        - exception: Исключение, вызвавшее ошибку 403.

        Возвращает:
        - HttpResponse объект, содержащий отрендеренную страницу с сообщением об ошибке 403.
    """
    # Рендерим шаблон 'system/errors/error_page.html' с контекстом для ошибки 403
    return render(
        request=request,
        template_name='system/errors/error_page.html',
        status=403,
        context={
            'title': 'Ошибка доступа: 403',  # Заголовок страницы ошибки
            'error_message': 'Доступ к этой странице ограничен',  # Сообщение об ошибке
        }
    )


########################################################################################################################
# Декоратор метода, который требует, чтобы пользователь был авторизован для доступа к данному представлению
@method_decorator(login_required, name='dispatch')
class ProfileFollowingCreateView(View):
    """
        Представление для создания и удаления подписки на пользователей.

        Этот класс позволяет текущему пользователю подписываться или отписываться
        от другого пользователя по его slug.

        Атрибуты:
            model (Type[Profile]): Модель профиля, используемая в представлении.

        Методы:
            is_ajax(self) -> bool:
                Проверяет, является ли запрос AJAX-запросом.

            post(self, request, slug) -> JsonResponse:
                Обрабатывает POST-запрос для создания или удаления подписки.

    """
    # Присваиваем переменной model класс модели Profile, который будет использоваться в текущем контексте
    model = Profile

    def is_ajax(self) -> bool:
        """
            Проверяет, является ли запрос AJAX-запросом.

            Returns:
                bool: True, если запрос является AJAX-запросом, иначе False.
        """
        # Проверяет, если в заголовках запроса присутствует заголовок 'X-Requested-With' с значением 'XMLHttpRequest'
        return self.request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    def post(self, request: HttpRequest, slug: str) -> JsonResponse:
        """
           Обрабатывает создание и удаление подписки на профиль пользователя.

           Метод получает профиль пользователя по slug и проверяет, является ли
           текущий пользователь уже подписчиком этого профиля. Затем он добавляет
           или удаляет подписку соответственно.

           Args:
               request (HttpRequest): Объект запроса.
               slug (str): Уникальный идентификатор профиля пользователя.

           Returns:
               JsonResponse: JSON-ответ с информацией о результате операции.

           Ответ содержит:
               - Информацию о пользователе, создающем или удаляющем подписку.
               - Сообщение о результате операции.
               - Флаг состояния для обновления пользовательского интерфейса.
        """
        # Получаем профиль пользователя, на которого подписываемся или отписываемся, по его slug
        user = self.model.objects.get(slug=slug)

        # Получаем профиль текущего пользователя
        profile = request.user.profile

        # Проверяем, если текущий пользователь уже подписан на этого пользователя
        if profile in user.followers.all():
            # Если подписан, удаляем из подписчиков
            user.followers.remove(profile)
            message = f'Подписаться на {user}'
            status = False

        # Если не подписан, добавляем в подписчики
        else:
            user.followers.add(profile)
            message = f'Отписаться от {user}'
            status = True

        # Формируем данные для ответа в формате JSON
        data = {
            'username': profile.user.username,  # Имя пользователя текущего профиля
            'get_absolute_url': profile.get_absolute_url(),  # URL текущего профиля
            'slug': profile.slug,  # Slug текущего профиля
            'avatar': profile.get_avatar,  # Аватар текущего профиля
            'message': message,  # Сообщение о результате операции
            'status': status,  # Статус подписки (подписан или нет)
        }

        # Возвращаем данные в формате JSON с HTTP-статусом 200 (OK)
        return JsonResponse(data, status=200)
########################################################################################################################
