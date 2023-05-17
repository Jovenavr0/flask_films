from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, FileField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileAllowed, FileRequired


class MovieForm(FlaskForm):
    title = StringField(
        'Название фильма',
        validators=[DataRequired(message='Поле не должно быть пустым'),
                    Length(max=255, message='Введите название фильма до 255 символов')]
    )
    description = TextAreaField(
        'Описание',
        validators=[DataRequired(message='Поле не должно быть пустым')]
    )
    image = FileField(
        'Изображение',
        validators=[FileRequired(message='Поле не должно быть пустым'),
                    FileAllowed(['jpg', 'png', 'jpeg'], message='Неверный формат файла')]
    )
    submit = SubmitField('Добавить')


class ReviewForm(FlaskForm):
    name = StringField(
        'Имя автора',
        validators=[DataRequired(message='Поле не должно быть пустым'),
                    Length(max=255, message='Введите ваше имя длиной до 255 символов')]
    )
    text = TextAreaField(
        'Отзыв',
        validators=[DataRequired(message='Поле не должно быть пустым')]
    )
    score = SelectField(choices=[(i, i) for i in range(1, 11)])
    submit = SubmitField('Добавить отзыв')