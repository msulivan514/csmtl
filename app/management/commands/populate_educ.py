from django.core.management.base import BaseCommand
from app.models import Sex, AgeGroup, EducationLevel, EmploymentRatio
import csv
import urllib2

class Command(BaseCommand):
   help = "Populate the Education Level tables"

   #-------------------------------------------------
   def _fetch_data(self, url):
      response = urllib2.urlopen(url)
      return response

   #-------------------------------------------------
   def _read_csv_into_db(self, csvFile):
      datareader = csv.reader(csvFile, delimiter=',')

      # Sex data
      sexMan = Sex.objects.filter(name = "Male")
      if( not sexMan ):
         sexMan = Sex.objects.create(name = "Male")
         sexMan.save()
      else:
         sexMan = sexMan[0]

      sexWoman = Sex.objects.filter(name="Female")
      if( not sexWoman ):
         sexWoman = Sex.objects.create(name = "Female")
         sexWoman.save()
      else:
         sexWoman = sexWoman[0]
      
      # read years, and skip bad lines
      lineSkipCount = 10 
      for i in range(lineSkipCount):
         row = next(datareader)

      # parse relevant sections
      for row in datareader:
         if "Statistics Canada" in row[0]:
            break;

         educLevelData = unicode(row[0], "latin-1")
         educLevel = EducationLevel.objects.create( name = educLevelData )
         educLevel.save()

         for i in range(3):
            row = next(datareader)
            ageGroupData = unicode(row[0], "latin-1") 
            ageGroup = AgeGroup.objects.filter( name = ageGroupData )
            if( not ageGroup ):
               ageGroup = AgeGroup.objects.create( name = ageGroupData )
               ageGroup.save()
            else:
               ageGroup = ageGroup[0]

            ratioMen = EmploymentRatio.objects.create( ageGroup=ageGroup, sex=sexMan, educLevel=educLevel, value=row[2])
            ratioWomen = EmploymentRatio.objects.create( ageGroup=ageGroup, sex=sexWoman, educLevel=educLevel, value=row[3])

            ratioMen.save()
            ratioWomen.save()

            print "Ratio Men: %s" %ratioMen
            print "Ratio Women: %s" %ratioWomen

   def handle(self, *args, **options):
      url = "http://www.statcan.gc.ca/cgi-bin/sum-som/fl/cstsaveascsv.cgi?filename=labor62-eng.htm&lan=eng"
      csvFile = self._fetch_data(url)
      self._read_csv_into_db(csvFile)
      print "Success"

