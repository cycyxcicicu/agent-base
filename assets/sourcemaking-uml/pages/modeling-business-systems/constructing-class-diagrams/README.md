# Constructing Class Diagrams

> **Nguồn gốc:** [https://sourcemaking.com/uml/modeling-business-systems/internal-view/constructing-class-diagrams](https://sourcemaking.com/uml/modeling-business-systems/internal-view/constructing-class-diagrams)  
> **Phân mục:** SourceMaking UML 2.0 / modeling-business-systems  
> **Số lượng hình ảnh:** 3  

---

/ UML
                                                / Modeling Business Systems

# Constructing Class Diagrams

The following steps have to be executed for the construction of class diagrams:

#### Checklist 3.9 Constructing Class Diagrams in the Internal View

- Find classes—Which classes exist in the class diagram?
- Create associations between classes—Which classes deal with each other?
- Substantiate associations—What do these relationships mean?
- Insert generalizations—Can business objects be grouped?
- Verify the view—Is everything correct?

### Find Classes—Which Classes Exist in the Class Diagram?

You can use the classes of package diagrams for the class diagram of the business system’s internal view, meaning workers and business objects. Actors from use case diagrams are also classes that can be adopted into this class diagram. In our example, you’ll find the classes that are displayed in Figure 3.37:

![Figure 3.37 Classes of the internal view of the business system](images/img_80.jpg)

Figure 3.37 Classes of the internal view of the business system

### Create Associations Between Classes—Which Classes Deal with Each Other?

In class diagrams, the relationships between the found classes as well as business rules are modeled as associations.

The question is:

What relationships exist between workers, business objects, and other objects?

Even though we begin with the classes that have already been found, we usually find more classes in this work step through domain discussions.

### Substantiate Associations—What do these Relationships Mean?

Associations between individual classes have to be labeled with meaningful names, so that the class diagram can be understood easily and intuitively. Generally, a direction is added to the association, according to which it can be read (see Figure 3.38).

### Insert Generalizations—Can Business Objects be Grouped?

It might make sense to group business objects into another higher-ranking class. In our case study, it is helpful to illustrate that the list of checked-in passengers, the list of passengers on board, and the list of passengers not yet on board, are of the typePassenger List(see Figure 3.39):

![Figure 3.38 Class diagram of passenger services](images/img_81.jpg)

Figure 3.38 Class diagram of passenger services

This shows that the lists have the same structure (see alsoGeneralization, Specialization, and Heredity):

![Figure 3.39 Generalization in the class diagram](images/img_82.jpg)

Figure 3.39 Generalization in the class diagram

### Verify the View—Is Everything Correct?

The completed class diagram can be verified with the following checklist:

#### Checklist 3.10 Verifying Class Diagrams in the Internal View

- Is the class diagram complete? Are all classes from the package diagram also present in the class diagram?
- Are all associations labeled in a meaningful way? Are the directions of the arrows correct?
- Is the class diagram correct? Intensive reading in collaboration with knowledge carriers and a run-through of each service will bring to light most mistakes.
- Is the level of detail optimized? Is the diagram detailed enough to cover everything, or is the diagram too detailed and obscure because it lacks clarity in certain aspects?