def sorter(data,sort_order,value):
    """
    Verilen veri listesini belirli bir değere göre sıralar.
    Args:
    - data (list): Sıralanacak veri listesi.
    - sort_order (str): Sıralama yöntemi ('ascending' veya 'descending').
    - value (str): Sıralama yapılacak değerin adı.
    Returns:
    - sorted_data: Sıralanmış veri listesi.
    """
    if sort_order == 'ascending':
        return tuple(sorted(data, key=lambda x: x[value]))
    elif sort_order == 'descending':
        return tuple(sorted(data, key=lambda x: x[value], reverse=True))
    else:
        print('WARNING!!!')
        return tuple(data)

def tr_to_eng(text):
    tr_letters = 'çğıöşüÇĞİÖŞÜ'
    eng_letters = 'cgiosuCGIOSU'
    return text.translate(str.maketrans(tr_letters,eng_letters))