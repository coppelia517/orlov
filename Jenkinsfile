pipeline {
  agent any
  stages {
    stage('Git Clone') {
      steps {
        git(url: 'https://github.com/coppelia517/orlov', branch: 'master', changelog: true)
      }
    }
  }
}