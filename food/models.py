# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

Zero = 0
One = 1
Two = 2
Three = 3
Four = 4
GRADE_CHOICES = (
    (Zero, 'Zero'),
    (One, 'One'),
    (Two, 'Two'),
    (Three, 'Three'),
    (Four, 'Four'),
)


class Category(models.Model):
    name = models.CharField(max_length=200, null=False)
    type = models.CharField(max_length=200, null=False)

    def __str__(self):
        return self.name.encode('utf8')

    def to_dict(self):
        return dict(id=self.id, name=self.name, type=self.type)


class SideEffect(models.Model):
    name = models.CharField(max_length=200, null=False)

    def __str__(self):
        return self.name.encode('utf8')

    def to_dict(self):
        return dict(id=self.id, name=self.name)


class RawMaterial(models.Model):
    name = models.CharField(max_length=200, null=False)

    def __str__(self):
        return self.name.encode('utf8')

    def to_dict(self):
        return dict(id=self.id, name=self.name)


class Additive(models.Model):

    TYPE_CHOICES = (
        ('Natural', 'Natural'),
        ('Chemical', 'Chemical')
    )

    name = models.CharField(max_length=200, null=False)
    sub_name = models.CharField(max_length=200, null=True, blank=True)
    eng_name = models.CharField(max_length=200, null=False)
    grade = models.IntegerField(default=Zero, choices=GRADE_CHOICES, null=False)
    cas_no = models.CharField(max_length=200, null=True, blank=True)
    ins_no = models.CharField(max_length=200, null=True, blank=True)
    design_date = models.CharField(max_length=200, null=False)

    main_use_food = models.CharField(max_length=500, null=True, blank=True)
    use_purpose_function = models.CharField(max_length=500, null=True, blank=True)
    characteristic = models.CharField(max_length=500, null=True, blank=True)

    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    toxic_ingredient_check = models.BooleanField(default=False)

    category = models.ManyToManyField(Category)
    side_effect = models.ManyToManyField(SideEffect, blank=True, null=True)

    def __str__(self):
        return self.name.encode('utf8')

    def to_dict(self):
        additive_dict = dict(id=self.id, name=self.name, subName=self.sub_name, engName=self.eng_name,
                             grade=self.grade, casNo=self.cas_no, insNo=self.ins_no, designDate=self.design_date,
                             mainUseFood=self.main_use_food, usePurposeFunction=self.use_purpose_function,
                             characteristic=self.characteristic, type=self.type)
        if self.category:
            additive_dict['categories'] = [category.to_dict() for category in self.category.all()]
        if self.side_effect:
            additive_dict['sideEffects'] = [side_effect.to_dict() for side_effect in self.side_effect.all()]
        return additive_dict

    def toxic_ingredient_to_dict(self):
        toxic_ingredient_dict = dict(id=self.id, name=self.name, grade=self.grade, mainUseFood=self.main_use_food,
                                     usePurposeFunction=self.use_purpose_function,
                                     characteristic=self.characteristic)
        if self.category:
            toxic_ingredient_dict['categories'] = ','.join([category.name for category in self.category.all()])
        if self.side_effect:
            toxic_ingredient_dict['sideEffects'] = ','.join([side_effect.name for side_effect
                                                             in self.side_effect.all()])
        return toxic_ingredient_dict

    def side_effect_to_dict(self):
        if self.side_effect:
            return [side_effect.name for side_effect in self.side_effect.all()]


class GovernmentSnack(models.Model):
    name = models.CharField(max_length=200, null=False)
    brand = models.CharField(max_length=200, null=False)

    calorie = models.IntegerField(default=0, null=False)
    carbohydrate = models.FloatField(default=0, null=False)
    amount_per_serving = models.FloatField(default=0, null=False)
    protein = models.FloatField(default=0, null=False)
    cholesterol = models.FloatField(default=0, null=False)
    saturated_fat = models.FloatField(default=0, null=False)
    trans_fat = models.FloatField(default=0, null=False)
    fat = models.FloatField(default=0, null=False)
    sodium = models.FloatField(default=0, null=False)
    sugar = models.FloatField(default=0, null=False)

    category = models.ForeignKey(Category)

    def __str__(self):
        return self.name.encode('utf8')

    def to_dict(self):
        return dict(id=self.id, name=self.name, brandName=self.brand, calorie=self.calorie,
                    carbohydrate=self.carbohydrate, amoutPerServing=self.amount_per_serving, protein=self.protein,
                    cholesterol=self.cholesterol, saturatedFat=self.saturated_fat, transFat=self.trans_fat,
                    fat=self.fat, sodium=self.sodium, sugar=self.sugar, category=self.category.to_dict())

    def nutrients_to_dict(self):
        return [self.sugar, self.fat, self.sodium]


