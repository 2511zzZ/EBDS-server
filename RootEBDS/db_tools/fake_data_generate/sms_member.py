# coding: utf-8
import random
from db_tools.tools.tools import get_db_connector

# 打开数据库连接
db = get_db_connector()
cursor = db.cursor()

random.seed(12345)
xing = '赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜戚谢邹喻柏水窦章云苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任袁柳酆鲍史唐费廉岑薛雷贺倪汤滕殷罗毕郝邬安常乐于时傅皮卞齐康伍余元卜顾孟平黄和穆萧尹姚邵湛汪祁毛禹狄米贝明臧计伏成戴谈宋茅庞熊纪舒屈项祝董梁'
ming = '豫章故郡洪都新府星分翼轸地接衡庐襟三江而带五湖郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜飞李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜戚谢邹喻柏水窦章云苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任袁柳酆鲍史唐湛汪祁毛禹狄米贝明臧计伏成戴谈宋茅庞熊纪舒屈项祝董梁'
sex = ['male', 'female']
province = ['河北省', '山西省', '辽宁省', '吉林省', '黑龙江省', '江苏省', '浙江省', '安徽省', '福建省', '江西省', '山东省', '河南省', '湖北省', '湖南省', '广东省', '海南省', '四川省', '贵州省', '云南省', '陕西省', '甘肃省', '青海省', '台湾省', '北京市', '天津市', '上海市', '重庆市', '内蒙古自治区', '广西壮族自治区', '西藏自治区', '宁夏回族自治区', '新疆维吾尔自治区', '香港特别行政区', '澳门特别行政区']


def name_generator():
    global xing, ming
    X = random.choice(xing)
    M = "".join(random.choice(ming) for _ in range(random.choice([1, 2])))
    return X + M


def sex_generator():
    global sex
    return random.choice(sex)


def birthday_generator():
    return "-".join(map(str, [random.randint(1960, 2001), random.randint(1, 12), random.randint(1, 28)]))


def birthplace_generator():
    global province
    return random.choice(province)


def insert_to_mysql(start, end, user_type):
    for index in range(start, end+1):
        name = name_generator()
        sex = sex_generator()
        birthday = birthday_generator()
        birthplace = birthplace_generator()
        try:
            sql = "INSERT INTO sms_member(employee_id, name, sex, birthday, birthplace, type) VALUES(%s, %s, %s, %s, %s, %s)"
            val = (index, name, sex, birthday, birthplace, user_type)
            cursor.execute(sql, val)
            # db.commit()
            if index % 100 == 0:
                print(index)
        except Exception as e:
            # 回滚
            print(e)
            db.rollback()
    db.commit()  # 最后提交加快插入，根据内存情况决定commit位置


def run():
    try:
        insert_to_mysql(1, 1+1, 4)  # 总经理/老板 2
        insert_to_mysql(3, 3+34, 3)  # 经理 35
        insert_to_mysql(38, 38+99, 2)  # 大组长 100
        insert_to_mysql(138, 138+14999, 1)  # 工人 1500
    finally:
        cursor.close()
        db.close()


if __name__ == '__main__':
    run()
