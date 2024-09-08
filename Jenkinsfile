pipeline {
    agent any

    stages {
        stage('Unit Test') {
            steps {
                script {
                    sh "apt-get install python3"
                    sh 'pip install -r requirements.txt'
                    def testResult = sh(script: 'python -m pytest test_app.py', returnStatus: true)
                    if (testResult != 0) {
                        error "Unit tests failed. Background is not blue."
                    }
                }
            }
        }
        
        stage('Build & Tag') {
            steps {
                script {
                    def dockerImage = docker.build("my-app:${env.BUILD_NUMBER}")
                    dockerImage.tag("latest")
                }
            }
        }
        
        stage('Push') {
            steps {
                script {
                    docker.withRegistry('https://hub.docker.com/repository/docker/shirannimni/flask-time-app/general', 'docker-credentials-id') {
                        def dockerImage = docker.image("my-app:${env.BUILD_NUMBER}")
                        dockerImage.push()
                        dockerImage.push("latest")
                    }
                    
                    
                }
            }
        }
        
        stage('Email') {
            steps {
                emailext (
                    subject: "Pipeline Status: ${currentBuild.result}",
                    body: "Build ${env.BUILD_NUMBER} completed. Status: ${currentBuild.result}",
                    to: 'nimnishiran@gmail.com'
                )
            }
        }
    }
}
