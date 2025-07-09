# Nudge Summary Flowchart

```mermaid
flowchart TD
    A[Client Calls /nudges/get-nudge-summary/:employeeId] --> B[Auth Middleware (transparent)]
    B --> C[Property Aggregator Service]

    C --> D1[Async: Fetch Nudges for employeeId]
    C --> D2[Async: Check Existing Summary in DB]

    D1 & D2 --> E[Compare Nudge Snippet]

    E -->|No Change| F[Return Existing Summary]

    E -->|Nudges Updated| G[Trigger LLM Summary Generation (Background)]

    G --> H[LLM Service (Separate Process)]
    H --> I[Generate Summary using OpenAI]
    I --> J[Store New Summary in Client DB]
    J --> K[Publish "summary ready" via Redis]

    K --> L[SSE Gateway]
    L --> M[Client Receives Summary via SSE]

    style G fill:#f9f,stroke:#333,stroke-width:1px
    style H fill:#f9f,stroke:#333,stroke-width:1px
    style L fill:#bbf,stroke:#333,stroke-width:1px

```
