def podTemplate = "podTemplate.yaml"

pipeline {
  agent {
    kubernetes{
      label "jenkins-${UUID.randomUUID().toString()}"
      yamlFile "$podTemplate"
    }
  }

  environment {
    NAME = "solar-system"
    VERSION = "${env.BUILD_ID}-${env.GIT_COMMIT}"
    IMAGE_REPO = "sarthaksatish"
    // ARGOCD_TOKEN = credentials('argocd-token')
    GITHUB_TOKEN = credentials('githubpat')
  }
  
  stages {
    stage('Unit Tests') {
      steps {
        echo 'Implement unit tests if applicable.'
        echo 'This stage is a sample placeholder'
      }
    }

    stage('Build Image') {
      steps {
        script{
            container(name: 'kaniko',shell:'/busybox/sh'){
              // sh "cp ${WORKSPACE}/Dockerfile ."
              sh "ls"
              sh'''#!/busybox/sh
              /kaniko/executor --dockerfile Dockerfile --context `pwd` --destination=${IMAGE_REPO}/${NAME}:${VERSION}
              '''
              // kaniko.buildImage dockerfile: 'Dockerfile',
              // image: "${NAME}", tags: "${IMAGE_REPO}/${NAME}:${VERSION}"
              // sh "docker tag ${NAME}:latest ${IMAGE_REPO}/${NAME}:${VERSION}"    
            }
          }
        }
      }

    // stage('Push Image') {
    //   steps {
    //     withDockerRegistry([credentialsId: "docker-hub", url: ""]) {
    //       sh 'docker push ${IMAGE_REPO}/${NAME}:${VERSION}'
    //     }
    //   }
    // }

    stage('Clone/Pull Repo') {
      steps {
        script {
          if (fileExists('gitops-argocd')) {

            echo 'Cloned repo already exists - Pulling latest changes'

            dir("gitops-argocd") {
              sh 'git pull'
            }

          } else {
            echo 'Repo does not exists - Cloning the repo'
            sh 'git clone -b feature-gitea https://github.com/sarsatis/gitops-argocd'
          }
        }
      }
    }
    
    stage('Update Manifest') {
      steps {
        dir("gitops-argocd/jenkins-demo") {
          sh 'sed -i "s#sarsatis.*#${IMAGE_REPO}/${NAME}:${VERSION}#g" deployment.yaml'
          sh 'cat deployment.yaml'
        }
      }
    }

    stage('Commit & Push') {
      steps {
        dir("gitops-argocd/jenkins-demo") {
          sh "git config --global user.email 'jenkins@ci.com'"
          sh 'git remote set-url origin https://github.com/sarsatis/gitops-argocd'
          sh 'git checkout feature-gitea'
          sh 'git add -A'
          sh 'git commit -am "Updated image version for Build - $VERSION"'
          sh 'git push origin feature-gitea'
        }
      }
    }

    stage('Raise PR') {
      steps {
        sh "bash pr.sh"
      }
    } 
  }
}
