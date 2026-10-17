# Cloud & AI Infrastructure — Security and Continuity Assessment

**Sanitized professional work · 11-section public reconstruction · authored by Gabriel Barbosa**

> **Publication boundary:** The author performed an authorized, read-only audit in a real organizational environment. All metrics, models, identifiers, architecture, operational dates, examples, findings and simulated decisions below are **fictional**. This is not the original private report, and no institutional sign-off or production remediation is claimed.


---

**SECURITY ENGINEERING · PUBLIC PORTFOLIO**

# Auditoria de Segurança e Continuidade de Serviços de IA

Avaliação de observabilidade cloud, consumo de serviços de IA, rastreabilidade de entrega e governança de mudanças.
PROVENIÊNCIA E LIMITE DE PUBLICAÇÃO
**Atividade profissional:** avaliação técnica READ ONLY realizada pelo autor em ambiente organizacional real.

**Neste relatório:** todas as identidades, arquiteturas, versões, métricas, proporções, datas operacionais, riscos e amostras são inteiramente **fictícias**. Este documento é uma reconstrução metodológica, não o relatório interno.

GABRIEL BARBOSACYBERSECURITY ENGINEERING · EVIDENCE FIRST / PRODUCTION SAFE

ESTUDO PROFISSIONAL · EDIÇÃO PÚBLICA RECONSTRUÍDA

---

**00 / CLASSIFICAÇÃO**

# O que é real e o que é fictício

A força do estudo está na atividade executada e na forma de raciocinar — não na atribuição de números ilustrativos à organização.
ATIVIDADE REAL, DESCRITA PELO AUTOR
O autor conduziu uma auditoria técnica sob escopo de leitura, combinando observabilidade, informações de execução e registros de entrega para organizar um inventário preliminar e apontar lacunas que condicionam decisões.

RECONSTRUÇÃO ILUSTRATIVA
Todas as tabelas, configurações, esquemas, métricas, riscos específicos e conclusões do exemplo das páginas seguintes foram criados para esta edição pública. Não são evidências da empresa auditada.

| Camada | Estado | Interpretação |
| --- | --- | --- |
| Atividade profissional | REAL — declarada | Avaliação e relatório ocorreram; sem atestado externo nesta publicação. |
| Sistema e organização | OCULTOS | Nenhum alvo ou componente privado pode ser identificado. |
| Métricas e diagramas | FICTÍCIOS | Substitutos didáticos, não cópias de dados operacionais. |
| Aprovação produtiva | NÃO ALEGADA | Este estudo não comprova cutover, remediação ou implantação. |

---

**01 / SUMÁRIO PARA DECISÃO**

# Situação e recomendação

Cenário fictício: uma organização usa mais de um caminho de inferência e precisa entender possíveis dependências legadas.
DECISÃO DEMONSTRATIVA
GO_FOR_PRELIMINARY_INVENTORY_WITH_EXCEPTIONS
HOLD_FOR_PRODUCTION_CHANGE

Aceitar um inventário preliminar condicionado, sem modificar versões, acesso, custo, logs ou roteamento até atribuir responsáveis e obter evidência adequada.

12.480EVENTOS FICTÍCIOS / 90 DIAS
03AMOSTRAS LEGADAS SIMULADAS
70 / 30ROTEAMENTO DECLARADO, FICTÍCIO

### Tese central

Três eventos em uma série agregada não determinam a aplicação que os gerou. Da mesma forma, configurações de duas revisões não comprovam a versão efetivamente servida em cada solicitação.
LIMITE DA EVIDÊNCIA
**UNKNOWN:** sem rastreabilidade de origem, implantação e atendimento, o impacto em consumidores específicos é indeterminado.

A ausência de eventos em janelas delimitadas não demonstra ausência universal de uso. Um CI verde tampouco estabelece o comportamento de todas as chamadas em produção.

---

**02 / ESCOPO E MÉTODO**

# Evidence First / Production Safe

A coleta é limitada por autorização; a decisão deve ser compatível com a qualidade da evidência disponível.

### Permitido: somente leitura

Inventário de integrações e superfícies de IA; análise de métricas agregadas; leitura de configurações e metadados de entrega; registro de lacunas, riscos e responsáveis.

### Não autorizado pelo estudo

Deploy, trocas de versões, reconfiguração de IAM e logs, alterações de tráfego, custos adicionais, aumento de quotas ou cutover produtivo.

**ESCOPO → COLETA → CORRELAÇÃO → DECISÃO**

