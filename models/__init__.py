from .orm import Base, engine
from .city import City

Base.metadata.create_all(engine)
