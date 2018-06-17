#!/usr/bin/env groovy

/**
* Jenkinsfile
*/

pipeline {
  agent any
  options {
    buildDiscarder(
      // Only keep the 10 most recent builds
      logRotator(numToKeepStr:'10'))
  }
  environment {
    projectName = 'Orlov Project'
    emailTo = 'dev.coppelia@gmail.com'
    emailFrom = 'dev.coppelia+jenkins@gmail.com'
    PYENV_ROOT = "{env.WORKSPACE}/.pyenv"
    VIRTUALENV = "${env.WORKSPACE}/.venv"
  }
  stages {
    stage('Checkout') {
      steps {
        git(url: 'https://github.com/coppelia517/orlov', branch: 'master', changelog: true)
      }
    }

    stage ('Install Requirements') {
      steps {
        sh """
          echo ${SHELL}
          if [ ! -d ${PYENV_ROOT} ]; then
            git clone https://github.com/yyuu/pyenv.git ${PYENV_ROOT}
            export PATH=${PYENV_ROOT}/bin:$PATH
            eval "\$(pyenv init -)"
            which pyenv
            pyenv install 3.6.5
            pyenv global 3.6.5
          else
            export PATH=${PYENV_ROOT}/bin:$PATH
            eval "\$(pyenv init -)"
            which pyenv
            pyenv global 3.6.5
          fi

          python --version
          
          [ -d ${VIRTUALENV} ] && rm -rf ${VIRTUALENV}
          python -m venv ${VIRTUALENV}
          . ${VIRTUALENV}/bin/activate
          pip install --upgrade pip
          pip install -r requirements_env.txt -r requirements_dev.txt
          """
      }
    }

    stage ('Pylint') {
      steps {
        sh """
          export PATH=${PYENV_ROOT}/bin:$PATH
          eval "\$(pyenv init -)"
          which pyenv
          pyenv global 3.6.5

          python --version
          
          . ${VIRTUALENV}/bin/activate          
          pylint orlov
        """
      }
    }

    stage ('Cleanup') {
      steps {
        sh """
          rm -rf ${VIRTUALENV}
        """
      }
    }
  }
}