| Estado | Uso |
| --- | --- |
| OBSERVED | Está presente em fonte delimitada e identificada. |
| VERIFIED | Corroborado por fonte ou controle independente. |
| INFERRED | Interpretação plausível, mas não diretamente demonstrada. |
| UNKNOWN | Lacuna de identificação, cobertura ou contexto impede a resposta. |
| NOT VERIFIED | A hipótese ou ação não foi testada. |
REGRA OPERACIONAL
Produção é fonte de evidências, não ambiente para experimentos não autorizados. Severidade e confiança na conclusão são dimensões diferentes.

---

**03 / ARQUITETURA DE REFERÊNCIA**

# Superfícies e confiança

Diagrama conceitual criado do zero; não revela nem representa a topologia da organização auditada.
APLICAÇÃO AAPI fictícia
APLICAÇÃO BConsumidor fictício

ORQUESTRADORIdentidades a provar
PROVEDOR AServiço fictício
PROVEDOR BAPI simulada

MÉTRICAS · AUDITORIA · METADADOS DE BUILD (FICTÍCIOS)

### Fronteiras que importam

| Fronteira | Pergunta de segurança |
| --- | --- |
| Caller → aplicação | Que identidade originou a chamada? Há identificadores confiáveis para correlacionar? |
| Aplicação → modelo | Configuração declarada e versão realmente atendida são distinguíveis? |
| Build → runtime | Commit, artefato e revisão implantada possuem vinculação verificável? |
| Logs → decisão | Retenção, filtros e permissões tornam a fonte suficientemente completa? |
NÃO INFERIR TOPOLOGIA
Este desenho não representa endpoints, projeto cloud, conta, rede ou arquitetura privados.

---

**04 / INVENTÁRIO E MÉTRICAS**

# Uso histórico simulado

As séries e os totais abaixo são inventados. Janelas sobrepostas nunca devem ser somadas.

### Fonte fictícia A · serviço gerenciado

| Janela | Eventos | Êxitos | Throttle | Uso legado |
| --- | --- | --- | --- | --- |
| 7 dias | 1.120 | 1.118 | 2 | Não visto na amostra |
| 30 dias | 4.620 | 4.605 | 15 | Não visto na amostra |
| 90 dias | 12.480 | 12.411 | 69 | 3 eventos simulados |
INTERPRETAÇÃO
Uma métrica agregada pode indicar o uso de uma versão sem identificar aplicação, chamador, proprietário nem contexto de negócio.

### Fonte fictícia B · API separada

| Janela | Requisições | Rótulos | Limite |
| --- | --- | --- | --- |
| 30 dias | 3.840 | 2 métricos | Inclui operações diversas; não equivale a dois aplicativos nem a uso legado. |

### Hipóteses a validar

H1. Existem integrações legadas ativas? H2. Quem é responsável? H3. Qual funcionalidade seria afetada? H4. Há integrações fora do caminho principal?

**UNKNOWN:** identidade do consumidor, impacto, fallback e necessidade de migração no cenário reconstruído.

---

**05 / RUNTIME E BUILD**

# Configuração não é execução

O que o código declara, o que o runtime implanta e o que a aplicação realmente serve são afirmações distintas.

| Revisão fictícia | Roteamento | Configuração | Serving |
| --- | --- | --- | --- |
| deploy-A | 70% | model-aster-base | NÃO COMPROVADO |
| deploy-B | 30% | model-aster-next | NÃO COMPROVADO |

**CÓDIGO → CI → DIGEST → RUNTIME → SERVING**

### Limites por camada

| Ligação | O que pode demonstrar | O que não demonstra |
| --- | --- | --- |
| Commit ↔ build | Workflow referenciou uma revisão. | Cobertura integral de segurança. |
| Artefato ↔ deploy | Uma revisão declarou um digest. | Atestação criptográfica de toda a cadeia. |
| Runtime ↔ modelo | Configuração da revisão. | Versão servida por requisição. |
| Chamada ↔ consumidor | Identidade, se houver telemetria adequada. | Autoria a partir de métricas agregadas. |
CRITÉRIO DE ENGENHARIA
Não promover o estado `CONFIGURED` a `VERIFIED_SERVING` sem evidência do atendimento real.

---

**06 / IAM, LOGS E CUSTOS**

# Limites e exceções

Ausência de dados e falta de permissão têm significados diferentes; nenhum deles comprova ausência de risco.

