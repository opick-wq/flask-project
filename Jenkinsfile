pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "sultan877/flask-rest-api"
        K8S_NAMESPACE = "flask-app-ns"
        // Ganti 'your-kubeconfig-credentials-id' dengan ID kredensial kubeconfig Anda di Jenkins
        KUBE_CREDS_ID = 'kubeconfig-dev'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/opick-wq/flask-project.git'
            }
        }

        stage('Lint & Test') {
            steps {
                sh '''
                    echo "--- Setting up Python Virtual Environment ---"
                    python3 -m venv venv
                    
                    echo "--- Activating Virtual Environment ---"
                    . venv/bin/activate
                    
                    echo "--- Installing dependencies ---"
                    # 1. Instal dependensi untuk testing (flake8, pytest)
                    pip install flake8 pytest
                    
                    # 2. Instal dependensi aplikasi dari requirements.txt (INI YANG PENTING)
                    pip install -r app/requirements.txt
                    
                    echo "--- Running Linter ---"
                    flake8 app --count --select=E9,F63,F7,F82 --show-source --statistics
                    
                    echo "--- Running Tests ---"
                    pytest app/test_app.py
                    
                    echo "--- Deactivating Virtual Environment ---"
                    deactivate
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    def imageTag = "${DOCKER_IMAGE}:${env.BUILD_NUMBER}"
                    echo "Building Docker image: ${imageTag}"
                    sh "docker build -t ${imageTag} ."
                    sh "docker tag ${imageTag} ${DOCKER_IMAGE}:latest"
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker-hub', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        echo "Logging in to Docker Hub..."
                        sh "docker login -u ${DOCKER_USER} -p ${DOCKER_PASS}"
                        
                        echo "Pushing image ${DOCKER_IMAGE}:${env.BUILD_NUMBER}"
                        sh "docker push ${DOCKER_IMAGE}:${env.BUILD_NUMBER}"

                        echo "Pushing image ${DOCKER_IMAGE}:latest"
                        sh "docker push ${DOCKER_IMAGE}:latest"
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withKubeConfig(credentialsId: env.KUBE_CREDS_ID) {
                    script {
                        echo "Applying Kubernetes manifests in namespace: ${K8S_NAMESPACE}"
                        sh "kubectl apply -f kubernetes/namespace.yaml"
                        sh "kubectl apply -f kubernetes/deployment.yaml -n ${K8S_NAMESPACE}"
                        sh "kubectl apply -f kubernetes/service.yaml -n ${K8S_NAMESPACE}"
                        
                        echo "Updating deployment image to ${DOCKER_IMAGE}:${env.BUILD_NUMBER}"
                        sh "kubectl set image deployment/flask-app-deployment flask-app=${DOCKER_IMAGE}:${env.BUILD_NUMBER} -n ${K8S_NAMESPACE}"
                    }
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
            cleanWs()
        }
    }
}
