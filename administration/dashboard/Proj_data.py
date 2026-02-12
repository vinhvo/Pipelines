import json
from jsonpath_ng.ext import parse
import getpass
import os
import xlsxwriter
import requests
import datetime
from datetime import datetime
from datetime import date
import Proj_list
import argparse

parser = argparse.ArgumentParser(description='Gets Jenkins Password.')

parser.add_argument("-p", "--print_string", help="Gets Jenkins Password.", type =str)

args = parser.parse_args()

token = 'FortifyToken NjVkMGM5M2MtMTNmYS00NjlkLTkzNTAtZTNiYjVjNWRlNmUz'

row = 0
column = 0

user = 'ics_jenkins'
password = args.print_string

today = date.today()
d = today.strftime("%d_%m_%Y")
workbook = xlsxwriter.Workbook('Dashboard_' + d + '.xlsx')


worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold': True})

data_fortify_list = Proj_list.fort_proj_list()
data_fortify_proj_url = Proj_list.fort_proj_url()


data_sonar_list = Proj_list.sonar_proj_list()
data_sonar_proj_url = Proj_list.sonar_proj_url()

data_nexusiq_list = Proj_list.nexusiq_proj_id()
data_nexusiq_proj_name = Proj_list.nexusiq_proj_name()
data_nexusiq_proj_url = Proj_list.nexusiq_proj_url()

data_generic_proj_name = Proj_list.generic_proj_name()


# --------------Fortify Proj1 Functions--------------------------
def fort_proj1_crit():
    critical = parse('data[0:].series[0:].points[?(@.x== "Critical")].y').find(resp_fortify_proj1)
    for matchCritical in critical:
        if len(critical) == 0:
            return 0
        else:
            return matchCritical.value

def fort_proj1_high():
    high  = parse('data[0:].series[0:].points[?(@.x== "High")].y').find(resp_fortify_proj1)
    for matchHigh in high:
        if len(high) == 0:
            return 0
        else:
            return matchHigh.value

def fort_proj1_lastScan():
    lastScan = parse('data[*].lastScanDate').find(resp_fortify_proj1_lastScan)
    for matchlastScan in lastScan:
        if len(lastScan) == 0:
            return 0
        else:
            date = datetime.strptime(matchlastScan.value, "%Y-%m-%dT%H:%M:%S.%f%z")
            return date.strftime("%b %d %Y %H:%M %p")


def fort_proj1_totalIssue():
    totalIssue = parse('data[0:].totalIssueCount').find(resp_fortify_proj1)
    for matchtotalIssue in totalIssue:
        if len(totalIssue) == 0:
            return 0
        else:
            return matchtotalIssue.value

def fort_proj1_percent_audited():
    audited = parse('$.data.value').find(resp_fortify_proj1_percent_audited)
    for matchpercentAudited in audited:
        if len(audited) == 0:
            return 0
        else:
            return matchpercentAudited.value

    # ----------Sonar Proj1 Functions------------------------------------

def sonar_proj1_critical():
    critical = parse('$.total').find(resp_sonar_proj1_critical)
    for matchCritical in critical:
        if len(critical) == 0:
            return 0
        else:
            return matchCritical.value

def sonar_proj1_blocker():
    blocker = parse('$.total').find(resp_sonar_proj1_blocker)
    for matchBlocker in blocker:
        if len(blocker) == 0:
            return 0
        else:
            return matchBlocker.value

def sonar_proj1_coverage():
    coverage = parse('$.component.measures[0:].value').find(resp_sonar_proj1_coverage)
    for matchCoverage in coverage:
        if len(coverage) == 0:
            return 0
        else:
            return matchCoverage.value

def sonar_proj1_lines_to_cover():
    lines_to_cover =  parse('$.component.measures[0:].value').find(resp_sonar_proj1_lines_to_cover)
    for matchLines_to_cover in lines_to_cover:
        if len(lines_to_cover) == 0:
            return 0
        else:
            return format(int(matchLines_to_cover.value),",")

