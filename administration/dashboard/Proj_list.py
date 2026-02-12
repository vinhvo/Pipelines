fortify_project_id = ['2318','2300','2373']


generic_project_names =['AFR008 Cameroun eID',
                    'AFR026 SENEGAL DL',
                    'C4PG87 Luxembourg eID'
                    ]


fortify_project_urls = ['https://vge1fortify.gemalto.com/ssc/html/ssc/version/2318/overview/null/?filterSet=a243b195-0a59-3f8b-1403-d55b7a7d78e6',
                        'https://vge1fortify.gemalto.com/ssc/html/ssc/version/2300/overview/null/?filterSet=a243b195-0a59-3f8b-1403-d55b7a7d78e6',
                        'https://vge1fortify.gemalto.com/ssc/html/ssc/version/2373/overview/null/?filterSet=a243b195-0a59-3f8b-1403-d55b7a7d78e6',]

sonar_project_keys = ['com.gemaltocogent.cabislib:aslib',
                     'com.gemalto.gbu.france.ingroup.cni:BatchServer',
                     'ics_deliverycenter_CES_Thailand_dl_CES']



sonar_project_urls =['https://vge1sonar.gemalto.com/dashboard?id=com.gemaltocogent.cabislib%3Aaslib',
                     'https://vge1sonar.gemalto.com/dashboard?id=com.gemalto.gbu.france.ingroup.cni%3ABatchServer',
                     'https://vge1sonar.gemalto.com/dashboard?id=ics_deliverycenter_CES_Thailand_dl_CES']


nexusiq_project_id = ['https://nexusiql1-emea.gemalto.com/rest/application/services/summary?order=APP_NAME_ASC&page=1&pageSize=5000',
                      'https://nexusiql1-emea.gemalto.com/rest/application/services/summary?order=APP_NAME_ASC&page=1&pageSize=5000',
                      'https://nexusiql1-emea.gemalto.com/rest/application/services/summary?order=APP_NAME_ASC&page=1&pageSize=5000']

nexusiq_project_names = ['GWK20001_Mvn_Pipeline',
                         'GWK20001_Jks_Pipeline',
                         'AS0043_IDMS']

nexusiq_project_urls = ['https://nexusiql1-emea.gemalto.com/assets/index.html#/management/view/application/GWK20001_Mvn_Pipeline',
                        'https://nexusiql1-emea.gemalto.com/assets/index.html#/management/view/application/GWK20001_Jks_Pipeline',
                        'https://nexusiql1-emea.gemalto.com/assets/index.html#/management/view/application/AS0043_IDMS']



def fort_proj_list():
    return fortify_project_id

def fort_proj_name():
    return fortify_project_names

def fort_proj_url():
    return fortify_project_urls

def sonar_proj_list():
    return sonar_project_keys

def sonar_proj_name():
    return sonar_project_names

def sonar_proj_url():
    return sonar_project_urls

def nexusiq_proj_id():
    return nexusiq_project_id

def nexusiq_proj_name():
    return nexusiq_project_names

def nexusiq_proj_url():
    return nexusiq_project_urls
    
def generic_proj_name():
    return generic_project_names