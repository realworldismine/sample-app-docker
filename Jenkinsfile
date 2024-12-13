pipeline {
    agent any

    triggers {
        githubPush()
    }
	
    stages {
        stage('Docker Image') {
            steps {
                dir('./user') {
                    docker.build("onikaze/sample-app-docker-user:latest")
                }
                dir('./post') {
                    docker.build("onikaze/sample-app-docker-post:latest")
                }
                dir('./notification') {
                    docker.build("onikaze/sample-app-docker-notification:latest")
                }
            }
        }
        stage('Docker Compose') {
            steps {            
                sh '''
                    export EMAIL_SERVER_ADDRESS=${EMAIL_SERVER_ADDRESS}
                    export EMAIL_SERVER_FROM=${EMAIL_SERVER_FROM}
                    export EMAIL_SERVER_KEY=${EMAIL_SERVER_KEY}
                    export EMAIL_SERVER_PORT=${EMAIL_SERVER_PORT}
                '''
                sh 'sudo docker-compose up -d'    
            }
        }
    }
}
