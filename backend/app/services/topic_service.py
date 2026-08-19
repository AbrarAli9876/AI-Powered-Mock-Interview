from sqlalchemy.orm import Session

from app.models.topic import Topic
from app.schemas.topic import TopicCreate, TopicUpdate


class TopicService:
    """
    Handles business logic related to interview topics.
    """

    def __init__(self, db: Session):
        self.db = db

    def create_topic(self, topic_data: TopicCreate) -> Topic:
        """
        Create a new topic.
        """

        existing_topic = (
            self.db.query(Topic)
            .filter(Topic.name == topic_data.name)
            .first()
        )

        if existing_topic:
            raise ValueError("A topic with this name already exists.")

        topic = Topic(
            name=topic_data.name,
            description=topic_data.description,
            is_active=True,
        )

        self.db.add(topic)
        self.db.commit()
        self.db.refresh(topic)

        return topic

    def get_active_topics(self) -> list[Topic]:
        """
        Return all active topics.
        """

        return (
            self.db.query(Topic)
            .filter(Topic.is_active.is_(True))
            .order_by(Topic.name.asc())
            .all()
        )

    def get_topic_by_id(self, topic_id: int) -> Topic | None:
        """
        Retrieve a topic by its ID.
        """

        return (
            self.db.query(Topic)
            .filter(Topic.id == topic_id)
            .first()
        )

    def update_topic(
        self,
        topic_id: int,
        topic_data: TopicUpdate,
    ) -> Topic:
        """
        Update an existing topic.
        """

        topic = self.get_topic_by_id(topic_id)

        if not topic:
            raise ValueError("Topic not found.")

        if topic_data.name is not None:
            existing_topic = (
                self.db.query(Topic)
                .filter(
                    Topic.name == topic_data.name,
                    Topic.id != topic_id,
                )
                .first()
            )

            if existing_topic:
                raise ValueError(
                    "A topic with this name already exists."
                )

            topic.name = topic_data.name

        if topic_data.description is not None:
            topic.description = topic_data.description

        if topic_data.is_active is not None:
            topic.is_active = topic_data.is_active

        self.db.commit()
        self.db.refresh(topic)

        return topic

    def delete_topic(self, topic_id: int) -> Topic:
        """
        Soft-delete a topic by marking it inactive.
        """

        topic = self.get_topic_by_id(topic_id)

        if not topic:
            raise ValueError("Topic not found.")

        topic.is_active = False

        self.db.commit()
        self.db.refresh(topic)

        return topic