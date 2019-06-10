import ast
from config import setting
from faker import Faker
from lib.public import logger


class RandomData(object):

    fake = Faker(locale='zh_CN')
    random_data = {
        'RandomName': fake.name(),
        'RandomPhoneNum': fake.phone_number(),
        'RandomWord': fake.word(ext_word_list=None),
        'RandomSentence': fake.sentence(nb_words=6, variable_nb_words=True, ext_word_list=None),
        'RandomParagraph': fake.paragraph(nb_sentences=3, variable_nb_sentences=True, ext_word_list=None),
        'RandomPostcode': fake.postcode(),
        'RandomCompany': fake.company(),
        'RandomDate': fake.date(),
        'RandomEmail': fake.ascii_email(),
        'RandomText': fake.text(),
        'RandomSsn': fake.ssn()
    }

    @classmethod
    def create_random_test_data(cls):
        for key, value in cls.random_data.items():
            filepath = setting.RES + key + '.yaml'
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write('{}: {}'.format(key, value))
                logger.log_info('生成随机测试数据 => {} 成功.'.format(filepath))
