height = 129
is_possible = height <= 220 and height >= 130

if is_possible:
    print("놀이기구 이용 가능")
else:
    print("놀이기구 이용 불가능")

current_time = 12
start_time = 16
end_time = 23
is_operational = current_time >= start_time and current_time < end_time

if is_operational:
    print("영업 중입니다.")
else:
    print("영업 준비중입니다.")
