pipeline {
    agent any

    options {
        timestamps()
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/karandesiddhi2006/academic-workload-balancer.git'
            }
        }

        stage('Check Python') {
            steps {
                bat '"C:\\Users\\SIDDHI\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" --version'
            }
        }

        stage('Create Virtual Environment') {
            steps {
                bat '''
                    if exist .venv rmdir /s /q .venv
                    "C:\\Users\\SIDDHI\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -m venv .venv
                    .venv\\Scripts\\python.exe --version
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '.venv\\Scripts\\python.exe -m pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                bat '.venv\\Scripts\\python.exe -m pytest -v'
            }
        }
    }

    post {
        success {
            echo 'CI pipeline completed successfully!'
        }
        failure {
            echo 'CI pipeline failed. Check the console output.'
        }
    }
}
