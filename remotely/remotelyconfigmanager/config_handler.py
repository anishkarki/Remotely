from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd
Base = declarative_base()


class Host(Base):
    __tablename__ = "hosts"
    id = Column(Integer, primary_key=True)
    hostname = Column(String,primary_key=True)
    switch_root = Column(String)
    users = relationship("User", back_populates="host")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    command = Column(String)
    host_id = Column(Integer, ForeignKey("hosts.id"))
    host = relationship("Host", back_populates="users")


class Database:
    def __init__(self, db_uri):
        self.engine = create_engine(db_uri)
        self.sessionmaker = sessionmaker(bind=self.engine)

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def get_hosts(self):
        session = self.sessionmaker()
        hosts = session.query(Host).all()
        session.close()
        hosts_data = [{"hostname": h.hostname, "switch_root": h.switch_root} for h in hosts]
        hosts_df = pd.DataFrame(hosts_data)
        return hosts_df

    def create_hosts(self, hostname: str, switch_root: str):
        session = self.sessionmaker()
        host = Host(hostname=hostname, switch_root=switch_root)
        session.add(host)
        session.commit()
        return host