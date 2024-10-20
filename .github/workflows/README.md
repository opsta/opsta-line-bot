# DevSecOps Pipeline

## Variables

These are the list of variables you need to put in your GitHub Actions Repository.

### Repository Variables

* IMAGE_REGISTRY: ghcr.io
* IMAGE_REPO: opsta/opsta-line-bot
* IMAGE_NAME: ghcr.io/opsta/opsta-line-bot
* ARGOCD_PROJECT: demo
* PREFIX_K8S_NAMESPACE: demo-opsta-line-bot
* PREFIX_IAC_FILENAME: opsta-line-bot
* HELM_VALUES_PATH: iac/helm-values

### Secret Variables

* ARGOCD_AUTH_TOKEN: [{YOUR ARGOCD TOKEN}](https://argo-cd.readthedocs.io/en/stable/user-guide/commands/argocd_account_generate-token/)
* ARGOCD_SERVER: https://argocd.example.com
* DEFECTDOJO_HOST: https://defectdojo.example.com/ (MUST PUT SLASH AT THE END)
* DEFECTDOJO_USERNAME: app-user
* DEFECTDOJO_PASSWORD: [YOUR DEFECTDOJO PASSWORD]
* SONARQUBE_TOKEN: [{YOUR SONARQUBE TOKEN}](https://docs.sonarsource.com/sonarqube/latest/user-guide/managing-tokens/)
* SONARQUBE_HOST: https://sonarcloud.io
* SONARQUBE_ORG: [{YOUR SONARQUBE ORGANIZATION}](https://docs.sonarsource.com/sonarcloud/administering-sonarcloud/managing-organizations/)