def sonar_proj1_uncovered_lines():
    uncovered_lines = parse('$.component.measures[0:].value').find(resp_sonar_proj1_uncovered_lines)
    for matchUncovered in uncovered_lines:
        if len(uncovered_lines) == 0:
            return 0
        else:
            return format(int(matchUncovered.value),",")

def sonar_proj1_unit_tests():
    unit_tests = parse('$.component.measures[0:].value').find(resp_sonar_proj1_tests)
    for matchUnitTests in unit_tests:
        if len(unit_tests) == 0:
            return 0
        else:
            return matchUnitTests.value

def sonar_proj1_test_success_density():
    test_success_density = parse('$.component.measures[0:].value').find(resp_sonar_proj1_test_sucess_density)
    for matchSucessDensity in test_success_density:
        if len(test_success_density) == 0:
            return 0
        else:
            return matchSucessDensity.value

def sonar_proj1_scan_date():
    scan_date = parse('$.analyses[*].date').find(resp_sonar_proj1_scan_date)
    for matchScanDate in scan_date:
        if len(scan_date) == 0:
            return 0
        else:
            date = datetime.strptime(matchScanDate.value, "%Y-%m-%dT%H:%M:%S%z")
            return date.strftime("%b %d %Y %H:%M %p")
            
def sonar_proj1_quality_profile():
    quality_profile = parse('$.profiles[0].name').find(resp_sonar_proj1_quality_profile)
    for matchQualityProfile in quality_profile:
        if len(quality_profile) == 0:
            return 0
        else:
            return matchQualityProfile.value


    # Guality gate metrics only refers to 'Default quality gate' and this measures can be changed based on gate profile which project uses
def sonar_proj1_quality_gate(sonar_proj1_blocker,sonar_proj1_coverage,sonar_proj1_critical,sonar_proj1_test_success_density):
    if int(sonar_proj1_blocker()) > 0 or int(float(sonar_proj1_coverage())) < 20.0 or int(sonar_proj1_critical()) > 0 or int(float(sonar_proj1_test_success_density())) < 100.0 :
        return 'Failed'
    else:
         return 'Passed'

    # --------------NexusIQ Proj1 Functions--------------------------
def nexusiq_proj1_critical():
    critical = parse('$[?(@.publicId == '+ nexusiq_proj1 +')].policyEvaluationsResults.build.criticalPolicyViolationCount').find(resp_nexusiq_proj1)
    for matchCritical in critical:
        if len(critical) == 0:
            return 0
        else:
            return matchCritical.value


def nexusiq_proj1_severe():
    severe = parse('$[?(@.publicId == '+ nexusiq_proj1 +')].policyEvaluationsResults.build.severePolicyViolationCount').find(resp_nexusiq_proj1)
    for matchSevere in severe:
        if len(severe) == 0:
            return 0
        else:
            return matchSevere.value


def nexuiq_proj1_moderate():
    moderate = parse('$[?(@.publicId =='+ nexusiq_proj1 +')].policyEvaluationsResults.build.moderatePolicyViolationCount').find(resp_nexusiq_proj1)
    for matchModerate in moderate:
        if len(moderate) == 0:
            return 0
        else:
            return matchModerate.value


def nexusiq_proj1_time():
    time = parse('$[?(@.publicId == '+ nexusiq_proj1 +')].policyEvaluations.build.time').find(resp_nexusiq_proj1)
    for matchTime in time:
        if len(time) == 0:
            return 0
        else:
            a = str(matchTime.value)
            date = int(a[:10])
            scan_time = datetime.fromtimestamp(date).strftime('%b %d %Y %H:%M %p')
            return scan_time

def nexusiq_proj1_total_viol():
    total_violations = nexusiq_proj1_critical() +nexusiq_proj1_severe() +nexuiq_proj1_moderate()
    return total_violations

