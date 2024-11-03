pipeline {
    agent {
        kubernetes {
            yaml """
                apiVersion: v1
                kind: Pod
                spec:
                  containers:
                  - name: ubuntu
                    image: ubuntu:22.04
                    command:
                    - sleep
                    args:
                    - 99d
                    tty: true
            """
        }
    }

    stages {
        stage('Setup Environment') {
            steps {
                container('ubuntu') {    // Explicitly specify ubuntu container
                    sh """
                        apt-get update
                        apt-get install -y git python3 python3-pip
                        python3 --version
                        pip3 --version
                        # Update package lists
                        apt-get update
                        
                        # Install prerequisites
                        apt-get install -y \
                            ca-certificates \
                            curl \
                            gnupg \
                            lsb-release \
                            git \
                            python3 \
                            python3-pip

                        # Add Docker's official GPG key
                        mkdir -p /etc/apt/keyrings
                        curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg

                        # Set up Docker repository
                        echo \
                            "deb [arch=\$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
                            \$(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

                        # Update package list again
                        apt-get update

                        # Install Docker
                        apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

                        # Verify Docker installation
                        docker --version
                    """
                }
            }
        }


        stage('Unit Test') {
            steps {
                container("ubuntu") {
                    script {
                        sh """


                        git clone https://github.com/shirannimni/project_k8s_jenkins.git
                    
                        pip3 install -r ./project_k8s_jenkins/src/requirements.txt
                        pip3 install pytest
                        python3 -m pytest ./project_k8s_jenkins/src/test_app.py -v
                        """
                        def testResult = sh(
                            script: """
                                cd \$HOME/python/project_k8s_jenkins/src
                                python3 -m pytest test_app.py -v
                            """,
                            returnStatus: true 
                        )
                       
                    
                        if (testResult != 0) {
                        error "Unit tests failed. Background is not blue."
                        }
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
