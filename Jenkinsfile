

pipeline {
    agent any

    triggers {
        githubPush()  // GitHub Push 이벤트를 트리거로 사용
    }
	
    stages {
        stage('Git Clone') {
            steps {
                // Get some code from a GitHub repository
                git branch: 'main', credentialsId: 'realworldismine', url: 'https://www.github.com/realworldismine/sample-app-docker'
            }
        }
        stage('Docker Image') {
            steps {
                dir('./user') {
                    sh 'sudo docker build -t onikaze/sample-app-docker-user:latest .'
                }
                dir('./post') {
                    sh 'sudo docker build -t onikaze/sample-app-docker-post:latest .'
                }
                dir('./notification') {
                    sh 'sudo docker build -t onikaze/sample-app-docker-notification:latest .'
                }
            }
        }
        stage('Docker Compose') {
            steps {            
                sh '''
                echo "   
EMAIL_SERVER_ADDRESS=
EMAIL_SERVER_FROM=
EMAIL_SERVER_KEY=
EMAIL_SERVER_PORT=
                " > .env
                '''
                sh 'sudo docker-compose up -d'    
            }
        }
    }
}