class Snack(models.Model):
    Nothing = 0
    Like = 1
    Hate = 2
    PREFERENCE_CHOICES = (
        (Nothing, 'Nothing'),
        (Like, 'Like'),
        (Hate, 'Hate'),
    )

    name = models.CharField(max_length=200, null=False)

    snack_grade = models.IntegerField(default=Zero, choices=GRADE_CHOICES, null=False)

    toxic_ingredient_count = models.PositiveSmallIntegerField(default=0, null=False)
    side_effect_count = models.PositiveSmallIntegerField(default=0, null=False)

    img_src = models.CharField(max_length=500, null=False)

    preference = models.IntegerField(default=Nothing, choices=PREFERENCE_CHOICES, null=False)

    government_snack = models.ForeignKey(GovernmentSnack, null=True, blank=True)
    additive = models.ManyToManyField(Additive)
    raw_material = models.ManyToManyField(RawMaterial)

    def __str__(self):
        return self.name.encode('utf8')

    def to_dict(self):
        snack_dict = dict(id=self.id, name=self.name, snackGrade=self.snack_grade, preference=self.preference,
                          toxicIngredientCount=self.toxic_ingredient_count, sideEffectCount=self.side_effect_count,
                          imgSrc=self.img_src, governmentSnack=self.government_snack.to_dict())

        if self.additive:
            snack_dict['Additives'] = [additive.to_dict() for additive in self.additive.all()]
        if self.raw_material:
            snack_dict['rawMaterials'] = [raw_material.to_dict() for raw_material in self.raw_material.all()]
        return snack_dict

    def list_to_dict(self):
        return dict(id=self.id, name=self.name, snackGrade=self.snack_grade, preference=self.preference,
                    imgSrc=self.img_src, brandName=self.government_snack.brand)

    def detail_to_dict(self):
        snack_dict = dict(id=self.id, name=self.name, calorie=self.government_snack.calorie,
                          snackGrade=self.snack_grade, preference=self.preference,
                          toxicIngredientCount=self.toxic_ingredient_count, sideEffectCount=self.side_effect_count,
                          imgSrc=self.img_src, brandName=self.government_snack.brand,
                          nutrients=self.government_snack.nutrients_to_dict())

        if self.additive:
            toxic_ingredients = []
            for additive in self.additive.all():
                if additive.toxic_ingredient_check:
                    toxic_ingredients = toxic_ingredients + [additive.toxic_ingredient_to_dict()]

            snack_dict['toxicIngredients'] = toxic_ingredients
            snack_dict['components'] = [additive.name for additive in self.additive.all()]

        if self.raw_material:
            snack_dict['components'] = snack_dict['components'] + [raw_material.name for raw_material in
                                                                   self.raw_material.all()]
        return snack_dict


class SnackLike(models.Model):
    snack = models.ForeignKey(Snack)
    user = models.ForeignKey(User)

    def to_dict(self):
        return dict(id=self.id, snack=self.snack.to_dict(), user=self.user.email)

    def list_to_dict(self):
        return self.snack.list_to_dict()


class SnackHate(models.Model):
    snack = models.ForeignKey(Snack)
    user = models.ForeignKey(User)

    def to_dict(self):
        return dict(id=self.id, snack=self.snack.to_dict(), user=self.user.email)

    def list_to_dict(self):
        return self.snack.list_to_dict()


class RequireSnack(models.Model):
    name = models.CharField(max_length=200, null=False)
    brand = models.CharField(max_length=200, null=False)
    user = models.ForeignKey(User)

    def __str__(self):
        return self.name.encode('utf8')

    def to_dict(self):
        return dict(id=self.id, name=self.name, brandName=self.brand, user=self.user.email)
