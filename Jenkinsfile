pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "sultan877/flask-rest-api"
        K8S_NAMESPACE = "flask-app-ns"
        KUBECONFIG_PATH = "/home/muhammad/.kube/config"
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
                    docker run --rm -v "$PWD:/app" -w /app python:3.11 \
                    /bin/bash -c "pip install flake8 pytest && flake8 app && pytest app/test_app.py"
                '''
            }
        }


        stage('Build Docker Image') {
            steps {
                script {
                    def imageTag = "${DOCKER_IMAGE}:${env.BUILD_NUMBER}"
                    sh "docker build -t ${imageTag} ."
                    sh "docker tag ${imageTag} ${DOCKER_IMAGE}:latest"
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh "docker login -u ${DOCKER_USER} -p ${DOCKER_PASS}"
                        sh "docker push ${DOCKER_IMAGE}:${env.BUILD_NUMBER}"
                        sh "docker push ${DOCKER_IMAGE}:latest"
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    sh "kubectl apply -f kubernetes/namespace.yaml --kubeconfig=${KUBECONFIG_PATH}"
                    sh "kubectl apply -f kubernetes/deployment.yaml -n ${K8S_NAMESPACE} --kubeconfig=${KUBECONFIG_PATH}"
                    sh "kubectl apply -f kubernetes/service.yaml -n ${K8S_NAMESPACE} --kubeconfig=${KUBECONFIG_PATH}"
                    sh "kubectl set image deployment/flask-app-deployment flask-app=${DOCKER_IMAGE}:${env.BUILD_NUMBER} -n ${K8S_NAMESPACE} --kubeconfig=${KUBECONFIG_PATH}"
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
