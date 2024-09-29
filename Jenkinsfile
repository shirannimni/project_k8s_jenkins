pipeline {
     agent {
        kubernetes {
            label 'main'
            defaultContainer 'python'
        }
    }

    stages {
        stage('Setup Environment') {
            steps {
                script {
                    sh """
                        # Update package lists
                        apt-get update || true

                        # Install git
                        apt-get install -y git || true

                        # Verify git installation
                        git --version

                        # Check for Python
                        which python3 || echo "Python3 not found"
                        which python || echo "Python not found"

                        # If Python is not found, install it
                        if ! which python3 && ! which python; then
                            apt-get install -y python3 python3-pip || true
                        fi

                        # Verify Python installation
                        python3 --version || echo "Python3 installation failed"
                        pip3 --version || echo "Pip3 installation failed"
                    """
                }
            }
        }


        stage('Unit Test') {
            steps {
                script {
                   sh """
                   mkdir -p \$HOME/python
                   cd \$HOME/python
                   # curl -L https://github.com/indygreg/python-build-standalone/releases/download/20230507/cpython-3.9.16+20230507-x86_64-unknown-linux-gnu-install_only.tar.gz | tar xz --strip-components=1
                   #  export PATH="\$HOME/python/bin:\$PATH"
                   # apt install -y git 
                   git clone https://github.com/shirannimni/project_k8s_jenkins.git
                   
                   python3 --version
                   ls && pwd
                   ./bin/pip install -r ./project_k8s_jenkins/src/requirements.txt
                   """
                  sh 'ls -R $HOME/python/project_k8s_jenkins'
                  sh 'pwd'
                  sh "ls -la && echo $HOME"
                  def testResult = sh(script: '$HOME/python/bin/python3 -m pytest $HOME/python/project_k8s_jenkins/src/test_app.py', returnStatus: true)

              // def testResult = sh(script: '\$HOME/python/bin/python3 -m pytest ./project_k8s_jenkins/src/test_app.py', returnStatus: true)
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
