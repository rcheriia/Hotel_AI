#файл com.txt содержит длинны отзывов
with open("com.txt", encoding="utf-8") as file:
    com = [int(x) for x in file.readline().split(", ") if int(x)]

print(len(com))


def normaliz(spism, rast=1):
    normal = []

    for i in range(len(spism)):
        start = max(0, i - rast)
        end = min(len(spism) - 1, i + rast)
        new = sum(spism[start:end]) // (end - start)

        normal.append(new)

    return normal


def alis(slv, rating=0.1):
    d1 = sorted([x for x in slv.keys()])

    normal = [0]
    uks = d1[0]

    for i in range(1, d1[-1] + 1):
        if d1[uks] < i and uks + 2 < len(d1):
            uks += 1

        razx = normal[i - 1] - (normal[i - 1] + slv[d1[uks]] + slv[d1[uks + 1]]) // 3
        new = normal[i - 1] - razx * rating

        normal.append(new)

    print(len(normal))

    return [x for x in range(d1[-1] + 1)], normal


def diogramma(spis_len):
    import matplotlib.pyplot as plt

    spis_len = com

    sred = sum(spis_len) // len(spis_len)
    sred_kor = 1000
    spis_len = [x for x in spis_len if x < sred_kor]

    slv = {}

    for i in spis_len:
        n = 15
        ind = (i // n) * n
        slv[ind] = slv.get(ind, 0) + 1

    slv[0] = 0

    y = sorted(slv.keys())
    x = [slv[i] for i in y]

    y, x = alis(slv, rating=0.1)

    for i in range(3):
        x = normaliz(x, rast=14)

    plt.plot(y, x)
    plt.fill_between(y, x)
    print("end")
    plt.show()


diogramma(com)
