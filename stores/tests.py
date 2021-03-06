import json
import bcrypt
import jwt
import uuid

from django.test       import Client, TransactionTestCase
from unittest.mock     import MagicMock, Mock, patch

from wisely.settings   import SECRET_KEY, ALGORITHMS
from user.models       import User
from stores.models     import (
GiftSet,
GiftSetImage,
RazorSet,
RazorSetImage,
Blade,
ShavingGel,
AfterShave,
AfterShaveSkinType,
SkinType,
Color,
Cart,
Order,
OrderStatus
)

class CartViewTest(TransactionTestCase):
    def setUp(self):
        user = User.objects.create(
            id = 1,
            password      = bcrypt.hashpw('12345678'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            phone         = '01012345678',
            birth         = '1994-05-11',
            name          = 'unittest',
            gender        = '남성',
            alarm_confirm = '1'
        )
        order_status = OrderStatus.objects.create(
            id = 1,
            status = '결제 대기'
        )
        order = Order.objects.create(
            id = 1,
            order_num       = 'wisely_9c5643d74e7c44b1a12bdcb8da72659f',
            user            = user,
            order_status    = order_status,
        )
        navy_color = Color.objects.create(
            id   = 1,
            name = '미드나이트 네이비',
            code = '#00306b'
        )
        gift_image = GiftSetImage.objects.create(
            id = 1,
            product_image = 'https://wiselyshave-cdn.s3.amazonaws.com/assets/images/items/gift_set/gift_set_navy.png',
            color = navy_color
        )
        gift_set_navy = GiftSet.objects.create(
            id = 1,
            name  = '선물세트(면도용품+기프트 카드)',
            price = 29800,
            image = gift_image
        )
        razor_image = RazorSetImage.objects.create(
            id = 1,
            product_image = 'https://wiselyshave-cdn.s3.amazonaws.com/assets/images/items/starter_kit/starter_navy.png',
            result_image  = 'https://wiselyshave-cdn.s3.amazonaws.com/assets/images/surveyResult/survey_result_razor_navy.png',
            color         = navy_color
        )
        RazorSet.objects.create(
            id    = 1,
            name = '면도기세트(면도기+날2입)',
            price = 8900,
            image = razor_image
        )
        Blade.objects.create(
            id = 1,
            name =  '리필면도날 (4입)',
            price = 9600,
            image = 'https://wiselyshave-cdn.s3.amazonaws.com/assets/images/items/blade/refill_blade.png',
            result_image = 'https://wiselyshave-cdn.s3.amazonaws.com/assets/images/surveyResult/survey_result_blade.png'
        )
        ShavingGel.objects.create(
            id   = 1,
            name = '스탠다드 150ml',
            price = 4500,
            image = 'https://wiselyshave-cdn.s3.amazonaws.com/assets/images/items/shaving_gel/shaving_gel_150.png',
            result_image = 'https://wiselyshave-cdn.s3.amazonaws.com/assets/images/surveyResult/survey_result_gel.png'
        )
        after_shave_60ml = AfterShave.objects.create(
            id    = 1,
            name  = '스탠다드 60ml',
            price = 6500
        )
        after_shave_30ml = AfterShave.objects.create(
            id    = 2,
            name  = '여행용 30ml',
            price = 3900
        )
        skin_type_dry = SkinType.objects.create(
            id   = 2,
            name = '건성'
        )
        skin_type_oily = SkinType.objects.create(
            id   = 1,
            name = '지성'
        )
        after_shave_60ml_dry = AfterShaveSkinType.objects.create(
            id = 2,
            after_shave  = after_shave_60ml,
            skin_type    = skin_type_dry,
            image        = 'https://wiselyshave-cdn.s3.amazonaws.com/assets/images/items/aftershaving/after_shaving_gel_dry_60.png',
            result_image = 'https://wiselyshave-cdn.s3.amazonaws.com/assets/images/surveyResult/survey_result_after_shaving_gel.png'
        )
        after_shave_30ml_oily = AfterShaveSkinType.objects.create(
            id = 3,
            after_shave = after_shave_30ml,
            skin_type   = skin_type_oily,
            image       = 'https://wiselyshave-cdn.s3.amazonaws.com/assets/images/items/starter_aftershaveing/after_shaving_gel_oily_30.png'
        )
        Cart.objects.create(
            id        = 1,
            quantity  = 1,
            user      = user,
            gift_set  = gift_set_navy,
            razor_set = None,
            blade     = None,
            shaving_gel = None,
            after_shave = None,
            color = None,
            order = order
        )

    def tearDown(self):
        User.objects.all().delete()
        Order.objects.all().delete()
        Color.objects.all().delete()
        GiftSetImage.objects.all().delete()
        GiftSet.objects.all().delete()
        RazorSetImage.objects.all().delete()
        RazorSet.objects.all().delete()
        Blade.objects.all().delete()
        ShavingGel.objects.all().delete()
        AfterShave.objects.all().delete()
        SkinType.objects.all().delete()
        AfterShaveSkinType.objects.all().delete()
        Cart.objects.all().delete()

    def test_cart_add_bad_request(self):
        user = User.objects.get(id = 1)
        client = Client()
        cart = {'gift_set_id'    : '1',
                'razor_set_id'   : '1',
                'blade_id'       : None,
                'shaving_gel_id' : None,
                'after_shave_id' : None
                }
        response = client.post('/cart', json.dumps(cart), content_type = 'application/json', **{'HTTP_AUTHORIZATION' : jwt.encode({'id': user.id}, SECRET_KEY, algorithm = ALGORITHMS).decode()})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{'message' : 'BAD_REQUEST'})

    def test_cart_add_create(self):
        client = Client()
        user = User.objects.get(id = 1)
        cart = {'gift_set_id'    : '1',
                'razor_set_id'   : None,
                'blade_id'       : None,
                'shaving_gel_id' : None,
                'after_shave_id' : None,
                }
        response = client.post('/cart', json.dumps(cart), content_type = 'application/json', **{'HTTP_AUTHORIZATION' : jwt.encode({'id': user.id}, SECRET_KEY, algorithm = ALGORITHMS).decode()})
        self.assertEqual(response.status_code, 200)

    def test_cart_add_intergrityerror(self):
        user = User.objects.get(id = 1)
        client = Client()
        cart = {'gift_set_id'    : '4',
                'razor_set_id'   : None,
                'blade_id'       : None,
                'shaving_gel_id' : None,
                'after_shave_id' : None
                }
        response = client.post('/cart', json.dumps(cart), content_type = 'application/json', **{'HTTP_AUTHORIZATION' : jwt.encode({'id': user.id}, SECRET_KEY, algorithm = ALGORITHMS).decode()})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{'message' : 'PRODUCT_DOES_NOT_EXISTS'})

    def test_cart_add_keyerror(self):
        user = User.objects.get(id = 1)
        client = Client()
        cart = {'gift_set'    : '1',
                'razor_set'   : None,
                'blade'       : None,
                'shaving_gel' : None,
                'after_shave' : None
                }
        response = client.post('/cart', json.dumps(cart), content_type = 'application/json', **{'HTTP_AUTHORIZATION' : jwt.encode({'id': user.id}, SECRET_KEY, algorithm = ALGORITHMS).decode()})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{'message' : 'KEY_ERROR'})

    def test_cart_list(self):
        self.maxDiff = None 
        user = User.objects.get(id =1)
        client = Client()
        cart = {'gift_set'    : '1',
                'razor_set'   : None,
                'blade'       : None,
                'shaving_gel' : None,
                'after_shave' : None
                }
        response = client.post('/cart', json.dumps(cart), content_type = 'application/json', **{'HTTP_AUTHORIZATION' : jwt.encode({'id': user.id}, SECRET_KEY, algorithm = ALGORITHMS).decode()})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 
        {'carts' : 
          [
           {'id'            : 1,
            'order_number'  : 'wisely_9c5643d74e7c44b1a12bdcb8da72659f',
            'name'          : 'unittest',
            'address'       : '',
            'phone_number'  : '',
            'memo'          : '',
            'order_status'  : '결제 대기',
            'cart': [
                   {'gift_id'          : 1,
                    'gift_set'         : '선물세트(면도용품+기프트 카드)',
                    'gift_color'       : '미드나이트 네이비',
                    'gift_price'       : 29800,
                    'gift_image'       : 'https://wiselyshave-cdn.s3.amazonaws.com/assets/images/items/gift_set/gift_set_navy.png',
                    'razor_id'         : None,
                    'razor_set'        : None,
                    'razor_color'      : None,
                    'razor_price'      : None,
                    'razor_image'      : None,
                    'blade_id'         : None,
                    'blade'            : None,
                    'blade_price'      : None,
                    'blade_image'      : None,
                    'shaving_gel_id'   : None,
                    'shaving_gel'      : None,
                    'shaving_gel_price': None,
                    'shaving_gel_image': None,
                    'after_shave_id'   : None,
                    'after_shave'      : None,
                    'skin_type'        : None,
                    'after_shave_price': None,
                    'after_shave_image': None
                    }
                ]
            }
          ],
            'quantities': {
                    'gift_set_navy': {
                        'quantity': 1
                    },
                    'gift_set_blue': {
                        'quantity': 0
                    },
                    'gift_set_gray': {
                        'quantity': 0
                    },
                    'razor_set_navy': {
                        'quantity': 0
                    },
                    'razor_set_blue': {
                        'quantity': 0
                    },
                    'razor_set_gray': {
                        'quantity': 0
                    },
                    'blade': {
                        'quantity': 0
                    },
                    'shaving_gel_150': {
                        'quantity': 0
                    },
                    'shaving_gel_75': {
                        'quantity': 0
                    },
                    'after_shave_60_oily': {
                        'quantity': 0
                    },
                    'after_shave_60_dry': {
                        'quantity': 0
                    },
                    'after_shave_30_oily': {
                        'quantity': 0
                    },
                    'after_shave_30_dry': {
                        'quantity': 0
                    }
                }
        })
