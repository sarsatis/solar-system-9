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

    // stage('Build Image') {
    //   steps {
    //     script{
    //         container(name: 'kaniko',shell:'/busybox/sh'){
    //           // sh "cp ${WORKSPACE}/Dockerfile ."
    //           sh "ls"
    //           withCredentials([file(credentialsId: 'docker-credentials', variable: 'DOCKER_CONFIG_JSON')]) {
    //             withEnv(['PATH+EXTRA=/busybox']) {
    //               sh'''#!/busybox/sh
    //               cp $DOCKER_CONFIG_JSON /kaniko/.docker/config.json
    //               /kaniko/executor --force --dockerfile Dockerfile --context `pwd` --destination ${IMAGE_REPO}/${NAME}:${VERSION}
    //               '''
    //             }
    //           }
    //           // kaniko.buildImage dockerfile: 'Dockerfile',
    //           // image: "${NAME}", tags: "${IMAGE_REPO}/${NAME}:${VERSION}"
    //           // sh "docker tag ${NAME}:latest ${IMAGE_REPO}/${NAME}:${VERSION}"    
    //         }
    //       }
    //     }
    //   }

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
            sh 'git clone https://github.com/sarsatis/gitops-argocd'
          }
        }
      }
    }
    
    stage('Update Manifest') {
      steps {
        dir("gitops-argocd/jenkins-demo") {
          sh 'sed -i "s#sarthaksatish.*#${IMAGE_REPO}/${NAME}:${VERSION}#g" deployment.yaml'
          sh 'cat deployment.yaml'
        }
      }
    }

    stage('Commit & Push') {
      steps {
        script {
          dir("gitops-argocd/jenkins-demo") {
            withCredentials([usernamePassword(credentialsId: 'githubpat',
                  usernameVariable: 'username',
                  passwordVariable: 'password')]){
            encodedPassword = URLEncoder.encode("$password",'UTF-8')
            echo "sa ${encodedPassword}"
            sh "git config --global user.email 'jenkins@ci.com'"
            sh "git remote set-url origin https://${username}:${encodedPassword}@github.com/${username}/gitops-argocd.git"
            sh 'git checkout -b feature-test'
            sh 'git add -A'
            sh 'git commit -am "Updated image version for Build - $VERSION"'
            echo 'push started'
            
            sh "git push -u origin feature-test"
                  // sh 'git push origin feature-branch'
            }
            echo 'push complete'
          }
        }
      }
    }

    stage('Raise PR') {
      steps {
        echo 'In Pr'
        sh "bash pr.sh"
      }
    } 
  }
}
