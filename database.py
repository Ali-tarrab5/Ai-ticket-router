from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Database ka naam aur connection URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./tickets.db"

# 2. Engine create karna (Jo database se baat karega)
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# 3. Database Table ka Structure (Schema)
class TicketRecord(Base):
    __tablename__ = "tickets_table"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)
    predicted_department = Column(String)  # AI ne kya socha
    actual_department = Column(String)     # Asal mein kya tha (Human correction ke baad)
    confidence_score = Column(Float)
    is_corrected = Column(Boolean, default=False) # Kya agent ne isay change kiya?

# 4. Table generate karna
Base.metadata.create_all(bind=engine)