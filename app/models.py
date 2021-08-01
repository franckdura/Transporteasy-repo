from flask_admin.contrib.pymongo import ModelView
from flask_wtf import FlaskForm
from wtforms import TextField,BooleanField,SubmitField,StringField,IntegerField
from wtforms.validators import DataRequired
from flask_admin.contrib.pymongo.filters import BasePyMongoFilter


class RatingForm(FlaskForm):
    rating = IntegerField('rating', validators=[DataRequired()], render_kw={
                          "placeholder": "So ?"})
    submit = SubmitField("Submit", render_kw={"placeholder": "Submit"})

class FilterSiteIndeed(BasePyMongoFilter):
    def apply(self, query,value):
        if value==1:

            return True

class RatingView(ModelView):

    column_list = ('user_id','rating')
    #column_filters = [FilterSiteIndeed(column =,name = '')]
    form = RatingForm
