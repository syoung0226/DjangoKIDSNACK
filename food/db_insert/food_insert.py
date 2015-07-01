import xlrd
from food.models import Category, SideEffect, RawMaterial, Additive, GovernmentSnack, Snack


def additive_category_insert():
    wb = xlrd.open_workbook('/home/sunyoung/kidsnack_db/additive_category_list.xlsx')
    sheet = wb.sheet_by_index(0)
    for row_num in range(0, sheet.nrows):
        row_values = sheet.row_values(row_num)
        try:
            Category.objects.get(name=row_values[0])
            print('duplicate : ' + row_values[0])
        except Category.DoesNotExist:
            additive_category = Category(name=row_values[0], type='additive_category')
            additive_category.save()


def snack_category_insert():
    wb = xlrd.open_workbook('/home/sunyoung/kidsnack_db/snack_category_list.xlsx')
    sheet = wb.sheet_by_index(0)
    for row_num in range(1, sheet.nrows):
        row_values = sheet.row_values(row_num)
        try:
            Category.objects.get(name=row_values[0], type='snack_category')
            print('duplicate : ' + row_values[0])
        except Category.DoesNotExist:
            snack_category = Category(name=row_values[0], type='snack_category')
            snack_category.save()


def side_effect_insert():
    wb = xlrd.open_workbook('/home/sunyoung/kidsnack_db/side_effect_list.xlsx')
    sheet = wb.sheet_by_index(0)
    for row_num in range(1, sheet.nrows):
        row_values = sheet.row_values(row_num)
        try:
            SideEffect.objects.get(name=row_values[0])
            print('duplicate : ' + row_values[0])
        except SideEffect.DoesNotExist:
            side_effect = SideEffect(name=row_values[0])
            side_effect.save()


def raw_materials_insert():
    wb = xlrd.open_workbook('/home/sunyoung/kidsnack_db/raw_materials_list.xlsx')
    sheet = wb.sheet_by_index(0)
    for row_num in range(1, sheet.nrows):
        row_values = sheet.row_values(row_num)
        try:
            RawMaterial.objects.get(name=row_values[0])
            print('duplicate : ' + row_values[0])
        except RawMaterial.DoesNotExist:
            raw_material = RawMaterial(name=row_values[0])
            raw_material.save()


def additive_insert():
    wb = xlrd.open_workbook('/home/sunyoung/kidsnack_db/additive_list.xlsx')
    sheet = wb.sheet_by_index(0)
    for row_num in range(1, sheet.nrows):
        row_values = sheet.row_values(row_num)
        try:
            Additive.objects.get(name=row_values[0])
            print('duplicate : ' + row_values[0])
        except Additive.DoesNotExist:
            if row_values[7]:
                check = True
            else:
                check = False

            additive = Additive(name=row_values[0], sub_name=row_values[11], eng_name=row_values[1], grade=row_values[6],
                                cas_no=row_values[3], ins_no=row_values[2], design_date=row_values[4],
                                main_use_food=row_values[8], use_purpose_function=row_values[9],
                                characteristic=row_values[10], type=row_values[5], toxic_ingredient_check=check)

            additive.save()

            for i in range(12, 16):
                try:
                    side_effect = SideEffect.objects.get(name=row_values[i])
                except SideEffect.DoesNotExist:
                    continue
                else:
                    additive.side_effect.add(side_effect)
            for i in range(17, 20):
                try:
                    additive_category = Category.objects.get(name=row_values[i], type='additive_category')
                except Category.DoesNotExist:
                    continue
                else:
                    additive.category.add(additive_category)


def government_snack_insert():
    wb = xlrd.open_workbook('/home/sunyoung/kidsnack_db/government_snack_list.xls')
    sheet = wb.sheet_by_index(0)
    for row_num in range(1, sheet.nrows):
        row_values = sheet.row_values(row_num)
        try:
            snack_category = Category.objects.get(name=row_values[1])
        except Category.DoesNotExist:
            print('snack_category not exist : ' + row_values[1])
            continue
        else:
            try:
                GovernmentSnack.objects.get(name=row_values[3])
                print('duplicate : ' + row_values[3])
            except GovernmentSnack.DoesNotExist:
                government_snack = GovernmentSnack(name=row_values[3], brand=row_values[2], calorie=int(row_values[5]),
                                                   carbohydrate=row_values[6], amount_per_serving=row_values[4],
                                                   protein=row_values[7], cholesterol=row_values[11],
                                                   saturated_fat=row_values[12], trans_fat=row_values[13],
                                                   fat=row_values[8], sodium=row_values[10], sugar=row_values[9],
                                                   category=snack_category)
                government_snack.save()


def snack_insert():
    wb = xlrd.open_workbook('/home/sunyoung/kidsnack_db/snack_list.xlsx')
    sheet = wb.sheet_by_index(0)
    for row_num in range(1, sheet.nrows):
        row_values = sheet.row_values(row_num)

        try:
            Snack.objects.get(name=row_values[0])
            print('duplicate : ' + row_values[0])
        except Snack.DoesNotExist:
            try:
                government_snack = GovernmentSnack.objects.get(name=row_values[0])
            except GovernmentSnack.DoesNotExist:
                print('government_snack_not_exist : ' + row_values[0])
                continue
            else:
                snack = Snack(name=row_values[0], img_src=row_values[59], government_snack=government_snack)

            snack.save()

            for i in range(3, 58):
                try:
                    additive = Additive.objects.get(name=row_values[i])
                except Additive.DoesNotExist:
                    continue
                else:
                    snack.additive.add(additive)

            for i in range(3, 58):
                try:
                    raw_material = RawMaterial.objects.get(name=row_values[i])
                except RawMaterial.DoesNotExist:
                    continue
                else:
                    snack.raw_material.add(raw_material)
