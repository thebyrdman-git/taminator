# Red Hat PAI Architecture Diagrams

## 🏗️ **Overall System Architecture**

```mermaid
graph TB
    subgraph "User Context (Any Directory)"
        U[User] --> PS[PAI Scripts]
        PS --> |"pai-fabric-compliant"| CD{Content Detection}
        PS --> |"pai-fabric-hybrid"| CD
        PS --> |"fabric direct"| FD[Direct Fabric]
    end

    subgraph "Model Selection Logic"
        CD --> |Customer Data| RHM[Red Hat Models]
        CD --> |Personal Data| EXT[External Models]
        FD --> ANY[Any Model Choice]
    end

    subgraph "Fabric AI (Universal)"
        RHM --> |granite-34b-instruct| FAB[Fabric Framework]
        EXT --> |gpt-4o, gemini-pro| FAB
        ANY --> |User Choice| FAB
    end

    subgraph "Model Routing"
        FAB --> ROUTER{Model Router}
        ROUTER --> |Red Hat Models| LITE[LiteLLM Proxy]
        ROUTER --> |External Models| DIRECT[Direct APIs]
    end

    subgraph "Local System"
        LITE --> |localhost:4000| LOCAL[Local LiteLLM Proxy]
    end

    subgraph "Red Hat Infrastructure (via VPN)"
        LOCAL --> |Red Hat VPN| RHI[Red Hat Models]
        RHI --> GRANITE[Granite 34B/7B]
    end

    subgraph "External APIs"
        DIRECT --> OPENAI[OpenAI GPT-4o]
        DIRECT --> GOOGLE[Google Gemini]
        DIRECT --> ANTHROPIC[Claude Sonnet]
    end

    style RHM fill:#ff9999
    style LITE fill:#ff9999
    style GRANITE fill:#ff9999
    style PS fill:#99ccff
    style FAB fill:#99ff99
```

## 🔄 **Model Selection Flow**

```mermaid
flowchart TD
    START[User runs PAI command] --> DETECT{Content Detection}

    DETECT -->|Keywords: customer, case, TAM| CUSTOMER[Customer Data Path]
    DETECT -->|File path: /rh/, .rh extension| CUSTOMER
    DETECT -->|Explicit --redhat flag| CUSTOMER
    DETECT -->|No triggers detected| PERSONAL[Personal Data Path]

    CUSTOMER --> GRANITE_MODEL[Use granite-34b-instruct]
    PERSONAL --> USER_CHOICE[Use preferred model]

    GRANITE_MODEL --> FABRIC_RH[fabric --model granite-34b-instruct]
    USER_CHOICE --> FABRIC_USER[fabric --model gpt-4o/gemini-pro]

    FABRIC_RH --> LITELLM[Route via LiteLLM Proxy]
    FABRIC_USER --> DIRECT_API[Direct to External API]

    LITELLM --> RH_INFRA[Red Hat Infrastructure]
    DIRECT_API --> EXTERNAL[OpenAI/Google/Anthropic]

    RH_INFRA --> AUDIT_LOG[Compliance Audit Log]
    EXTERNAL --> RESULT[Response to User]
    AUDIT_LOG --> RESULT

    style CUSTOMER fill:#ffcccc
    style GRANITE_MODEL fill:#ff9999
    style LITELLM fill:#ff9999
    style RH_INFRA fill:#ff9999
    style AUDIT_LOG fill:#ff9999
```

## 🛠️ **PAI Script Intelligence**

```mermaid
graph LR
    subgraph "Smart PAI Scripts"
        A[pai-fabric-compliant] --> |Always| RH[granite-34b-instruct]
        B[pai-fabric-hybrid] --> |Detection| SMART{Smart Choice}
        C[pai-case-processor] --> |Always| RH
        D[fabric direct] --> |User Choice| ANY[Any Model]
    end

    SMART --> |Customer Content| RH
    SMART --> |Personal Content| EXT[gpt-4o]

    RH --> FABRIC[Fabric AI Framework]
    EXT --> FABRIC
    ANY --> FABRIC

    FABRIC --> ROUTER{Model Router}

    ROUTER --> |granite-*| PROXY[LiteLLM Proxy]
    ROUTER --> |gpt-*| OPENAI_API[OpenAI API]
    ROUTER --> |gemini-*| GOOGLE_API[Google API]

    style A fill:#ff9999
    style C fill:#ff9999
    style RH fill:#ff9999
    style PROXY fill:#ff9999
```

## 🔐 **Compliance Flow**

```mermaid
sequenceDiagram
    participant User
    participant PAI as PAI Script
    participant Fabric as Fabric AI
    participant LiteLLM as LiteLLM Proxy
    participant RH as Red Hat Models
    participant Audit as Audit System

    User->>PAI: Process customer_case.md
    PAI->>PAI: Detect customer data
    PAI->>Fabric: fabric --model granite-34b-instruct

    Fabric->>LiteLLM: API call to granite model
    LiteLLM->>Audit: Log request
    LiteLLM->>RH: Route to Red Hat infrastructure

    RH-->>LiteLLM: AIA-compliant response
    LiteLLM->>Audit: Log response
    LiteLLM-->>Fabric: Return response

    Fabric-->>PAI: Processed content
    PAI->>Audit: Log PAI operation
    PAI-->>User: Results with compliance metadata

    rect rgb(255, 200, 200)
        Note over LiteLLM,Audit: All customer data processing<br/>uses AIA-approved models<br/>with complete audit trail
    end
```

## 🌍 **Global Universal Access**

```mermaid
graph TB
    subgraph "Any Directory"
        DESKTOP[~/Desktop/] --> GLOBAL[Global PAI Context]
        DOCS[~/Documents/] --> GLOBAL
        DOWNLOADS[~/Downloads/] --> GLOBAL
        CODING[~/coding/projects/] --> GLOBAL
    end

    GLOBAL --> DETECT{Context Detection}

    DETECT --> |Red Hat Content| RH_MODE[Red Hat Compliance Mode]
    DETECT --> |Personal Content| PERSONAL_MODE[Personal Mode]

    RH_MODE --> RH_TOOLS[pai-case-processor<br/>pai-fabric-compliant<br/>pai-compliance-check]
    PERSONAL_MODE --> PERSONAL_TOOLS[garcia-daily-brief<br/>analyze-youtube<br/>fabric direct]

    RH_TOOLS --> GRANITE[granite-34b-instruct<br/>via LiteLLM]
    PERSONAL_TOOLS --> ANY_MODEL[gpt-4o, gemini-pro<br/>claude-sonnet, etc.]

    style GLOBAL fill:#99ff99
    style RH_MODE fill:#ffcccc
    style GRANITE fill:#ff9999
```

---

*Visual representation of Red Hat PAI architecture*
*Showing model selection, compliance flow, and universal access*