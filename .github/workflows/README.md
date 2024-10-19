# DevSecOps Pipeline

## Secret Variables

These are the list of variables you need to put in GitHub Actions Repository secrets.

* ARGOCD_AUTH_TOKEN: [{YOUR ARGOCD TOKEN}](https://argo-cd.readthedocs.io/en/stable/user-guide/commands/argocd_account_generate-token/)
* ARGOCD_SERVER: https://argocd.example.com
* DEFECTDOJO_HOST: https://defectdojo.example.com/ (MUST PUT SLASH AT THE END)
* DEFECTDOJO_USERNAME: app-user
* DEFECTDOJO_PASSWORD: [YOUR DEFECTDOJO PASSWORD]
* SONARQUBE_TOKEN: [{YOUR SONARQUBE TOKEN}](https://docs.sonarsource.com/sonarqube/latest/user-guide/managing-tokens/)
* SONARQUBE_HOST: https://sonarcloud.io
* SONARQUBE_ORG: [{YOUR SONARQUBE ORGANIZATION}](https://docs.sonarsource.com/sonarcloud/administering-sonarcloud/managing-organizations/)
