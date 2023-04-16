def podTemplate = "podTemplate.yaml"

pipeline {
    agent {
        kubernetes {
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
                script {
                    container(name: 'kaniko') {
                        sh """
                  printenv
                  /kaniko/executor --context `pwd` --destination ${IMAGE_REPO}/${NAME}:${VERSION}
                """
                    }
                }
            }
        }
        stage('Clone/Pull Repo') {
            steps {
                script {
                    sh 'git clone https://github.com/sarsatis/helm-charts'
                    sh 'ls -ltr'
                }
            }
        }
        stage('Commit & Push') {
            steps {
                script {
                    dir("helm-charts/manifests/${NAME}/") {
                        withCredentials([usernamePassword(
                            credentialsId: 'githubpat',
                            usernameVariable: 'username',
                            passwordVariable: 'password'
                        )]) {
                            encodedPassword = URLEncoder.encode("$password", 'UTF-8')
                            echo "sa ${encodedPassword}"
                            sh "git config --global user.email 'jenkins@ci.com'"
                            sh "git remote set-url origin https://${username}:${encodedPassword}@github.com/${username}/helm-charts.git"
                            sh 'sed -i "s#tag:.*#tag: ${VERSION}#g" values-dev.yaml'
                            sh "git checkout -b feature-${env.BUILD_ID}"
                            sh 'cat values-dev.yaml'
                            sh 'git add values-dev.yaml'
                            sh 'git commit -am "Updated image version for Build - $VERSION"'
                            echo 'push started'
                            sh "git push -u feature-${env.BUILD_ID}"
                        }
                        echo 'push complete'
                    }
                }
            }
        }
        stage('Raise PR') {
          steps {
             script {
                withCredentials([usernamePassword(credentialsId: 'githubpat',
                      usernameVariable: 'username',
                      passwordVariable: 'password')]){
                    encodedPassword = URLEncoder.encode("$password",'UTF-8')
                    echo 'In Pr'
                    sh"""
                    curl -L \
                      -X POST \
                      -H "Accept: application/vnd.github+json" \
                      -H "Authorization: Bearer ${encodedPassword}"\
                      -H "X-GitHub-Api-Version: 2022-11-28" \
                      'https://api.github.com/repos/sarsatis/gitops-argocd/pulls' \
                      -d '{
                      "assignee": "sarsatis",
                      "assignees": [
                        "sarsatis"
                      ],
                      "base": "main",
                      "body": "Updated deployment specification with a new image version.",
                      "head": "feature-${env.BUILD_ID}",
                      "title": "Updated Solar System Image"
                      "labels": [
                        "solar-system"
                      ]
                    }'
                """
                      }
                // sh "bash pr.sh"
            }
          }
        }
    }
}
