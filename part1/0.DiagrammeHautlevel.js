```mermaid
classDiagram
    class PresentationLayer {
        <<interface>>
        +UserService()
        +PlaceService()
        +ReviewService()
        +AmenityService()
    }

    class BusinessLogicLayer {
        +UserModel()
        +PlaceModel()
        +ReviewModel()
        +AmenityModel()
    }

    class PersistenceLayer {
        +UserRepository()
        +PlaceRepository()
        +ReviewRepository()
        +AmenityRepository()
    }

    PresentationLayer --> BusinessLogicLayer : uses (Facade Pattern)
    BusinessLogicLayer --> PersistenceLayer : interacts with (DB operations)
    ```
