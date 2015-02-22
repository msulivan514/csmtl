from django.core.management.base import BaseCommand
from app.models import WorkField, DataQuality, UnemploymentToVacanciesRatio, Province
import csv
import urllib2
import zipfile
import StringIO

#------------------------------------------------------------------------
def _GetDataQualityData(workFieldData):
   dataQuality = \
   { 
         "Accommodation and food services"                                          : "C",
         "Administrative and support, waste management and remediation services"    : "D",
         "All unemployed"                                                           : "A",
         "Arts, entertainment and recreation"                                       : "D",
         "Construction"                                                             : "D",
         "Educational services"                                                     : "D",
         "Finance and insurance"                                                    : "D",
         "Forestry, logging and support"                                            : "F",
         "Health care and social assistance"                                        : "C",
         "Information and cultural industries"                                      : "D",
         "Management of companies and enterprises"                                  : "..",
         "Manufacturing"                                                            : "C",
         "Mining, quarrying, and oil and gas extraction"                            : "E",
         "Other services (except public administration)"                            : "E",
         "Professional, scientific and technical services"                          : "D",
         "Public administration"                                                    : "C",
         "Real estate and rental and leasing"                                       : "E",
         "Retail trade"                                                             : "C",
         "Transportation and warehousing"                                           : "C",
         "Unemployed, all sectors, worked within past 12 months"                    : "A",
         "Utilities"                                                                : "E",
         "Wholesale trade"                                                          : "D",
   }
   if workFieldData not in dataQuality.keys():
      print "workfield not found %s, len: %u" %(workFieldData, len(workFieldData))
      raise

   return dataQuality[workFieldData]
   
#------------------------------------------------------------------------
def _GetOrCreateDataQuality( dataQualityData ):
   dataQuality = DataQuality.objects.filter(name = dataQualityData )
   if not dataQuality:
      dataQuality = DataQuality.objects.create(name = dataQualityData)
      dataQuality.save()
   else:
      dataQuality = dataQuality[0]

   return dataQuality

#------------------------------------------------------------------------
def _GetOrCreateProvince( provinceData ):
   province = Province.objects.filter( name = provinceData )
   if not province:
      province = Province.objects.create( name = provinceData )
      province.save()
   else:
      province = province[0]

   return province


#------------------------------------------------------------------------
def _GetOrCreateWorkField( workFieldData ):
   workField = WorkField.objects.filter( name = workFieldData )
   if not workField:
      dataQualityData = _GetDataQualityData(workFieldData)
      dataQuality = _GetOrCreateDataQuality(dataQualityData)
      workField = WorkField.objects.create( name = workFieldData, quality=dataQuality )
      workField.save()
   else:
      workField = workField[0]

   return workField


#------------------------------------------------------------------------
class Command(BaseCommand):
   help = "Populate the Education Level tables"

   #-------------------------------------------------
   def _fetch_zipped_data(self, url, zippedFileName ):
      zippedData = urllib2.urlopen(url).read()
      zf = zipfile.ZipFile( StringIO.StringIO(zippedData) )
      fd = zf.open(zippedFileName)
      return fd

   #-------------------------------------------------
   def _read_csv_into_db(self, csvFile):
      datareader = csv.reader(csvFile, delimiter=',')
      yearSelected = "2013"
      ratioString = "Unemployment-to-job vacancies ratio"

     
      # parse relevant sections
      for row in datareader:

         # exclude unwanted years
         year = unicode(row[0], "latin-1")
         if year != yearSelected:
            continue

         # exclude unwanted results
         ratioData = unicode(row[2], "latin-1")
         if ratioData != ratioString:
            continue

         # exclude missing results
         resultData = unicode(row[6], "latin-1")
         if not resultData.replace(".", "", 1).isdigit():
            continue

         # fetch the province 
         provinceData = unicode(row[1], "latin-1")
         province = _GetOrCreateProvince(provinceData)

         # fetch the work field
         workFieldData = unicode(row[3], "latin-1")
         workField = _GetOrCreateWorkField(workFieldData)

         # create the result
         unemploymentToVacanciesRatio = UnemploymentToVacanciesRatio.objects.create( workField = workField,
               province = province, value = resultData )

         unemploymentToVacanciesRatio.save()

         print "%s" %unemploymentToVacanciesRatio

   #-------------------------------------------------
   def handle(self, *args, **options):
      url = "http://www20.statcan.gc.ca/tables-tableaux/cansim/csv/02840004-eng.zip"
      csvFile = self._fetch_zipped_data(url, "02840004-eng.csv" )
      self._read_csv_into_db(csvFile)
      print "Success"