for i in range(0,len(data_fortify_list)):
    fortify_project_id = data_fortify_list[i]
    url_fort_proj1 = 'https://vge1fortify.gemalto.com/ssc/api/v1/projectVersions/' + fortify_project_id +'/issueSummaries?seriestype=ISSUE_FOLDER&groupaxistype=ISSUE_FOLDER'
    url_fort_proj1_lastScan = 'https://vge1fortify.gemalto.com/ssc/api/v1/projectVersions/' + fortify_project_id +'/artifacts?fields=lastScanDate&start=0&limit=1'
    url_fort_proj1_percent_audited = 'https://vge1fortify.gemalto.com/ssc/api/v1/projectVersions/' + fortify_project_id +'/performanceIndicatorHistories/PercentAudited'

    resp_fortify_proj1 = requests.get(url_fort_proj1, verify=False, headers={'Authorization': token}).json()
    resp_fortify_proj1_lastScan = requests.get(url_fort_proj1_lastScan, verify=False, headers={'Authorization': token}).json()
    resp_fortify_proj1_percent_audited = requests.get(url_fort_proj1_percent_audited, verify=False, headers={'Authorization': token}).json()

    # ----- Fortify ---------------------------
    worksheet.write('A1', 'Project_Names', bold)
    worksheet.write('B1', 'Fortify_Url', bold)
    worksheet.write('C1', 'Fortify_LastScanDate', bold)
    worksheet.write('D1', 'Fortify_Critical', bold)
    worksheet.write('E1', 'Fortify_High', bold)
    worksheet.write('F1', 'Fortify_TotalIssueCount', bold)
    worksheet.write('G1', 'Total_Issues_Audited', bold)

    worksheet.write(row+1, column, data_generic_proj_name[i])
    worksheet.write(row+1, column+1,data_fortify_proj_url[i])
    worksheet.write(row+1, column+2, fort_proj1_lastScan())
    worksheet.write(row+1, column+3, fort_proj1_crit())
    worksheet.write(row+1, column+4, fort_proj1_high())
    worksheet.write(row+1, column+5, fort_proj1_totalIssue())
    worksheet.write(row+1, column+6, fort_proj1_percent_audited())
    row += 1

