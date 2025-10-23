```mermaid
classDiagram
    class User {
        +UUID id
        +String firstName
        +String lastName
        +String email
        +String password
        +Bool isAdmin
        +Date created_at
        +Date updated_at
        +Place[] places
        +Review[] reviews

        +register()
        +updateProfile()
        +delete_account()
    }

    class Place {
        +UUID id
        +String title
        +String description
        +Float price
        +Float latitude
        +Float longitude
        +User owner
        +List<Amenity> amenities
        +Date created_at
        +Date updated_at

        +create()
        +update()
        +delete()
        +List<Place> list()
    }

    class Review {
        +UUID id
        +UUID placeId
        +UUID userId
        +Int rating
        +String comment
        +Date created_at
        +Date updated_at

        +create()
        +update()
        +delete()
        +List<Review> listByPlace(UUID placeId)
    }

    class Amenity {
        +UUID id
        +String name
        +String description
        +Date created_at
        +Date updated_at

        +create()
        +update()
        +delete()
        +List<Amenity> list()
    }

    %% Relations
    User "1" --> "*" Place : owns
    User "1" --> "*" Review : writes
    Place "1" --> "*" Review : has
    Place "1" --> "*" Amenity : includes
    ```
