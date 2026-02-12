pipeline {
    parameters {
        // *** In this section you can add strings,booleanParam and modify choices for execution node ***
        choice(choices: ['PRGJENKINSWIN7', 'PRG-Jenkins04','PRG-Jenkins05','PRGJENKINSW10','PRG-Jenkins01','PRG-Jenkins03'], description: 'Choose the agent to execute build', name: 'execution_node')
        booleanParam(name: 'SONAR', defaultValue: true, description: "Run Sonarqube scan")
        booleanParam(name: 'FORTIFY', defaultValue: true, description: "Run Fortify scan")
        booleanParam(name: 'RELEASE', defaultValue: true, description: "Set to 'true' to explicitly trigger Release build deploy on Nexus")
        booleanParam(name: 'SNAPSHOT', defaultValue: false, description: "Set to 'true' to explicitly trigger SNAPSHOT build deploy on Nexus")
        booleanParam(name: 'NEXUSIQ', defaultValue: true, description: "'Run Nexus IQ scan")
        booleanParam(name: 'DOCKER', defaultValue: false, description: "Set to 'true' to explicitly trigger DOCKER BUILD and deploy image on DockerHub")
        booleanParam(name: 'SOAPUI', defaultValue: false, description: 'Run Stage : Integration Test SOAPUI')
		booleanParam(name: 'CLAMAV', defaultValue: false, description: 'Run Stage : CLAMAV Antivirus scan')
    }
    // *** No need to touch this section ***
    agent { label "${execution_node}" }
	tools {
        // Please use java version based on your project
        jdk 'JDK 8u271'
    }
    options {
        timestamps()
        skipDefaultCheckout()
        buildDiscarder(logRotator(numToKeepStr: '5', artifactNumToKeepStr: '1'))
    }

    // *** Load and define parameters used during the pipeline ***
    environment {

        //General pipeline parameters
        WORKSPACE_INNER_DIR = 'DeviceAgents'    //Change it to your workspace

        //MSBuild parameters
        MSBUILD_BUILD_FILE = 'DeviceAgents.sln'  // Change it to your sln file
        BUILD_ARGS = """/t:Restore;Rebuild /p:Configuration=Debug /p:RunOpenCover=true"""    // Change BUILD_ARGS based on your project

        //Fortify parameters
        FORTIFY_FILE = 'DeviceAgents.fpr'   // Change to yours and be careful Fortify is case sensitive
        FORTIFY_PROJECT_NAME = 'GWK20001_Jks_Pipeline'   // Change it to yours
        FORTIFY_VERSION = '1.0.0'   // Change it to yours
        FORTIFY_TOKEN = credentials('ea1781da-b06a-4713-9e50-0514d2396df0')    // No need to change
        LOGFILE = 'scan.log'
		SCA_UPLOAD = 'GWK20001_Mvn_Pipeline@1.0.0.mbs'                         // app-name@vers-name.mbs>: --> name of the application and of the version defined on the SSC server

        //Nexus IQ Parameters
        NEXUSIQ_PROJECT_NAME = 'GWK20001_Jks_Pipeline'   //Change it to yours
        NEXUSIQ_USER = 'ibs_automation'    //No need to change
        NEXUSIQ_GENERIC_SECRET_POWERSHELL = credentials('0c2e2067-87a9-4f12-8c20-6923367a0d09')      //No need to change

        //Sonar Parameters
        SONAR_PROJECT_KEY = 'com.gemalto.ics.GWK20001_Jks_Pipeline'  //Change it to yours but be careful to REGEX (keep com.gemalto.ics.xxx)
        SONAR_PROJECT_NAME = 'com.gemalto.ics.GWK20001_Jks_Pipeline' //Change it to yours
        SONAR_TOKEN = credentials('af5d14f5-524c-4b96-9dac-3d17960a32ec')  //No need to change
        MSBUILD_SQ_SCANNER_HOME = tool name: '5.0.3', type: 'hudson.plugins.sonar.MsBuildSQRunnerInstallation' //No need to change

        //Repository parameters
        REPOSITORY_URL = 'https://vge1hg.gemalto.com/hg/ICS/DeliveryCenter/Passport/Norway-eP2-eID/Module_4a/Application/Device-agents'  //Change it to yours
        REPOSITORY_BRANCH = 'default'   //Change it to yours
        REPOSITORY_CREDS = '7f34684a-afd3-480f-8c35-746727cd542c' //No need to change

        //Mail Parameters  -- You can add more recipients in this section with comma --
        MAIL_RECIPIENTS = 'tural.aliyev@external.thalesgroup.com'

        //Nuget tool
        NUGET = tool name: 'NuGet', type: 'com.cloudbees.jenkins.plugins.customtools.CustomTool'   //No need to change

        //SoapUi tool
        SoapUI = tool name: 'SoapUI', type: 'com.cloudbees.jenkins.plugins.customtools.CustomTool'  //No need to change

        //Docker parameters
        url = "dockerhub.gemalto.com" //No need to change
        registryCredential = '0884a94d-4f0b-4d77-9781-51ca63a9d3f7' // No need to change
        dockerImage = ''    //No need to change

    }
    // *** Checkout with Mercurial (Remove this stage if you are using GIT ) ***
    stages {
        stage('Initialization') {
            steps {
                println "******************************** $STAGE_NAME ********************************"
                script { currentBuild.displayName = currentBuild.displayName + " - ${execution_node}" }
                deleteDir()
                println "******************************** Checkout Repository ********************************"
                checkout(
                        changelog: false,
                        poll: false,
                        scm: [$class       : 'MercurialSCM',
                              credentialsId: """${REPOSITORY_CREDS}""",
                              installation : 'latest',
                              revision     : """${REPOSITORY_BRANCH}""",
                              source       : """${REPOSITORY_URL}"""]
                )
            }
        }
		
		// *** Checkout with GIT ***  (Remove this stage if you are using Mercurial )
		stage('InitializationGIT') {
				steps {
					println "******************************** $STAGE_NAME ********************************"
					bat "dir"
                    script { currentBuild.displayName = currentBuild.displayName + " - ${execution_node}" }
                    deleteDir()
					println "******************************** Checkout Repository ********************************"
					checkout(
                    changelog: false,
                    poll: false,
                    scm: [$class: 'GitSCM',
                            branches: [[name: "${REPOSITORY_BRANCH}"]],
                            userRemoteConfigs: [[credentialsId: """${REPOSITORY_CREDS}""", url: "${REPOSITORY_URL}"]],
                            browser: [$class: 'RhodeCode', url: "${REPOSITORY_URL}"],
                            clean: false
                         ]
                        )
                    }
                }
		
        // *** In this stage change reportsPaths to yours /d:sonar.cs.opencover.reportsPaths= ***
        stage('Sonar Analysis begin') {
            when {
                expression { params.SONAR == true }
            }
            steps {
                echo "********************************Run SonarScanner Begin********************************"
                withSonarQubeEnv('La Ciotat') {
                    bat "${MSBUILD_SQ_SCANNER_HOME}\\SonarScanner.MSBuild.exe begin /k:\"${SONAR_PROJECT_KEY}\" /n:\"${SONAR_PROJECT_NAME}\" /d:sonar.cs.opencover.reportsPaths=DeviceAgent.UnitTests/TestResults/testResult.xml"
                }
            }
        }
        // *** Change Msbuild tool version to yours  ${tool 'xx'} ***
        stage('Build Debug and Unit tests') {
            //when: always
            steps {
                echo "********************************Debug / Unit Test Build********************************"
                bat "${NUGET}\\nuget.exe restore ${MSBUILD_BUILD_FILE}"
                bat "\"${tool '15'}\" ${MSBUILD_BUILD_FILE} ${BUILD_ARGS}"
            }
        }
        // *** No need to change anything in this stage ***
        stage('Sonar Analysis finish') {
            when {
                expression { params.SONAR == true }
            }
            steps {
                echo "********************************Run SonarScanner Finish********************************"
                withSonarQubeEnv('La Ciotat') {
                    bat "${MSBUILD_SQ_SCANNER_HOME}\\SonarScanner.MSBuild.exe end"
                }
            }
        }
        // *** No need to change anything in this stage ***
        stage('Build Release') {
            when {
                expression { params.RELEASE == true }
            }
            steps {
                echo "******************************** Build Release Package ********************************"
                bat """MSBuild.exe ${MSBUILD_BUILD_FILE} ${BUILD_ARGS}"""

            }
        }
        // *** No need to change anything in this stage ***
        stage('Fortify') {
            when {
                expression { params.FORTIFY == true }
            }
            steps {
                echo "********************************Run Fortify Analysis********************************"
                bat "sourceanalyzer -b \"${FORTIFY_PROJECT_NAME}\" -clean -logfile clean.log"
                bat "sourceanalyzer -b \"${FORTIFY_PROJECT_NAME}\" -logfile build.log -libdirs **/* **/*"
                bat "sourceanalyzer -b \"${FORTIFY_PROJECT_NAME}\" -scan -f ${FORTIFY_FILE} -logfile ${LOGFILE}"
                bat "fortifyclient uploadFPR -f ${FORTIFY_FILE} -project \"${FORTIFY_PROJECT_NAME}\" -version ${FORTIFY_VERSION} -url ${FORTIFY_SERVER} -authtoken ${FORTIFY_TOKEN}"

                // if your Fortify scan is taking too much time, you can move the scan on the SCA server directly
				//bat "D:\\pscp.exe -P 22 -hostkey 8f:54:2d:11:01:cb:38:f4:bf:f2:b6:ce:3b:c2:c0:dc -pw scaupload ${SCA_UPLOAD} scaupload@vge1sca.gemalto.com:${SCA_UPLOAD}"

            }
        }
        // *** In this stage you can add scanPattern and modify powershell and ISL json file based on your project ***
        stage('NexusIQ') {
            when {
                expression { params.NEXUSIQ == true }
            }
            steps {
                echo "********************************Restore NuGet packages ********************************"
                bat "dotnet restore ${MSBUILD_BUILD_FILE} --packages ./packages"

                echo "***************************Pack NuGet packages for submit to Nexus IQ***************************"
                powershell script: '''
                    Get-ChildItem -Path "./packages" -Recurse -Include "*.nupkg" -Exclude "Gemalto.*", "Thales.*", "cmiemxsdk.*", "cmcc.sign.*", "cogent.segseqchk.*", "edsdk.*", "emperor.control.*", "fpcaptureaccess.*", "greenbit.*", "mmmsdkwithplugins.*", "openblas.*", "wacomstusdk.*" |
                Compress-Archive -Verbose -DestinationPath "./NexusIqNugetPackages.zip" '''

                echo "********************************Run Nexus IQ analysis ********************************"
                nexusPolicyEvaluation iqApplication: "${NEXUSIQ_PROJECT_NAME}", iqScanPatterns: [[scanPattern: 'NexusIqNugetPackages.zip']], iqStage: "build"
				
				/* To Run ISL analysis uncomment this
                echo "********************************Run ISL analysis ********************************"
                // Please refer to confluence documentation for ISL script https://confluence.gemalto.com/display/ICSKS/ISL+automation+module
                powershell returnStdout: true, script: '''
                    $InformationPreference = "Continue";
                Invoke-OssRequestsRegistration -userCredentials (New-Object System.Management.Automation.PSCredential ("$env:NEXUSIQ_USER", (ConvertTo-SecureString "$env:NEXUSIQ_GENERIC_SECRET_POWERSHELL_PSW" -AsPlainText -Force))) -jsonFilesFolder "./Isl"
                ''' */
            }
        }
		
		 // *** For CLAMAV usage please refer to this page: https://docs.clamav.net/manual/Usage.html?highlight=usage#usage
		stage('CLAMAV') {
            when {
                expression { params.CLAMAV == true }
            }
            steps {
                echo "********************************Run CLAMAV Antivirus********************************"
                bat "clamscan.exe -r %WORKSPACE%\\* > ClamScanResults.txt"
                
            }
        }
        // *** In this stage you can modify powershell based on your project ***
        stage('Upload Snapshot on Nexus') {
            when {
                expression { params.SNAPSHOT == true }
            }
            steps {
                echo "******************************** Archive Snapshot artifacts ********************************"
                // Please find below example with RND script 'NugetPush.ps1', either you can use your script
                // Url for NugetPush.ps1 --> https://vge1hg.gemalto.com/hg/ICS/Shared/NugetScripts/NugetPush/ (Branch: develop)
                powershell script: '''
                    $FILTER = ($env:WORKSPACE + '/Build/NuGet/*.nupkg') 
                    $SOURCE = 'https://nexusl1-emea.gemalto.com/repository/ICS-NuGet-DC-Snapshots/'
					. "${env:WORKSPACE}/NugetPush.ps1"
                    ExecuteScript -nugetFilesFilter $FILTER -nugetSource $SOURCE '''
            }
        }
        // *** In this stage you need to use username for Dockerhub and create Dockerfile ***
        stage('Deploy on Docker') {
            when {
                expression { params.DOCKER == true }
				}
            steps {

                    //build image and publish to dockerHUB
                    step([$class                     : 'DockerBuilderPublisher',
                          cleanImages                : true,
                          cleanupWithJenkinsJobDelete: true,
                          cloud                      : 'docker-prg01',
                          dockerFileDirectory        : '.',   // this is root directory where you need store you your Dockerfile
                          fromRegistry               : ["url": "${url}", "credentialsId": "${registryCredential}"],
                          pushCredentialsId          : """${registryCredential}""",
                          pushOnSuccess              : true,
                          tagsString                 : "${url}/ics_jenkins/myapp$BUILD_NUMBER:latest"  //myapp--> your project name and tag latest can be changed
                    ])

                    // run container
                    step([$class: 'DockerBuilderControl',
                          option: [$class           : 'DockerBuilderControlOptionRun',
                                   cloudName        : 'docker-prg01',
                                   pullCredentialsId: """${registryCredential}""",
                                   image            : "${url}/10062503/myapp$BUILD_NUMBER:latest",  //myapp--> your project name and tag latest can be changed
                                   //dockerCommand: "--name devops-con",
                                   bindPorts        : "8080:8080" // Change it please with Jenkins admin first
                          ]])

                    // Stop container --> Container needed to stop manually on Jenkins node by Jenkins Admin. 
                }
            }

            // *** In this stage you need to use arguments for testrunner ***
            stage('Integration Tests SOAPUI') {
                when {
                    expression { params.SOAPUI == true }
                }
                steps {
                    echo "******************************** Integration Test SOAPUI ********************************"
                    // Please use your own arguments for testrunner like PServiceEndpoint or other's ...
                    bat "${SoapUI}\\testrunner -M -r -PServiceEndpoint=http://Nor3-Docker02:8097/mockCalculatorSoap -f \"SoapUI_Reports\" -s \"TestSuite 1\" -c \"Add\" \"C:\\app\\calculator-soapui-project.xml\""
                }
            }
            // *** In this stage you can modify powershell based on your project ***
            stage('Upload Release on Nexus') {
                when {
                    expression { params.RELEASE == true }
                }
                steps {
                    echo "******************************** Archive Release artifacts ********************************"
                    // Please find below example with RND script 'NugetPush.ps1', either you can use your script
                    // Url for NugetPush.ps1 --> https://vge1hg.gemalto.com/hg/ICS/Shared/NugetScripts/NugetPush/ (Branch: develop)
                    powershell script: '''
                    $FILTER = ($env:WORKSPACE + '/Build/NuGet/*.nupkg')
                    $SOURCE = 'https://nexusl1-emea.gemalto.com/service/local/nuget/ICS-NuGet-DC-RELEASE/'
					. "${env:WORKSPACE}/NugetPush.ps1"
                    ExecuteScript -nugetFilesFilter $FILTER -nugetSource $SOURCE '''
                }
            }
        }

        // *** In this stage you can add more Post steps ***
        post {
            always
                    {
                        step([$class: 'Mailer', recipients: "${MAIL_RECIPIENTS}", sendToIndividuals: true])
                    }

        }
    }