| Domínio | Observação fictícia | Conclusão |
| --- | --- | --- |
| Auditoria e logs | Consultas retornam vazio em recortes selecionados. | UNKNOWN: revisar filtros, cobertura e retenção. |
| IAM | Leitura de controles herdados indisponível. | NOT VERIFIED: sem inferir política organizacional. |
| Capacidade | Exportação disponível sem ordens visíveis. | OBSERVED na exportação; não ausência global. |
| Residência | Região do runtime difere do endpoint de inferência. | UNKNOWN até validação contratual e técnica. |
| Custo e SLO | Orçamento de teste adicional não aprovado. | HOLD até autorização. |

### Impacto em segurança

**Detecção:** lacunas reduzem capacidade de atribuir ações. **Autorização:** um subconjunto observável não representa toda a organização. **Continuidade:** dependências sem proprietário e fallback validado merecem triagem. **Governança:** custo, localização lógica e controles precisam de donos.
PRINCÍPIO
Uma exportação vazia não equivale a uma declaração ampla de segurança. Um relatório defensável pode entregar valor com exceções explícitas.

---

**07 / CRITÉRIOS DE ACEITE**

# Sete perguntas de engenharia

As respostas pertencem exclusivamente ao cenário fictício.

| Pergunta | Conclusão ilustrativa | Estado |
| --- | --- | --- |
| 1. Houve uso legado? | Três amostras históricas fictícias. | OBSERVED |
| 2. Quem executou? | Não há IDs de origem confiáveis. | UNKNOWN |
| 3. Serviço principal afetado? | Origem não atribuída. | UNKNOWN |
| 4. Nova versão implantada? | Configuração declarada, serving não provado. | CONFIGURED |
| 5. Risco de continuidade? | Incompatibilidade potencial. | POTENTIAL |
| 6. Plano de migração? | Gates propostos sem execução. | PROPOSED |
| 7. Pendências? | Owners, logs, contrato, orçamento e fallback. | OPEN |
GO DOCUMENTAL NÃO É GO PRODUTIVO
A autorização para aceitar o levantamento preliminar não substitui autorização para mudar modelos, acesso, infraestrutura ou tráfego.

Antes de qualquer mudança real: mapa de consumidores, impacto, testes controlados, rollback, observabilidade, recursos e aprovação técnica/financeira devem estar demonstrados.

---

**08 / RISCOS E PLANO**

# Prioridades e gates

Classificações e prioridades são hipóteses inventadas para ilustrar o método.

| Prioridade simulada | Risco ilustrativo | Próxima validação |
| --- | --- | --- |
| P0 · PROPOSTO | Integração sem proprietário. | Relacionar chamadas à origem autorizada. |
| P0 · PROPOSTO | Configuração confundida com serving. | Recuperar telemetria de atendimento. |
| P1 · PROPOSTO | Logs, quotas ou contrato sem reconciliação. | Designar donos e verificar cobertura. |

### Plano progressivo G0–G6

| Gate | Critério |
| --- | --- |
| G0 Inventário | Fontes, consumidores, limites e riscos sem mutação. |
| G1 Contrato | Compatibilidade, descontinuação, owners. |
| G2 Segurança | Identidades, limites de acesso e logs. |
| G3 Evidências | Correlação entre métricas, artefato, revisão e serving. |
| G4 Custos/SLO | Orçamento, latência e fallback aprovados. |
| G5 Rollout | Canário controlado, monitoramento e rollback. |
| G6 Pós-mudança | Testes, métricas e encerramento documentados. |

---

**09 / CUSTÓDIA E CONCLUSÃO**

# Relatório público, limites claros

A publicação demonstra raciocínio e disciplina técnica sem expor anexos confidenciais.

| Evidência da prática privada | Tratamento nesta edição |
| --- | --- |
| Exportações e séries | Substituídas integralmente por tabelas inventadas. |
| Configurações e metadados | Diagrama genérico e nomes fictícios. |
| Logs e decisões de IAM | Metodologia descrita sem valores internos. |
| Manifesto de arquivos | Nenhum hash privado ou atestado reproduzido. |

### Limitações materiais

**Identificação:** não permite reconstruir serviços, pessoas ou clientes reais. **Integridade:** hash de arquivo não é prova de completude de coleta. **Execução:** a reconstrução não prova migração, ataque ou desempenho real. **Aprovação:** este documento não contém assinatura, validação institucional ou parecer regulatório.
CONCLUSÃO
O diferencial técnico está em separar configuração de execução, evidência de hipótese e recomendação de autorização. **UNKNOWN** é uma conclusão aceitável quando falta prova suficiente. Nenhuma mudança produtiva decorre automaticamente deste estudo.

NOTA EDITORIAL: Estudo público redigido com base em aprendizado de auditoria real, sem transcrever informações confidenciais. Não equivale ao relatório original nem a um atestado sobre ambiente da organização.
