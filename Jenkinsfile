pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Project checked out from GitHub'
            }
        }

        stage('Setup Python') {
            steps {
                bat '"C:\\Users\\AVICHAL JAIN\\AppData\\Local\\Programs\\Python\\Python312\\python.exe" -m venv .venv'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '.venv\\Scripts\\python.exe -m pip install -r requirements.txt'
            }
        }

        stage('Code Validation') {
            steps {
                bat '.venv\\Scripts\\python.exe -m compileall app.py'
            }
        }

        stage('Build Success') {
            steps {
                echo 'DevOps Monitoring Build Successful!'
            }
        }
    }
}