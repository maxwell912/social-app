def config = [
    namespace: 'pycamp-socialapp-dev',
    image: 'registry.saritasa.com/saritasa/python/pycamp/social-app',
    gitHash: '',

]

node ('docker') {
    try {
        stage('clean') {
            if ("${BUILD_CLEAN}" == "true") {
                cleanWs()
            }

        }

        stage('scm') {
            gitlabCommitStatus('scm') {
                checkout(scm)
                //hash for docker image tags
                config.gitHash = sh(returnStdout: true, script: 'git rev-parse HEAD').take(8)
            }
        }

        stage('build')
        {
            gitlabCommitStatus('build') {
                sh("docker build \
                --file ci/docker/Dockerfile \
                --no-cache=${BUILD_CLEAN} \
                --build-arg APP_ENV=${APP_ENV} \
                --rm --tag ${config.image}:latest .")
            }
        }
        stage('registry') {
            gitlabCommitStatus('registry') {
                withCredentials([usernamePassword(credentialsId: 'jenkins-gitlab-token', passwordVariable: 'PASSWORD', usernameVariable: 'USERNAME')]) {
                sh("docker login --username ${env.USERNAME} --password ${env.PASSWORD} registry.saritasa.com")
                sh("docker push ${config.image}:latest")
                sh("docker tag ${config.image}:latest ${config.image}:${config.gitHash}")
                sh("docker push ${config.image}:${config.gitHash}")
                }
            }
        
        }
        
        stage('migrations') {
            gitlabCommitStatus('migrations') {
                withKubeConfig(credentialsId: 'saritasa-k8s-develop-token', serverUrl: "${K8S_DEVELOPMENT_URL}") {
                sh("kubectl delete -f ci/charts/migrations.yaml || true && \
                kubectl create -f ci/charts/migrations.yaml && \
                kubectl -n ${config.namespace} wait --for=condition=complete --timeout=200s job/migrations")
                }
            }
        }

        stage('deploy'){
            gitlabCommitStatus('deploy') {
                withKubeConfig(credentialsId: 'saritasa-k8s-develop-token', serverUrl: "${K8S_DEVELOPMENT_URL}") {
                    sh("helm --namespace ${config.namespace} \
                    upgrade --install \
                    ${config.namespace} \
                    ci/charts/ \
                    --set=deployment.image.repository=${config.image}:${config.gitHash}")

                }
            }
        }

    currentBuild.result = 'SUCCESS'
    } catch (error) {
        // for future autotests checks
        currentBuild.result = 'FAILURE'
    }
}

