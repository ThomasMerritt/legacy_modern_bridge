from sqlalchemy import create_engine, Column, Integer, String, Date, Float, MetaData 
from sqlalchemy.orm import declarative_base, sessionmaker

_engine = create_engine("sqlite:///ledger.db")
Session = sessionmaker(bind=_engine)
Base = declarative_base()

class LoadMeta(Base):
    __tablename__ = "load_meta"
    domain = Column(String, primary_key=True)
    source_tag = Column(String)
    schema_version = Column(String)

class LedgerRow(Base):
    __tablename__ = "ledger"
    id = Column(Integer, primary_key=True)
    load_id = Column(Integer, foreign_key="load_meta.id")
    txn_id = Column(Integer, index=True)
    txn_data = Column(String)
    dept_code = Column(String, index=True)
    gl_code = Column(String, index=True)
    amount = Column(Float)
    currency = Column(String, (String(3)))
    description = Column(String)
    fiscal_month = Column(String, index=True)


    

def init_db(url: str):
    global _engine
    _engine = create_engine(url)
    Session.configure(bind=_engine)
    Base.metadata.create_all(_engine)

def begin_load(source_tag, schema_version):
    s = Session()
    lm = LoadMeta(
        domain="ledger",
        source_tag=source_tag,
        schema_version=schema_version
    )
    s.add(lm)
    s.commit()
    return lm.id

def insert_ledger_rows(source_tag: str, schema_version: str):
    s = Session()
    lm = LoadMeta(source_tag=source_tag, schema_version=schema_version)
    s.add(lm)
    s.commit()


