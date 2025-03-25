from sqlalchemy.orm import DeclarativeBase
from flask_sqlalchemy import SQLAlchemy


class Base(DeclarativeBase):
    def __repr__(self):
        class_name = type(self).__name__
        class_fields = self.__dict__

        fields = [f"{field}={value}" for field, value in class_fields.items() if
                  not any(e in field for e in ["_sa", "id"])]

        return f"<{class_name}_{self.id} {', '.join(fields)}>"


db = SQLAlchemy(model_class=Base)
