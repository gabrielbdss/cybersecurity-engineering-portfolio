# Estudo de Caso 08 — Operation Cymbal: Cold Room

**Threat Hunting · Resposta a Incidentes · Segurança de IA com base em evidências**

**Evento:** Google Cloud Security Community × Hack The Box (HTB CTF)  
**Período:** 29 de outubro a 1º de novembro de 2026  
**Ambiente:** CTF simulado e autorizado — **não é auditoria de produção nem de empregador**  
**Estado:** **Apresentação pública sem spoilers; soluções preservadas fora do GitHub**  
**Participante:** Gabriel Barbosa · Cybersecurity Engineer

[English](README.md) · [Metodologia](methodology.md) · [Controle de divulgação](DISCLOSURE.md) · [Portfólio](../../README.pt-BR.md)

## Resultado registrado na plataforma

| Indicador | Resultado |
| --- | ---: |
| Cenários concluídos | **3 / 3** |
| Flags aceitas | **18 / 18** |
| Conclusão | **100%** |
| Integrantes cadastrados na equipe | **1** |
| Classificação final oficial | **Não verificada** |

Resultado observado na plataforma HTB. A pontuação do evento é dinâmica; não afirmamos pontuação definitiva nem posição no ranking. Trata-se de uma competição simulada, **não de certificação Google Cloud, endosso dos organizadores ou demonstração da segurança da FoundLab**.

**Transparência quanto à assistência:** foram utilizados recursos de IA conversacional para interpretar logs, apoiar o raciocínio técnico e elaborar documentação. As conclusões foram confrontadas com a telemetria do laboratório e o aceite da plataforma. Uma equipe com um participante não significa resolução sem assistência. A elegibilidade para prêmios depende do regulamento e da decisão dos organizadores.

## Escopo e áreas de prática

| Trilha | Competências praticadas |
| --- | --- |
| **Investigation** | Triagem de eventos Windows e endpoint, identidade e reconstrução de linha do tempo |
| **Threat Hunting** | Hipóteses orientadas por inteligência, consultas SIEM, correlação de logs de nuvem, SaaS e proxy |
| **AI Misuse** | Proveniência de ferramentas de desenvolvimento, relações entre processos, riscos de identidade cloud e CI/CD |

**Ferramentas e fontes analisadas:** Google Security Operations (SecOps), Google Threat Intelligence (GTI), Windows/Sysmon, registros de proxy HTTP e auditoria SaaS, exclusivamente no ambiente controlado da competição.

## Metodologia aplicada

~~~mermaid
flowchart LR
    A["Escopo autorizado"] --> B["Hipótese"]
    B --> C["Telemetria"]
    C --> D["Linha do tempo"]
    D --> E["Corroboração"]
    E --> F["Conclusões e limites"]
~~~

As análises distinguem **OBSERVADO** (registro direto), **CORROBORADO** (evidências independentes), **INFERIDO** (hipótese plausível) e **DESCONHECIDO** (sem comprovação suficiente). Horários próximos, nomes de técnicas ou respostas HTTP isoladas não são provas completas de autoria ou resultado final.

## Aprendizados defensivos

- Vincular consultas do SIEM aos registros originais e normalizar horários.
- Avaliar autenticação, OAuth, permissões excessivas e contas de serviço.
- Investigar a confiança depositada em extensões e ferramentas de desenvolvimento.
- Proteger identidades de automação, scripts de build e pipelines CI/CD.
- Priorizar rastreabilidade, critérios de validação e limites de evidência.

## Restrições de publicação

**Não são publicados:** respostas ou flags, indicadores específicos, identidades e arquivos do desafio, consultas que revelem soluções, comandos operacionais de ataque, logs brutos, screenshots de respostas ou o PDF forense pessoal.

O término do evento **não autoriza automaticamente um write-up público**. Qualquer divulgação técnica futura exige conferir as regras vigentes e obter as autorizações necessárias. Leia [DISCLOSURE.md](DISCLOSURE.md).

Este é um registro independente de participação, não uma publicação oficial do Google ou HTB; a FoundLab é mencionada apenas como contexto profissional, sem implicar patrocínio ou avaliação da empresa.
