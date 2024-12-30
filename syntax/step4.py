def check_adult(age):
    possible_age = 18

    if age > possible_age:
        return "성인입니다."
    else:
        return "미성년자입니다."


print(check_adult(19))