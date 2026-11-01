# Modeling Business Systems

> **Nguồn gốc:** [https://sourcemaking.com/uml/modeling-business-systems](https://sourcemaking.com/uml/modeling-business-systems)  
> **Phân mục:** SourceMaking UML 2.0 / general  
> **Số lượng hình ảnh:** 0  

---

/ UML

# Modeling Business Systems

Commercial IT systems are used mainly for dealing with business transactions of various sorts. Because of this, the development and integration of IT systems determine the views of those business processes that are embedded in the IT system. The business system model and its business processes serve as the basis for this. In this chapter we will discuss the construction of business system models.

To ensure smooth business transactions through the use of IT systems, it is indispensable to know and understand thebusiness environmentof IT systems. Therefore, analysis and modeling of business processes are important components of development and integration of IT systems.

Today, most IT systems are not only embedded in a business environment, but are also connected with other IT systems. Thus, every new IT system has to fit not into one, but two different target environments:

- Integration on the business-process level: Each IT system has to be assigned the activities of a business process in a way that enables correct and efficient execution of the entire business process with all involved components.
- Integration at the IT-system level: Communication with other IT systems involved in the business process has to go smoothly. This requires semantically and technically perfect interfaces. Integration on the IT-system level will be discussed inModeling for System Integration.

Answer the following questions for yourself:

- When was the last time you experienced a functional gap between a new IT system and its environment that appeared during the development process?
- How many IT systems do you know that do not optimally support, or even obstruct, the operating processes of users?
- When was the last time you experienced an IT system having to be halted on the day it was rolled out, because a functional error in the interfaces made operation impossible?

We don’t want to look only at the dynamic aspects of our model, but also at the static elements. Because of this, we will construct a business system model that entails both business processes and business structures.