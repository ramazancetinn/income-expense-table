from wtforms import Form, StringField,FileField, TextAreaField, SubmitField, PasswordField, validators, FileField, IntegerField, DateField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Regexp
import logging

logger = logging.getLogger('gunicorn.info')
logger.setLevel('INFO')

class ResetPasswordForm(Form):
    logger.info('ResetPasswordForm class is processing')
    password = PasswordField('Password', [DataRequired(),validators.Length(min=6,max=25),
        EqualTo('confirm', message='Passwords do not match')])
    confirm = PasswordField('Confirm Password',[DataRequired()])
    submit = SubmitField('Reset Password')

class RequestResetForm(Form):
    logger.info('RequestResetForm class is processing')
    email = StringField('Email', [DataRequired(), Email(), validators.Length(min=6, max=50)])
    submit = SubmitField('Request Password Reset')


# Register Form Class
class RegisterForm(Form):
    logger.info('RegisterForm class is processing')

    company_name = StringField('İşletme Adı:', [validators.Length(min=1, max=20,message="İşletme adınız 1 ile 20 arasında karakterden oluşmalıdır.")])

    username = StringField('Kullanıcı Adı', [validators.Length(min=4, max=25,message="Kullanıcı adınız 4 ile 25 arasında karakterden oluşmalıdır.")])
    email = StringField('E-Mail Adresi', [Email(), validators.Length(min=4, max=50,message="E-mail adresiniz 4 ile 50 arasında karakterden oluşmalıdır.")])
    password = PasswordField('Şifre', [
        validators.DataRequired(),validators.Length(min=6,max=25,message="Şifreniz 4 ile 25 arasında karakterden oluşmalıdır."),
        EqualTo('confirm', message='Şifreler uyuşmuyor')])
    confirm = PasswordField('Şifre (Tekrar)',[DataRequired()])


# Register Form Class
class LoginForm(Form):
    logger.info('LoginForm class is processing')
    username = StringField('Kullanıcı Adı:', [DataRequired()])
    password = PasswordField('Şifre:', [DataRequired()])