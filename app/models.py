"""
Definition of models.
"""

from django.db import models

# Create your models here.

#------------------------------------------------------------------------
class AgeGroup(models.Model):
    # use default id primary key
    name = models.CharField(max_length = 60)

class Sex(models.Model):
    # use default id primary key
    name = models.CharField(max_length=8)

class EducationLevel(models.Model):
    name = models.CharField(max_length=60)

class EmploymentRatio(models.Model):
    ageGroup = models.ForeignKey(AgeGroup)
    sex = models.ForeignKey(Sex)
    educLevel = models.ForeignKey(EducationLevel)
    value = models.FloatField()
    
    def __unicode__(self):
        return "AgeGroup: %s, Sex: %s, EducLevel: %s, Ratio: %s" \
                 %(self.ageGroup.name, self.sex.name, self.educLevel.name, self.value )

#------------------------------------------------------------------------
class DataQuality(models.Model):
   name = models.CharField(max_length=8)

class WorkField(models.Model):
   name = models.CharField(max_length=128)
   quality = models.ForeignKey(DataQuality)

class Province(models.Model):
   name = models.CharField(max_length=60)
   
class UnemploymentToVacanciesRatio(models.Model):
   value = models.FloatField()
   province = models.ForeignKey(Province)
   workField = models.ForeignKey(WorkField)

   def __unicode__(self):
      return "Province: %s, WorkField: %s, DataQuality: %s, UnemploymentToVacanciesRatio: %s" \
            %(self.province.name, self.workField.name, self.workField.quality.name, self.value)






