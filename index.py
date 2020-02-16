import random
from sqlalchemy import create_engine, Table, MetaData, select, Column, String, Integer, SmallInteger, ForeignKey
from sqlalchemy.sql import and_, or_, not_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref


engine = create_engine('sqlite:///db.sqlite3')
connection = engine.connect()
Base = declarative_base()
Session = sessionmaker(bind = engine)
session = Session()


class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    books = relationship("Book", secondary='association_table')

    def __repr__(self):
        return "Author:" + self.first_name


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    copyright = Column(SmallInteger, nullable=False)
    authors = relationship("Author", secondary='association_table')

    def __repr__(self):
        return "Book:" + self.title + str(self.copyright)


class AssociationTable(Base):
    __tablename__ = 'association_table'
    author_id = Column(Integer, ForeignKey('authors.id'), primary_key = True)
    book_id = Column(Integer, ForeignKey('books.id'), primary_key = True)
    author = relationship("Author", backref=backref("association_table", cascade="all, delete-orphan"))
    book = relationship("Book", backref=backref("association_table", cascade="all, delete-orphan"))


Base.metadata.create_all(engine)


a1 = Author(first_name='tolstoy', last_name='lev')
a2 = Author(first_name='turgenev', last_name='ivan')

b1 = Book(title='war and peace', copyright='1880')
b2 = Book(title='anna karenina', copyright='1890')
b3 = Book(title='rudin', copyright='1870')
b4 = Book(title='anekdotes', copyright='1840')


a1.books.append(b1)
a1.books.append(b2)
a2.books.append(b3)

b4.authors.append(a1)
b4.authors.append(a2)

session.add(a1)
session.add(a2)

session.add(b1)
session.add(b2)
session.add(b3)
session.add(b4)

session.commit()


authors_result = []
authors = session.query(Author).all()
for author in authors:
    authors_result.append({'id': author.id, 'first_name': author.first_name})
print('authors:', authors_result, '\n\n')


books = session.query(Book).all()
for book in books:
    print(book, '---', book.id, book.title, book.copyright, '---', book.authors)

