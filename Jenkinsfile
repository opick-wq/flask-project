pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "sultan877/flask-rest-api"
        K8S_NAMESPACE = "flask-app-ns"
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/opick-wq/flask-project.git' // Ganti dengan URL repository Git Anda
            }
        }

        stage('Lint & Test') {
            steps {
                sh 'pip install flake8 pytest'
                sh 'flake8 app --count --select=E9,F63,F7,F82 --show-source --statistics'
                sh 'pytest app/test_app.py'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    def imageTag = "${DOCKER_IMAGE}:${env.BUILD_NUMBER}"
                    sh "docker build -t ${imageTag} ."
                    sh "docker tag ${imageTag} ${DOCKER_IMAGE}:latest" // Tambahkan tag latest
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh "docker login -u ${DOCKER_USER} -p ${DOCKER_PASS}"
                        sh "docker push ${DOCKER_IMAGE}:${env.BUILD_NUMBER}"
                        sh "docker push ${DOCKER_IMAGE}:latest" // Push juga dengan tag latest
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    sh "kubectl apply -f kubernetes/namespace.yaml --kubeconfig=/home/muhammad/.kube/config"
                    sh "kubectl apply -f kubernetes/deployment.yaml -n ${K8S_NAMESPACE} --kubeconfig=/home/muhammad/.kube/config"
                    sh "kubectl apply -f kubernetes/service.yaml -n ${K8S_NAMESPACE} --kubeconfig=/home/muhammad/.kube/config"
                    sh "kubectl set image deployment/flask-app-deployment flask-app=${DOCKER_IMAGE}:${env.BUILD_NUMBER} -n ${K8S_NAMESPACE} --kubeconfig=/path/to/your/kubeconfig"
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