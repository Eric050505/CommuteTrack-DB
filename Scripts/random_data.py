import random


def generate_random_chinese_name():
    """ Generate a random Chinese name of length 2 to 4 characters. """
    common_chinese_chars = "赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜戚谢邹喻柏水窦章云苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任袁柳酆鲍史唐费廉岑薛雷贺倪汤滕殷罗毕郝邬安常乐于时傅皮卞齐康伍余元卜顾孟平黄和穆萧尹姚邵湛汪祁毛禹狄米贝明臧计伏成戴谈宋茅庞熊纪舒屈项祝董梁杜阮蓝闵席季麻强贾路娄危江童颜郭梅盛林刁钟徐邱骆高夏蔡田樊胡凌霍虞万支柯昝管卢莫经房裘缪干解应宗丁宣贲邓郁单杭洪包诸左石崇龙"
    return ''.join(random.choice(common_chinese_chars) for _ in range(random.randint(2, 3)))


def generate_random_phone_number():
    """ Generate a random phone number starting with '1'. """
    return '1' + ''.join(random.choice('0123456789') for _ in range(10))


def generate_data(number_of_records):
    genders = ['男', '女']
    districts = ['Chinese Mainland', 'Chinese Hong Kong', 'Chinese Macau', 'Chinese Taiwan']

    sql_commands = ["id_number, name, phone_number, gender, district\n"]
    for _ in range(number_of_records):
        id_number = ''.join(random.choice('0123456789') for _ in range(18))
        name = generate_random_chinese_name()
        phone_number = generate_random_phone_number()
        gender = random.choice(genders)
        district = random.choice(districts)

        sql_commands.append(
            f"'{id_number}', '{name}', '{phone_number}', '{gender}', '{district}'\n")
    sql_commands = sql_commands[:-2]

    return sql_commands


# Generate 100,000 records
sql_data = generate_data(100000)

# Optionally, write to a file if needed, using UTF-8 encoding to avoid issues with Chinese characters
with open('../out/random_passenger.csv', 'w', encoding='utf-8') as f:
    f.writelines(sql_data)

'../out/random_passenger.sql'  # Return the path to the generated file
