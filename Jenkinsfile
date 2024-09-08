pipeline {
    agent any

    stages {
        stage('Unit Test') {
            steps {
                script {
                    sh "mkdir -p $HOME/python
                    cd $HOME/python
                    curl -L https://github.com/indygreg/python-build-standalone/releases/download/20230507/cpython-3.9.16+20230507-x86_64-unknown-linux-gnu-install_only.tar.gz | tar xz --strip-components=1
                    export PATH="$HOME/python/bin:$PATH""
                    sh " pip install --upgrade pip"
                    sh ' pip install -r /var/jenkins_home/.pyenv/plugins/python-build/scripts/requirements.txt'
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
