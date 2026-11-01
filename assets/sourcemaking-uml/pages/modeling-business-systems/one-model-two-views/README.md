# One Model—Two Views

> **Nguồn gốc:** [https://sourcemaking.com/uml/modeling-business-systems/one-model-two-views](https://sourcemaking.com/uml/modeling-business-systems/one-model-two-views)  
> **Phân mục:** SourceMaking UML 2.0 / modeling-business-systems  
> **Số lượng hình ảnh:** 2  

---

/ UML
                                                / Modeling Business Systems

# One Model—Two Views

A business system can be viewed from different perspectives. Because of this, our business system model consists of two different views. Each of the views emphasizes certain aspects of the business system, and each of them is linked to the other. We clarify the different views in Figure 3.3.

Viewing a business system from the outside, we take on the role of a customer, a business partner, a supplier, or another business system. From thisexternal view, only those business processes that involve outsiders are of interest. The external view describes the environment of a business system. The business system itself remains a black box.

Within the business system, we findemployeesandtoolsthat are responsible for fulfilling the demands of the environment, and for handling the necessary business processes. Behind the business processes areworkflowsandIT systems. Each individual employee is part of theorganizational structure. Normally thisinternal viewremains hidden to outsiders.

Take a look at our case study:

- Think about what services Passenger Services provides to you, as a passenger.
- Which employees of Passenger Services are you in contact with as a passenger?
- As a passenger, do you see the procedures that a check-in employee performs, when you are issued your boarding pass? Would you like to know how your luggage ends up in the airplane, or do you not care, as long it doesn’t get lost?

![Figure 3.3 External and internal view of the business system](images/img_16.jpg)

Figure 3.3 External and internal view of the business system

We begin with the external view in modeling our business system. In this way, we start with the description of the business system from the perspective of customers, business partners, and suppliers:

![Figure 3.4 The different views and diagrams](images/img_17.jpg)

Figure 3.4 The different views and diagrams

Following this, the internal view describeshowthe business system provides these services. The use cases of the external view serve well as the basis for constructing test scenarios, which are necessary for testing a finished IT system.

The individual views that we use for the business-system model, and the UML diagrams that they incorporate, are depicted in Figure 3.4.