for i in range(0,len(data_sonar_list)):
    sonar_project_key = data_sonar_list[i]

    url_sonar_proj1_critical = 'https://vge1sonar.gemalto.com/api/issues/search?componentKeys=' + sonar_project_key + '&resolved=false&severities=CRITICAL'
    url_sonar_proj1_blocker = 'https://vge1sonar.gemalto.com/api/issues/search?componentKeys=' + sonar_project_key + '&resolved=false&severities=BLOCKER'
    url_sonar_proj1_coverage = 'https://vge1sonar.gemalto.com/api/measures/component?component=' + sonar_project_key + '&metricKeys=coverage'
    url_sonar_proj1_lines_to_cover = 'https://vge1sonar.gemalto.com/api/measures/component?component=' + sonar_project_key + '&metricKeys=lines_to_cover'
    url_sonar_proj1_uncovered_lines = 'https://vge1sonar.gemalto.com/api/measures/component?component=' + sonar_project_key + '&metricKeys=uncovered_lines'
    url_sonar_proj1_tests = 'https://vge1sonar.gemalto.com/api/measures/component?component=' + sonar_project_key + '&metricKeys=tests'
    url_sonar_proj1_test_sucess_density = 'https://vge1sonar.gemalto.com/api/measures/component?component=' + sonar_project_key + '&metricKeys=test_success_density'
    url_sonar_proj1_scan_date = 'https://vge1sonar.gemalto.com/api/project_analyses/search?project=' + sonar_project_key + '&p=1&ps=1'
    url_sonar_proj1_quality_profile= 'https://vge1sonar.gemalto.com/api/qualityprofiles/search?language=java&project=' + sonar_project_key +''
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
    resp_sonar_proj1_critical = requests.get(url_sonar_proj1_critical, verify=False, auth=(user, password)).json()
    resp_sonar_proj1_blocker = requests.get(url_sonar_proj1_blocker, verify=False, auth=(user, password)).json()
    resp_sonar_proj1_coverage = requests.get(url_sonar_proj1_coverage, verify=False, auth=(user, password)).json()
    resp_sonar_proj1_lines_to_cover = requests.get(url_sonar_proj1_lines_to_cover, verify=False, auth=(user, password)).json()
    resp_sonar_proj1_uncovered_lines = requests.get(url_sonar_proj1_uncovered_lines, verify=False, auth=(user, password)).json()
    resp_sonar_proj1_tests = requests.get(url_sonar_proj1_tests, verify=False, auth=(user, password)).json()
    resp_sonar_proj1_test_sucess_density = requests.get(url_sonar_proj1_test_sucess_density, verify=False, auth=(user, password)).json()
    resp_sonar_proj1_scan_date = requests.get(url_sonar_proj1_scan_date, verify=False, auth=(user, password)).json()
    resp_sonar_proj1_quality_profile= requests.get(url_sonar_proj1_quality_profile, verify=False, auth=(user, password)).json()

    #----- Sonar ------------------------------
    worksheet.write('A15', 'Project_Names', bold)
    worksheet.write('B15', 'Sonar_Url', bold)
    worksheet.write('C15', 'Sonar_Last_Scan_Date', bold)
    worksheet.write('D15', 'Sonar_Blocker', bold)
    worksheet.write('E15', 'Sonar_Critical', bold)
    worksheet.write('F15', 'Quality_Gate_Result', bold)
    worksheet.write('G15', 'Sonar_Coverage', bold)
    worksheet.write('H15', 'Sonar_Line_To_Cover', bold)
    worksheet.write('I15', 'Sonar_Uncovered_Lines', bold)
    worksheet.write('J15', 'Sonar_Unit_Tests', bold)
    worksheet.write('K15', 'Test_Sucess Rate', bold)
    worksheet.write('L15', 'Quality_Profile', bold)

    #----------------Sonar Proj 1---------------------------------------------------

    worksheet.write(row+12, column, data_generic_proj_name[i])
    worksheet.write(row+12, column+1,data_sonar_proj_url[i])
    worksheet.write(row+12, column+2, sonar_proj1_scan_date())
    worksheet.write(row+12, column+3, sonar_proj1_blocker())
    worksheet.write(row+12, column+4, sonar_proj1_critical())
    worksheet.write(row+12, column+5, sonar_proj1_quality_gate(sonar_proj1_blocker,sonar_proj1_coverage,sonar_proj1_critical,sonar_proj1_test_success_density))
    worksheet.write(row+12, column+6, sonar_proj1_coverage())
    worksheet.write(row+12, column+7, sonar_proj1_lines_to_cover())
    worksheet.write(row+12, column+8, sonar_proj1_uncovered_lines())
    worksheet.write(row+12, column+9, sonar_proj1_unit_tests())
    worksheet.write(row+12, column+10, sonar_proj1_test_success_density())
    worksheet.write(row+12, column+11, sonar_proj1_quality_profile())
    row += 1
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
for i in range(0,len(data_nexusiq_proj_name)):
    nexusiq_proj1 = data_nexusiq_proj_name[i]
    url_nexusiq_proj1 = 'https://nexusiql1-emea.gemalto.com/rest/application/services/summary?order=APP_NAME_ASC&page=1&pageSize=5000'
    resp_nexusiq_proj1 = requests.get(url_nexusiq_proj1, verify=False, auth=(user, password)).json()
# ----- NexusIQ ---------------------------
    worksheet.write('A25', 'Project_Names', bold)
    worksheet.write('B25', 'NEXUS_IQ_Url', bold)
    worksheet.write('C25', 'NEXUS_IQ_Last_Scan_Date', bold)
    worksheet.write('D25', 'NEXUS_IQ_Critical', bold)
    worksheet.write('E25', 'NEXUS_IQ_Severe', bold)
    worksheet.write('F25', 'NEXUS_IQ_Total_Violations', bold)

    # ----------------NexusIQ Proj 1-----------------------------------------------------
    worksheet.write(row+19, column,   data_generic_proj_name[i])
    worksheet.write(row+19, column+1, data_nexusiq_proj_url[i])
    worksheet.write(row+19, column+2, nexusiq_proj1_time())
    worksheet.write(row+19, column+3, nexusiq_proj1_critical())
    worksheet.write(row+19, column+4, nexusiq_proj1_severe())
    worksheet.write(row+19, column+5, nexusiq_proj1_total_viol())
    row += 1

workbook.close()



