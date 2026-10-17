# Gabriel Barbosa — Cybersecurity Engineer

**Cloud Security · Incident Response · DevSecOps · AI Security**

> **Evidence First. Production Safe. Security by Design.**

[English version](README.md) · [Plano de estudos e exercícios técnicos](LEARNING_PATH.md)

## Sobre

Atuo como **Cybersecurity Engineer na FoundLab**, com foco em segurança cloud-native, resposta a incidentes, DevSecOps e AI Security.

Meu trabalho segue uma disciplina baseada em evidências: definir escopo e autorização, coletar telemetria, separar fatos de hipóteses, validar com segurança, propor controles proporcionais e verificar a remediação.

**Limite de afiliação profissional:** a FoundLab é citada neste repositório apenas como contexto profissional. O repositório diferencia **laboratórios sintéticos**, **evidências públicas do próprio GitHub** e **resumos anonimizados de avaliações que realmente executei**. Não publica arquitetura interna, códigos proprietários, logs brutos, credenciais, achados sensíveis ou configuração real da empresa.

## Visão rápida do portfólio

| Evidência pública | Repositório atual |
|---|---:|
| Case studies de engenharia de segurança | **7** |
| Labs sintéticos hands-on | **5** |
| Ferramentas de segurança executáveis localmente | **3** |
| Testes de regressão do merge gate | **17** |
| Testes do laboratório de incidentes | **14** |
| Testes de segurança cloud (permissões + serverless) | **18** |
| Total de testes unitários Python | **80** |

Os [laboratórios de incidentes](labs/01-cloud-incident-triage/README.md) e de [menor privilégio](labs/02-cloud-least-privilege/README.md) incluem analisadores Python, com 14 testes no laboratório de incidentes e sete no de menor privilégio, com evidências sintéticas e sem acesso a ambientes reais.

## Áreas demonstradas

| Área | Foco |
|---|---|
| **Cloud Security** | IAM, workload identity, least privilege, key management, audit logging e segurança serverless |
| **Incident Response** | triagem, timeline, correlação de logs, preservação de evidências e contenção proporcional |
| **DevSecOps** | CI/CD security gates, SAST, dependency risk, governança de branches e fail-closed controls |
| **AI Security** | AI red teaming, prompt injection, trust boundaries entre modelo/agentes/ferramentas e autorização |
| **Security Governance** | baselines, threat models, playbooks, evidence packages e remediation planning |

## Princípios de engenharia

- **Evidência antes de mutação.**
- **Produção é fonte de evidência, não laboratório.**
- **Claims exigem evidência.**
- **Least privilege por padrão.**
- **Severidade e confiança são dimensões diferentes.**
- **“Desconhecido” é uma conclusão aceitável.**
- **Remediação exige validação e rollback.**
- **IA propõe; pessoas e sistemas autorizados decidem.**

## Trabalhos profissionais em destaque · Estudos sanitizados

As atividades descritas abaixo foram **realizadas em ambientes organizacionais reais**. Os exemplos públicos foram reconstruídos ou generalizados para preservar a confidencialidade. **Dados, métricas e diagramas fictícios não são evidência operacional da empresa.**

| Área | Atividade executada | Versão pública |
|---|---|---|
| **Cloud Security / Governança de IA** | Auditoria READ ONLY de consumo de serviços de IA, observabilidade, rastreabilidade de artefatos e riscos de migração | [Auditoria Cloud & IA — relatório reconstruído](case-studies/07-cloud-ai-continuity-audit/README.md) |
| **Resposta a Incidentes** | Investigação e correlação de eventos de segurança cloud, com conclusões limitadas às evidências | [Cloud-Native Incident Response — edição sanitizada](case-studies/01-cloud-native-incident-response/README.md) |
| **Application Security** | Auditoria real de código e dependências, com análise manual de autorização | [Projeto Lumen — avaliação anonimizada](case-studies/04-ai-security-red-teaming/PROJECT_LUMEN_ASSESSMENT.md) |

**Limite:** trabalho profissional real, reconstrução técnica pública fictícia, sem atestado de terceiros ou divulgação de findings privados.

## Case studies

1. [Cloud-Native Incident Response](case-studies/01-cloud-native-incident-response/README.md) — [relatório profissional sanitizado (PDF)](case-studies/01-cloud-native-incident-response/Cloud_Native_Incident_Response_Public_Portfolio.pdf)
2. [Cloud Security Baseline & Least Privilege](case-studies/02-cloud-security-baseline/README.md)
3. [Deterministic DevSecOps Merge Gate](case-studies/03-devsecops-merge-gate/README.md) — [evidência pública de proteção da main e teste negativo](case-studies/03-devsecops-merge-gate/BRANCH_PROTECTION_VALIDATION.md)
4. [AI Security & Red Teaming](case-studies/04-ai-security-red-teaming/README.md) — [assessment AppSec real e anonimizado — Projeto Lumen](case-studies/04-ai-security-red-teaming/PROJECT_LUMEN_ASSESSMENT.md)
5. [Security Incident Response Playbook](case-studies/05-incident-response-playbook/README.md)
6. [Dependency Vulnerability Triage](case-studies/06-dependency-vulnerability-triage/README.md)
7. [Cloud & AI Infrastructure Security Audit](case-studies/07-cloud-ai-continuity-audit/README.md) — [relatório público reconstruído de 11 seções](case-studies/07-cloud-ai-continuity-audit/PUBLIC_REPORT.md)

## Hands-on labs

- [Lab 01 — Evidence-Driven Cloud Incident Triage](labs/01-cloud-incident-triage/README.md)
- [Lab 02 — Cloud Least-Privilege Review](labs/02-cloud-least-privilege/README.md)
- [Lab 03 — AI Tool Authorization Boundary](labs/03-ai-tool-authorization/README.md)
- [Lab 04 — Deterministic DevSecOps Merge Gate](labs/04-devsecops-merge-gate/README.md)
- [Lab 05 — Dependency Finding Reconciliation](labs/05-dependency-triage/README.md)

## Evidência reproduzível

O [Lab 04](labs/04-devsecops-merge-gate/README.md) contém código executável, fixtures positivas e negativas e testes unitários. O workflow público executa 80 testes unitários, uma checagem sintática e verificação de links locais. A proteção obrigatória da branch é feita pelo ruleset do GitHub, validado com uma [PR negativa](case-studies/03-devsecops-merge-gate/BRANCH_PROTECTION_VALIDATION.md).

## Confidencialidade

Os laboratórios são **sintéticos ou controlados**. Alguns estudos de caso também apresentam **atividades técnicas realmente executadas em avaliações privadas**, com resultados gerais anonimizados e sem divulgação de evidências, configurações ou arquitetura interna. Não publico projetos privados, identidade de clientes, arquitetura interna, tickets, logs reais, credenciais, código proprietário, identificadores operacionais ou findings não públicos.

Consulte a política completa em [SECURITY.md](SECURITY.md).

## Autor

**Gabriel Barbosa · Cybersecurity Engineer**  
**FoundLab**

[GitHub](https://github.com/gabrielbdss) · [LinkedIn](https://www.linkedin.com/in/gabriel-b-souza-silva-255397316)
