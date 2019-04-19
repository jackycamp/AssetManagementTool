

def split_input(some_list):
    k, m = divmod(len(some_list), 3)
    return (some_list[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(0, 3))


if __name__ == '__main__':
    my_list = ['mchc101', 'mchc102', 'mchc103', 'mchc104', 'mchc105', 'mchc106','mchc107', 'mchc108', 'mchc109', 'mchc110', 'mchc111', 'mchc112', 'mchc113',
    'mchc114','mchc115','mchc116','mchc117','mchc118','mchc119','mchc120','mchc121']

    B,C,D = split_input(my_list)
    print(B)
    print(C)
    print(D)

    # print(list(split(my_list, 3)))
