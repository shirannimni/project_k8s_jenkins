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
                         # Update package lists and try to fix potential issues
                        apt-get update || true
                        apt-get install -y --fix-missing || true

                        # Install git, python3, and pip3
                        apt-get install -y git python3 python3-pip || true

                        # Verify installations
                        git --version || echo "Git installation failed"
                        python3 --version || echo "Python3 installation failed"
                        pip3 --version || echo "Pip3 installation failed"

                        # If installations failed, try an alternative method
                        if ! command -v python3 &> /dev/null; then
                            echo "Trying alternative Python3 installation method"
                            add-apt-repository ppa:deadsnakes/ppa -y
                            apt-get update
                            apt-get install -y python3.8 python3-pip
                        fi

                        # Verify installations again
                        python3 --version
                        pip3 --version

                         # Upgrade pip to the latest version
                        python3 -m pip install --upgrade pip
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
