from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, IntegerField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

class ProductForm(FlaskForm):
    title = StringField('产品标题',
                        validators=[DataRequired(), Length(min=2, max=255)])
    description = TextAreaField('产品介绍',
                                validators=[Optional(), Length(max=5000)])
    image_url = URLField('产品图片URL (选填)',
                         validators=[Optional(), Length(max=500)])
                         # Later, this could be FileField for uploads
    purchase_url = URLField('拿货地址 (选填)',
                            validators=[Optional(), Length(max=500)])
    purchase_price = DecimalField('拿货价格',
                                  validators=[DataRequired(), NumberRange(min=0)],
                                  default=0.00, places=2)
    selling_url = URLField('卖货地址 (选填)',
                           validators=[Optional(), Length(max=500)])
    selling_price = DecimalField('卖货价格',
                                 validators=[DataRequired(), NumberRange(min=0)],
                                 default=0.00, places=2)
    # Profit is calculated, so not in the form for direct input
    exposure = IntegerField('产品曝光量 (选填)',
                            validators=[Optional(), NumberRange(min=0)],
                            default=0)
    sales_count = IntegerField('出单数量 (选填)',
                               validators=[Optional(), NumberRange(min=0)],
                               default=0)
    submit = SubmitField('保存产品')
