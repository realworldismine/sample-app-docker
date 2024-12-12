pipeline {
    agent any

    triggers {
        githubPush()  // GitHub Push 이벤트를 트리거로 사용
    }
	
    stages {
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
EMAIL_SERVER_ADDRESS=smtp.gmail.com
EMAIL_SERVER_FROM=xinguifeng3@gmail.com
EMAIL_SERVER_KEY=ndfdezhukrftnqox
EMAIL_SERVER_PORT=587
                " > .env
                '''
                sh 'sudo docker-compose up -d'    
            }
        }
    }
}
