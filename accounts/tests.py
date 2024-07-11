from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.form import CustomUserRegistrationForm


CustomUser = get_user_model()


class CustomUserModelTest(TestCase):

    def setUp(self):
        self.student_user = CustomUser.objects.create_user(
            username='student_user',
            email='student@example.com',
            first_name='Student',
            last_name='User',
            status='student',
            password='testpassword123'
        )

        self.librarian_user = CustomUser.objects.create_user(
            username='librarian_user',
            email='librarian@example.com',
            first_name='Librarian',
            last_name='User',
            status='librarian',
            password='testpassword123'
        )

    def test_string_representation(self):
        self.assertEqual(str(self.student_user), 'student_user')
        self.assertEqual(str(self.librarian_user), 'librarian_user')

    def test_get_full_name(self):
        self.assertEqual(self.student_user.get_full_name(), 'Student User')
        self.assertEqual(self.librarian_user.get_full_name(), 'Librarian User')

    def test_can_add_book(self):
        self.assertFalse(self.student_user.can_add_book())
        self.assertTrue(self.librarian_user.can_add_book())

    def test_email_uniqueness(self):
        with self.assertRaises(ValidationError):
            duplicate_email_user = CustomUser(
                username='another_user',
                email='student@example.com',
                first_name='Another',
                last_name='User',
                status='student',
                password='testpassword123'
            )
            duplicate_email_user.full_clean()

    def test_default_user_photo(self):
        self.assertEqual(self.student_user.user_photo.name, 'default_photo.jpg')
        self.assertEqual(self.librarian_user.user_photo.name, 'default_photo.jpg')

    def test_user_status_default(self):
        new_user = CustomUser.objects.create_user(
            username='new_user',
            email='newuser@example.com',
            first_name='New',
            last_name='User',
            password='testpassword123'
        )
        self.assertEqual(new_user.status, 'student')

    def test_invalid_user_status(self):
        with self.assertRaises(ValidationError):
            invalid_status_user = CustomUser(
                username='invalid_user',
                email='invalid@example.com',
                first_name='Invalid',
                last_name='User',
                status='invalid_status',
                password='testpassword123'
            )
            invalid_status_user.full_clean()

    def test_username_uniqueness(self):
        with self.assertRaises(ValidationError):
            duplicate_username_user = CustomUser(
                username='student_user',
                email='anotheremail@example.com',
                first_name='Another',
                last_name='User',
                status='student',
                password='testpassword123'
            )
            duplicate_username_user.full_clean()


class RegisterViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('accounts:register')
        self.index_url = reverse('index')
        self.login_url = reverse('accounts:login')
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        }
        self.existing_user = CustomUser.objects.create_user(
            username='existing_user',
            email='existinguser@example.com',
            password='testpassword123'
        )

    def test_get_register_view_authenticated_user(self):
        self.client.login(username='existing_user', password='testpassword123')
        response = self.client.get(self.register_url)
        self.assertRedirects(response, self.index_url)

    def test_get_register_view_unauthenticated_user(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_post_register_view_authenticated_user(self):
        self.client.login(username='existing_user', password='testpassword123')
        response = self.client.post(self.register_url, data=self.user_data)
        self.assertRedirects(response, self.index_url)

    def test_post_register_view_invalid_form(self):
        invalid_data = self.user_data.copy()
        invalid_data['password2'] = 'differentpassword123'
        response = self.client.post(self.register_url, data=invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')
        self.assertFalse(CustomUser.objects.filter(username='testuser').exists())


class CustomUserRegistrationFormTest(TestCase):

    def setUp(self):
        self.existing_user = CustomUser.objects.create_user(
            username='existing_user',
            email='existinguser@example.com',
            password='testpassword123'
        )
        self.form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'Testpassword123!',
            'password2': 'Testpassword123!'
        }

    def test_form_valid(self):
        form = CustomUserRegistrationForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_due_to_existing_email(self):
        form_data = self.form_data.copy()
        form_data['email'] = 'existinguser@example.com'
        form = CustomUserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertEqual(form.errors['email'], ["A user with that email already exists."])

    def test_form_invalid_due_to_password_mismatch(self):
        form_data = self.form_data.copy()
        form_data['password2'] = 'Differentpassword123!'
        form = CustomUserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
        self.assertEqual(form.errors['password2'], ["The two password fields didn’t match."])

    def test_form_invalid_due_to_blank_first_name(self):
        form_data = self.form_data.copy()
        form_data['first_name'] = ''
        form = CustomUserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)
        self.assertEqual(form.errors['first_name'], ["This field is required."])

    def test_form_invalid_due_to_blank_last_name(self):
        form_data = self.form_data.copy()
        form_data['last_name'] = ''
        form = CustomUserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('last_name', form.errors)
        self.assertEqual(form.errors['last_name'], ["This field is required."])

    def test_form_invalid_due_to_short_password(self):
        form_data = self.form_data.copy()
        form_data['password1'] = 'Short1!'
        form_data['password2'] = 'Short1!'
        form = CustomUserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
        self.assertEqual(form.errors['password2'], ["This password is too short. It must contain at least 8 characters."])

    def test_form_invalid_due_to_invalid_email_format(self):
        form_data = self.form_data.copy()
        form_data['email'] = 'invalid-email'
        form = CustomUserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertEqual(form.errors['email'], ["Enter a valid email address."])

    def test_form_invalid_due_to_blank_username(self):
        form_data = self.form_data.copy()
        form_data['username'] = ''
        form = CustomUserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertEqual(form.errors['username'], ["This field is required."])

    def test_form_invalid_due_to_existing_username(self):
        form_data = self.form_data.copy()
        form_data['username'] = 'existing_user'
        form = CustomUserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertEqual(form.errors['username'], ["A user with that username already exists."])

    def test_form_invalid_due_to_invalid_username_characters(self):
        form_data = self.form_data.copy()
        form_data['username'] = 'invalid user!'
        form = CustomUserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertEqual(form.errors['username'], ["Username can only contain letters, numbers, and underscores."])

    def test_form_invalid_due_to_password_missing_digit(self):
        form_data = self.form_data.copy()
        form_data['password1'] = 'Testpassword!'
        form_data['password2'] = 'Testpassword!'
        form = CustomUserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
        self.assertEqual(form.errors['password2'], ["The password must contain at least one digit."])

    def test_form_invalid_due_to_password_missing_uppercase(self):
        form_data = self.form_data.copy()
        form_data['password1'] = 'testpassword123!'
        form_data['password2'] = 'testpassword123!'
        form = CustomUserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
        self.assertEqual(form.errors['password2'], ["The password must contain at least one uppercase letter."])

    def test_form_invalid_due_to_password_missing_lowercase(self):
        form_data = self.form_data.copy()
        form_data['password1'] = 'TESTPASSWORD123!'
        form_data['password2'] = 'TESTPASSWORD123!'
        form = CustomUserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
        self.assertEqual(form.errors['password2'], ["The password must contain at least one lowercase letter."])

    def test_form_invalid_due_to_password_missing_special_character(self):
        form_data = self.form_data.copy()
        form_data['password1'] = 'Testpassword123'
        form_data['password2'] = 'Testpassword123'
        form = CustomUserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
        self.assertEqual(form.errors['password2'], ["The password must contain at least one special character."])


class LoginViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.login_url = reverse('accounts:login')
        self.index_url = reverse('index')
        self.username = 'testuser'
        self.password = 'testpassword123'
        self.user = CustomUser.objects.create_user(username=self.username, password=self.password)

    def test_get_login_view_authenticated_user(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.login_url)
        self.assertRedirects(response, self.index_url)

    def test_get_login_view_unauthenticated_user(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_post_login_view_authenticated_user(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(self.login_url, data={})
        self.assertRedirects(response, self.index_url)

    def test_post_login_view_invalid_form(self):
        response = self.client.post(self.login_url, data={'username': self.username})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertIn('This field is required', response.content.decode())


class ProfileViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.profile_url = reverse('accounts:profile')
        self.login_url = reverse('accounts:login')
        self.username = 'testuser'
        self.password = 'testpassword123'
        self.user = CustomUser.objects.create_user(username=self.username, password=self.password)

    def test_get_profile_view_authenticated_user(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')

    def test_get_profile_view_unauthenticated_user(self):
        response = self.client.get(self.profile_url)
        self.assertRedirects(response, f'{self.login_url}?next={self.profile_url}')

    def test_get_profile_view_context_data(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'], self.user)
        self.assertEqual(response.context['user'].username, self.username)
        self.assertEqual(response.context['user'].email, self.user.email)


class ProfileEditTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.profile_edit_url = reverse('accounts:profile_edit')
        self.login_url = reverse('accounts:login')
        self.username = 'testuser'
        self.password = 'testpassword123'
        self.user = CustomUser.objects.create_user(username=self.username, password=self.password)

    def test_get_profile_edit_view_authenticated_user(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.profile_edit_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile_edit.html')

    def test_get_profile_edit_view_unauthenticated_user(self):
        response = self.client.get(self.profile_edit_url)
        self.assertRedirects(response, f'{self.login_url}?next={self.profile_edit_url}')

    def test_post_profile_edit_view_unauthenticated_user(self):
        response = self.client.post(self.profile_edit_url, data={'first_name': 'Updated', 'last_name': 'User'})
        self.assertRedirects(response, f'{self.login_url}?next={self.profile_edit_url}')

    def test_post_profile_edit_view_invalid_data(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(self.profile_edit_url, data={'first_name': '', 'last_name': 'Updated'})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'first_name', 'This field is required.')

    def test_post_profile_edit_view_with_invalid_image(self):
        self.client.login(username=self.username, password=self.password)
        invalid_image = SimpleUploadedFile("invalid_image.txt", b"file_content", content_type="text/plain")
        response = self.client.post(self.profile_edit_url, {'first_name': 'Updated', 'last_name': 'User', 'user_photo': invalid_image})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'user_photo', 'Upload a valid image. The file you uploaded was either not an image or a corrupted image.')

    def test_post_profile_edit_view_with_large_image(self):
        self.client.login(username=self.username, password=self.password)
        large_image = SimpleUploadedFile("large_image.jpg", b"file_content" * 1000000, content_type="image/jpeg")
        response = self.client.post(self.profile_edit_url, {'first_name': 'Updated', 'last_name': 'User', 'user_photo': large_image})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'user_photo', 'Upload a valid image. The file you uploaded was either not an image or a corrupted image.')

