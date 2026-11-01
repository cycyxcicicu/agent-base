# Modeling for System Integration

> **Nguồn gốc:** [https://sourcemaking.com/uml/modeling-for-system-integration](https://sourcemaking.com/uml/modeling-for-system-integration)  
> **Phân mục:** SourceMaking UML 2.0 / general  
> **Số lượng hình ảnh:** 0  

---

/ UML

# Modeling for System Integration

System Integration was long one of the least considered areas within information technology. Only recently, with the emergence of electronic business and Enterprise Application Integration (EAI), it is starting to receive more attention. Even though system integration has existed since the first two IT systems were connected by an interface, only in the last couple of years have standards for the fields of design, method, and implementation became established. This chapter illustrates how UML can be used to model messages and processes for the exchange of these messages.

We understand system integration to be theembeddingof existing and new IT systems into an existing IT environment. Embedding can take place in-house, where we generate interfaces to other IT systems within the organization. Embedding can also span several organizations, where we connect the IT systems of different organizations. Whether the IT systems that need to be integrated in existing infrastructure and processes are within the organization (in-house) or external plays a minor role from a modeling perspective.

Integration of an IT system requires knowledge about the environment of the IT system and its borders. Since an IT system that needs to be integrated has to be embedded into a business environment, the surrounding business processes have to be known. The basis for this is thebusiness system model, which we constructed and described inModeling Business Systems. In order for an IT system to cooperate efficiently with other IT systems, interfaces have to be generated—to in-house IT systems, as well as to the IT systems of other organizations.

In this chapter, we will discuss how to model the messages that are exchanged between the various IT systems, and the processes that are necessary to exchange these messages.