from app.models.database import engine
from app.models import model

# app = create_app()


model.Base.metadata.create_all(bind=engine)
