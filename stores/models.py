from django.db import models

class GiftSet(models.Model):
    name  = models.CharField(max_length = 20)
    price = models.PositiveIntegerField(default = 0)
    image = models.ForeignKey('GiftSetImage', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'gift_sets'

class GiftSetImage(models.Model):
    product_image = models.URLField(max_length = 2000)
    color         = models.ForeignKey('Color', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'gift_set_images'

class RazorSet(models.Model):
    name  = models.CharField(max_length = 20)
    price = models.PositiveIntegerField(default = 0)
    image = models.ForeignKey('RazorSetImage', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'razor_sets'

class RazorSetImage(models.Model):
    product_image = models.URLField(max_length = 2000)
    result_image  = models.URLField(max_length = 2000)
    color         = models.ForeignKey('Color', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'razor_set_images'

class Blade(models.Model):
    name         = models.CharField(max_length = 20)
    price        = models.PositiveIntegerField(default = 0)
    image        = models.URLField(max_length = 2000)
    result_image = models.URLField(max_length = 2000)

    class Meta:
        db_table = 'blades'

class ShavingGel(models.Model):
    name         = models.CharField(max_length = 20)
    price        = models.PositiveIntegerField(default = 0)
    image        = models.URLField(max_length = 2000)
    result_image = models.URLField(max_length = 2000)

    class Meta:
        db_table = 'shaving_gels'

class AfterShave(models.Model):
    name                  = models.CharField(max_length = 20)
    price                 = models.PositiveIntegerField(default = 0)
    after_shave_skin_type = models.ManyToManyField('SkinType', through = 'AfterShaveSkinType')

    class Meta:
        db_table = 'after_shaves'

class AfterShaveSkinType(models.Model):
    after_shave  = models.ForeignKey('AfterShave', on_delete = models.SET_NULL, null = True)
    skin_type    = models.ForeignKey('SkinType', on_delete = models.SET_NULL, null = True)
    image        = models.URLField(max_length = 2000)
    result_image = models.URLField(max_length = 2000)

    class Meta:
        db_table = 'after_shaves_skin_types'

class SkinType(models.Model):
    name = models.CharField(max_length = 30)

    class Meta:
        db_table = 'skin_types'

class Color(models.Model):
    name = models.CharField(max_length = 20)
    code = models.CharField(max_length = 10)

    class Meta:
        db_table = 'colors'

class RazorImages(models.Model):
    image_type       = models.CharField(max_length = 20)
    image            = models.URLField(max_length = 2000)
    background_image = models.URLField(max_length = 2000)
    color            = models.ForeignKey('Color', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'razor_images'

class Cart(models.Model):
    quantity    = models.PositiveIntegerField(default = 0)
    user        = models.ForeignKey('user.User', on_delete = models.SET_NULL, null = True)
    gift_set    = models.ForeignKey('GiftSet', on_delete = models.SET_NULL, null = True)
    razor_set   = models.ForeignKey('RazorSet', on_delete = models.SET_NULL, null = True)
    blade       = models.ForeignKey('Blade', on_delete = models.SET_NULL, null = True)
    shaving_gel = models.ForeignKey('ShavingGel', on_delete = models.SET_NULL, null = True)
    after_shave = models.ForeignKey('AfterShaveSkinType', on_delete = models.SET_NULL, null = True)
    order       = models.ForeignKey('Order', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'carts'

class Order(models.Model):
    order_num      = models.CharField(max_length = 50)
    name           = models.CharField(max_length = 50)
    phone_number   = models.CharField(max_length = 20)
    address        = models.CharField(max_length = 1000)
    detail_address = models.CharField(max_length = 500)
    memo           = models.CharField(max_length = 500)
    order_status   = models.ForeignKey('OrderStatus', on_delete = models.SET_NULL, null = True)
    user           = models.ForeignKey('user.User', on_delete = models.SET_NULL, null = True)
    created_at     = models.DateTimeField(auto_now_add = True)
    updated_at     = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'orders'

class OrderStatus(models.Model):
    status = models.CharField(max_length = 30)

    class Meta:
        db_table = 'order_status'

