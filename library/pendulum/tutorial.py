import pendulum

now = pendulum.now('UTC')

print(now)

print(now.timezone.name)

print(now.format("YYYYMMDDHHmmssSSSSSS"))

print(now.in_timezone('Asia/Seoul'))

print(now.in_timezone('Asia/Seoul').format("YYYYMMDDHHmmssSSSSSS"))

print(now.to_iso8601_string())

print(pendulum.from_format('1975-05-21 22', 'YYYY-MM-DD HH'))

print(type(pendulum.parse("2024-05-20 00:28:29.536141+09:00")))
